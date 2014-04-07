import signal
from collections import deque
import timeit
from pyinstrument.base import BaseProfiler, Frame

timer = timeit.default_timer


class NotMainThreadError(Exception):
    """pyinstrument.StatProfiler must be used on the main thread"""
    def __init__(self, message=''):
        super(NotMainThreadError, self).__init__(message or NotMainThreadError.__doc__)


class StatProfiler(BaseProfiler):
    def __init__(self, *args, **kwargs):
        try:
            signal.SIGALRM
        except AttributeError:
            raise AttributeError('pyinstrument.StatProfiler uses signal.SIGALRM, which is not available on your system. Consider using pyinstrument.EventProfiler instead.')

        self.next_profile_time = 0
        self.interval = 0.001
        self.last_signal_time = 0
        self.stack_self_time = {}
        super(StatProfiler, self).__init__(*args, **kwargs)

    def start(self):
        try:
            signal.signal(signal.SIGALRM, self.signal)
        except ValueError:
            raise NotMainThreadError()

        signal.setitimer(signal.ITIMER_REAL, self.interval, 0.0)
        self.last_signal_time = timer()

    def stop(self):
        signal.setitimer(signal.ITIMER_REAL, 0.0, 0.0)

        try:
            signal.signal(signal.SIGALRM, signal.SIG_IGN)
        except ValueError:
            raise NotMainThreadError()

    def signal(self, signum, frame):
        now = timer()
        time_since_last_signal = now - self.last_signal_time

        stack = self._call_stack_for_frame(frame)
        self.stack_self_time[stack] = self.stack_self_time.get(stack, 0) + time_since_last_signal

        signal.setitimer(signal.ITIMER_REAL, self.interval, 0.0)
        self.last_signal_time = now

    def _call_stack_for_frame(self, frame):
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
