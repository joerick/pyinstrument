import sys
import os
import time
import inspect
from operator import attrgetter
from pyinstrument.base import BaseProfiler, Frame

class EventProfiler(BaseProfiler):
    def __init__(self):
        self.stack_time = {}
        self.current_call_stack = []
        self.current_call_stack_start_times = []
        self.time_spent_in_profiler = 0

    def start(self):
        for frame_record in inspect.stack()[::-1]:
            # call the profile function as if we just entered all the frames on the stack
            self._profile(frame_record[0], 'call', None)

        sys.setprofile(self._profile)

    def stop(self):
        sys.setprofile(None)

        while len(self.current_call_stack) > 0:
            # call the profile function as if we just left all the frames on the stack
            self._profile(None, 'return', None)

    def _profile(self, frame, event, arg):
        method_time = time.clock()

        if event == 'call':
            self.current_call_stack.append(self._identifier_for_frame(frame))
            self.current_call_stack_start_times.append(method_time - self.time_spent_in_profiler)
        elif event == 'return':
            stack = tuple(self.current_call_stack)
            self.current_call_stack.pop()

            frame_start = self.current_call_stack_start_times.pop()
            frame_duration = method_time - frame_start - self.time_spent_in_profiler
            
            self.stack_time[stack] = self.stack_time.get(stack, 0) + frame_duration

        self.time_spent_in_profiler += time.clock() - method_time

    def root_frame(self):
        """
        Returns the parsed results in the form of a tree of Frame objects
        """
        if not hasattr(self, '_root_frame'):
            self._root_frame = EventFrame()

            # define a recursive function that builds the heirarchy of frames given the
            # stack of frame identifiers
            def frame_for_stack(stack):
                if len(stack) == 0:
                    return self._root_frame

                parent = frame_for_stack(stack[:-1])
                frame_name = stack[-1]

                if not frame_name in parent.children:
                    parent.children[frame_name] = EventFrame(frame_name, parent)

                return parent.children[frame_name]

            for stack_frame in self.stack_time.iteritems():
                frame_for_stack(stack_frame[0]).time = stack_frame[1]

            # fix up root_frames's time so Frame's proportion_of_total works correctly
            for child_frame in self._root_frame.children.values():
                self._root_frame.time += child_frame.time

        return self._root_frame


class EventFrame(Frame):
    def __init__(self, *args, **kwargs):
        super(EventFrame, self).__init__(*args, **kwargs)
        self.time = 0
