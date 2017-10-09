import sys, os
from operator import methodcaller


class Frame(object):
    """
    Object that represents a stack frame in the parsed tree
    """
    def __init__(self, identifier='', parent=None):
        self.identifier = identifier
        self.parent = parent
        self.self_time = 0

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
        if not hasattr(self, '_time'):
            # can't use a sum(<generator>) expression here sadly, because this method
            # recurses down the call tree, and the generator uses an extra stack frame,
            # meaning we hit the stack limit when the profiled code is 500 frames deep.
            self._time = self.self_time

            for child in self.children:
                self._time += child.time()

        return self._time

    @property
    def proportion_of_parent(self):
        if not hasattr(self, '_proportion_of_parent'):
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
        if not hasattr(self, '_proportion_of_total'):
            if not self.parent:
                self._proportion_of_total = 1.0
            else:
                self._proportion_of_total = self.parent.proportion_of_total * self.proportion_of_parent

        return self._proportion_of_total

    def add_child(self, child):
        self.children.append(child)

    @property
    def children(self):
        raise NotImplementedError()

    def __repr__(self):
        return 'Frame(identifier=%s, time=%f, len(children)=%d)' % (self.identifier, self.time(), len(self.children))


class TimelineFrame(Frame):
    def __init__(self, *args, **kwargs):
        self._children = []
        super(TimelineFrame, self).__init__(*args, **kwargs)

    def add_child(self, child):
        self._children.append(child)

    @property
    def children(self):
        return self._children


class TimeAggregatingFrame(Frame):
    def __init__(self, *args, **kwargs):
        self.children_dict = {}
        super(TimeAggregatingFrame, self).__init__(*args, **kwargs)

    def add_child(self, child):
        self.children_dict[child.identifier] = child

    @property
    def children(self):
        if not hasattr(self, '_children'):
            unsorted_children = self.children_dict.values()
            self._children = sorted(unsorted_children, key=methodcaller('time'), reverse=True)

        return self._children
