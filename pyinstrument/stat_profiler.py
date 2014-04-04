import time
import signal
from collections import deque
from pyinstrument.profiler import BaseProfiler, Frame


class StatProfiler(BaseProfiler):
    def __init__(self, *args, **kwargs):
        self.next_profile_time = 0
        self.interval = 0.001
        self.stack_self_time = {}
        super(StatProfiler, self).__init__(*args, **kwargs)

    def start(self):
        signal.signal(signal.SIGPROF, self.signal)
        signal.setitimer(signal.ITIMER_PROF, self.interval, 0.0)

    def stop(self):
        signal.setitimer(signal.ITIMER_PROF, 0.0, 0.0)
        signal.signal(signal.SIGPROF, signal.SIG_IGN)

    def signal(self, signum, frame):
        stack = self.call_stack_for_frame(frame)
        self.stack_self_time[stack] = self.stack_self_time.get(stack, 0) + self.interval

        signal.setitimer(signal.ITIMER_PROF, self.interval, 0.0)

    def call_stack_for_frame(self, frame):
        result_list = deque()

        while frame is not None:
            result_list.appendleft(self._identifier_for_frame(frame))
            frame = frame.f_back

        return tuple(result_list)

    def root_frame(self):
        """
        Returns the parsed results in the form of a tree of Frame objects
        """
        if not hasattr(self, '_root_frame'):
            self._root_frame = StatFrame()

            # define a recursive function that builds the heirarchy of frames given the
            # stack of frame identifiers
            def frame_for_stack(stack):
                if len(stack) == 0:
                    return self._root_frame

                parent = frame_for_stack(stack[:-1])
                frame_name = stack[-1]

                if not frame_name in parent.children:
                    parent.children[frame_name] = StatFrame(frame_name, parent)

                return parent.children[frame_name]

            for stack, self_time in self.stack_self_time.iteritems():
                frame_for_stack(stack).self_time = self_time

        return self._root_frame


class StatFrame(Frame):
    def __init__(self, *args, **kwargs):
        super(StatFrame, self).__init__(*args, **kwargs)
        self.self_time = 0

    @property
    def time(self):
        if not hasattr(self, '_time'):
            self._time = sum(child.time for child in self.children.values()) + self.self_time
        return self._time

