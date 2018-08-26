import sys, os


class Frame(object):
    """
    Object that represents a stack frame in the parsed tree
    """
    def __init__(self, identifier='', parent=None, children=None, self_time=0):
        self.identifier = identifier
        self.parent = parent
        self.self_time = self_time
        self._children = []

        self._time = None
        self._proportion_of_parent = None
        self._proportion_of_total = None

        if children:
            for child in children:
                self.add_child(child)
    
    def add_child(self, frame, after=None):
        '''
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        '''
        frame.remove_from_parent()
        frame.parent = self
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, frame)

        self._invalidate_tree_caches()
    
    def add_children(self, frames, after=None):
        '''
        Convenience method to add multiple frames at once.
        '''
        if after is not None:
            # if there's an 'after' parameter, add the frames in reverse so the order is
            # preserved.
            for frame in reversed(frames):
                self.add_child(frame, after=after)
        else:
            for frame in frames:
                self.add_child(frame)

    # pylint: disable=W0212
    def remove_from_parent(self):
        '''
        Removes this frame from its parent, and nulls the parent link
        '''
        if self.parent:
            self.parent._children.remove(self)
            self.parent._invalidate_tree_caches()
            self.parent = None

        self._invalidate_tree_caches()

    @property
    def children(self):
        # Return an immutable copy (this property should only be mutated using methods)
        # Also, returning a copy avoid problems when mutating while iterating, which happens a lot
        # in processors!
        return tuple(self._children)

    @property
    def function(self):
        if self.identifier:
            return self.identifier.split('\x00')[0]

    @property
    def file_path(self):
        if self.identifier:
            return self.identifier.split('\x00')[1]

    @property
    def line_no(self):
        if self.identifier:
            return int(self.identifier.split('\x00')[2])

    @property
    def file_path_short(self):
        """ Return the path resolved against the closest entry in sys.path """
        if not hasattr(self, '_file_path_short'):
            if self.file_path:
                result = None

                for path in sys.path:
                    # On Windows, if self.file_path and path are on different drives, relpath
                    # will result in exception, because it cannot compute a relpath in this case.
                    # The root cause is that on Windows, there is no root dir like '/' on Linux.
                    try:
                        candidate = os.path.relpath(self.file_path, path)
                    except ValueError:
                        continue

                    if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                        result = candidate

                self._file_path_short = result
            else:
                self._file_path_short = None

        return self._file_path_short

    @property
    def is_application_code(self):
        if self.identifier:
            return ('%slib%s' % (os.sep, os.sep)) not in self.file_path

    @property
    def code_position_short(self):
        if self.identifier:
            return '%s:%i' % (self.file_path_short, self.line_no)

    # stylistically I'd rather this was a property, but using @property appears to use twice
    # as many stack frames, so I'm forced into using a function since this method is recursive
    # down the call tree.
    def time(self):
        if self._time is None:
            # can't use a sum(<generator>) expression here sadly, because this method
            # recurses down the call tree, and the generator uses an extra stack frame,
            # meaning we hit the stack limit when the profiled code is 500 frames deep.
            self._time = self.self_time

            for child in self.children:
                self._time += child.time()

        return self._time

    @property
    def proportion_of_parent(self):
        if self._proportion_of_parent is None:
            if self.parent and self.time():
                try:
                    self._proportion_of_parent = self.time() / self.parent.time()
                except ZeroDivisionError:
                    self._proportion_of_parent = float('nan')
            else:
                self._proportion_of_parent = 1.0

        return self._proportion_of_parent

    @property
    def proportion_of_total(self):
        if self._proportion_of_total is None:
            if not self.parent:
                self._proportion_of_total = 1.0
            else:
                self._proportion_of_total = (self.parent.proportion_of_total 
                                             * self.proportion_of_parent)

        return self._proportion_of_total

    def _invalidate_tree_caches(self):
        # should be called when manipulating the tree i.e. when changing `parent` or `children`
        # properties.
        self._time = None
        self._proportion_of_parent = None
        self._proportion_of_total = None

    def __repr__(self):
        return 'Frame(identifier=%s, time=%f, len(children)=%d)' % (
            self.identifier, self.time(), len(self.children)
        )
