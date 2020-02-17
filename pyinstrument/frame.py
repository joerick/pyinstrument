import sys, os, uuid


class BaseFrame(object):
    def __init__(self, parent=None, self_time=0):
        self.parent = parent
        self._self_time = self_time
        self.group = None

    # pylint: disable=W0212
    def remove_from_parent(self):
        '''
        Removes this frame from its parent, and nulls the parent link
        '''
        if self.parent:
            self.parent._children.remove(self)
            self.parent._invalidate_time_caches()
            self.parent = None

    @property
    def proportion_of_parent(self):
        if self.parent:
            try:
                return self.time() / self.parent.time()
            except ZeroDivisionError:
                return float('nan')
        else:
            return 1.0

    @property
    def total_self_time(self):
        '''
        The total amount of self time in this frame (including self time recorded by SelfTimeFrame
        children)
        '''
        self_time = self.self_time
        for child in self.children:
            if isinstance(child, SelfTimeFrame):
                self_time += child.self_time
        return self_time

    @property
    def self_time(self):
        return self._self_time

    @self_time.setter
    def self_time(self, self_time):
        self._self_time = self_time
        self._invalidate_time_caches()

    # invalidates the cache for the time() function.
    # called whenever self_time or _children is modified.
    def _invalidate_time_caches(self):
        pass

    # stylistically I'd rather this was a property, but using @property appears to use twice
    # as many stack frames, so I'm forced into using a function since this method is recursive
    # down the call tree.
    def time(self): raise NotImplementedError()

    @property
    def function(self): raise NotImplementedError()

    @property
    def file_path(self): raise NotImplementedError()

    @property
    def line_no(self): raise NotImplementedError()

    @property
    def file_path_short(self): raise NotImplementedError()

    @property
    def is_application_code(self): raise NotImplementedError()

    @property
    def code_position_short(self): raise NotImplementedError()

    @property
    def children(self): raise NotImplementedError()


class Frame(BaseFrame):
    """
    Object that represents a stack frame in the parsed tree
    """
    def __init__(self, identifier='', parent=None, children=None, self_time=0):
        super(Frame, self).__init__(parent=parent, self_time=self_time)

        self.identifier = identifier
        self._children = []

        self._time = None

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

        self._invalidate_time_caches()
    
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
            file_path = self.file_path

            if ('%slib%s' % (os.sep, os.sep)) in file_path:
                return False

            if file_path.startswith('<'):
                if file_path.startswith('<ipython-input-'):
                    # lines typed at a console or in a notebook are app code
                    return True
                else:
                    # otherwise, this is probably some library-internal code gen
                    return False

            return True

    @property
    def code_position_short(self):
        if self.identifier:
            return '%s:%i' % (self.file_path_short, self.line_no)

    def time(self):
        if self._time is None:
            # can't use a sum(<generator>) expression here sadly, because this method
            # recurses down the call tree, and the generator uses an extra stack frame,
            # meaning we hit the stack limit when the profiled code is 500 frames deep.
            self._time = self.self_time

            for child in self.children:
                self._time += child.time()

        return self._time

    # pylint: disable=W0212
    def _invalidate_time_caches(self):
        self._time = None
        # null all the parent's caches also.
        frame = self
        while frame.parent is not None:
            frame = frame.parent
            frame._time = None


    def __repr__(self):
        return 'Frame(identifier=%s, time=%f, len(children)=%d), group=%r' % (
            self.identifier, self.time(), len(self.children), self.group
        )


class SelfTimeFrame(BaseFrame):
    """
    Represents a time spent inside a function
    """
    def time(self): 
        return self.self_time
    
    @property
    def function(self): return '[self]'

    @property
    def _children(self): return []

    @property
    def children(self): return []

    @property
    def file_path(self): return self.parent.file_path

    @property
    def line_no(self): return self.parent.line_no

    @property
    def file_path_short(self): return ''

    @property
    def is_application_code(self): return False

    @property
    def code_position_short(self): return ''

    @property
    def identifier(self): return '[self]'


class FrameGroup(object):
    def __init__(self, root, **kwargs):
        super(FrameGroup, self).__init__(**kwargs)
        self.root = root
        self.id = str(uuid.uuid4())
        self._frames = []
        self._exit_frames = None
        self._libraries = None

        self.add_frame(root)
    
    @property
    def libraries(self):
        if self._libraries is None:
            libraries = []
            for frame in self.frames:
                library = frame.file_path_short.split(os.sep)[0]
                library, _ = os.path.splitext(library)
                if library and library not in libraries:
                    libraries.append(library)
            self._libraries = libraries      

        return self._libraries

    @property
    def frames(self):
        return tuple(self._frames)

    # pylint: disable=W0212
    def add_frame(self, frame):
        if frame.group:
            frame.group._frames.remove(frame)

        self._frames.append(frame)
        frame.group = self

    @property
    def exit_frames(self):
        '''
        Returns a list of frames whose children include a frame outside of the group
        '''
        if self._exit_frames is None:
            exit_frames = []
            for frame in self.frames:
                if any(c.group != self for c in frame.children):
                    exit_frames.append(frame)
            self._exit_frames = exit_frames

        return self._exit_frames

    def __repr__(self):
        return 'FrameGroup(len(frames)=%d)' % len(self.frames)
