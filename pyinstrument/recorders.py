from collections import deque
import abc
from .frame import TimeAggregatingFrame, TimelineFrame
from . import six


class Recorder(object):
    '''
    An object that can record frames and return a tree structure of Frame objects
    '''

    def record_frame(self, frame, time):
        '''
        Record that `time` seconds was spent in `frame`. `frame` is an interpreter frame.
        '''
        raise NotImplementedError()

    def root_frame(self):
        '''
        Output a Frame object that represents the parsed tree of frames
        '''
        raise NotImplementedError()


class TimeAggregatingRecorder(Recorder):
    '''
    Records each frame according to the frame identifiers of the call stack. Does not preserve
    the order in which frames are visited.
    '''
    def __init__(self):
        self.stack_self_time = {}

    def record_frame(self, frame, time):
        stack = self._call_stack_for_frame(frame)
        self.stack_self_time[stack] = self.stack_self_time.get(stack, 0) + time

    def _call_stack_for_frame(self, frame):
        result_list = deque()

        while frame is not None:
            result_list.appendleft(self._identifier_for_frame(frame))
            frame = frame.f_back

        return tuple(result_list)

    def _identifier_for_frame(self, frame):
        # we use a string here as a tuple hashes slower and this is used as a key in a dictionary
        return '%s\x00%s\x00%i' % (
            frame.f_code.co_name, frame.f_code.co_filename, frame.f_code.co_firstlineno
        )

    def root_frame(self):
        root_frame = TimeAggregatingFrame()

        # define a recursive function that builds the hierarchy of frames given the
        # stack of frame identifiers
        def frame_for_stack(stack):
            if len(stack) == 0:
                return root_frame

            parent = frame_for_stack(stack[:-1])
            frame_name = stack[-1]

            if frame_name not in parent.children_dict:
                child = TimeAggregatingFrame(frame_name, parent)
                parent.add_child(child)

            return parent.children_dict[frame_name]

        for stack, self_time in self.stack_self_time.items():
            frame_for_stack(stack).self_time = self_time

        return root_frame


class TimelineRecorder(Recorder):
    '''
    Records every frame separately so that the order that frames are visited is preserved.
    '''
    def __init__(self):
        self.frames = []

    def record_frame(self, frame, time):
        stack = self._call_stack_for_frame(frame)
        self.frames.append((stack, time))

    def _call_stack_for_frame(self, frame):
        result_list = deque()

        while frame is not None:
            result_list.appendleft(self._identifier_for_frame(frame))
            frame = frame.f_back

        return tuple(result_list)

    def _identifier_for_frame(self, frame):
        # we use a string here as a tuple hashes slower and this is used as a key in a dictionary
        return '%s\x00%s\x00%i' % (
            frame.f_code.co_name, frame.f_code.co_filename, frame.f_code.co_firstlineno
        )

    def root_frame(self):
        root_frame = TimelineFrame()

        frame_objects = []

        for frame_tuple in self.frames:
            identifier_stack = frame_tuple[0]
            time = frame_tuple[1]

            # now we must create a stack of frame objects and assign this time to the leaf
            for stack_depth, frame_identifier in enumerate(identifier_stack):
                if stack_depth < len(frame_objects):
                    if frame_identifier != frame_objects[stack_depth].identifier:
                        # trim any frames after and including this one
                        del frame_objects[stack_depth:]

                if stack_depth >= len(frame_objects):
                    if stack_depth == 0:
                        parent = root_frame
                    else:
                        parent = frame_objects[stack_depth-1]

                    frame = TimelineFrame(frame_identifier, parent)
                    parent.add_child(frame)
                    frame_objects.append(frame)

            # trim any extra frames
            del frame_objects[stack_depth+1:]

            # assign the time to the final frame
            frame_objects[-1].self_time += time

        return root_frame
