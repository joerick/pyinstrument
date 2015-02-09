# -*- coding: utf-8 -*-
import sys
import os
import timeit
import signal

from . import recorders
from . import renderers

from rate_limiter import RateLimiter

timer = timeit.default_timer


class NotMainThreadError(Exception):
    '''pyinstrument must be used on the main thread in signal mode'''
    def __init__(self, message=''):
        super(NotMainThreadError, self).__init__(message or NotMainThreadError.__doc__)


class SignalUnavailableError(Exception):
    '''pyinstrument uses signal.SIGALRM in signal mode, which is not available on your system.

    You can pass the argument 'use_signal=False' to run in setprofile mode.'''
    def __init__(self, message=''):
        super(SignalUnavailableError, self).__init__(message or SignalUnavailableError.__doc__)


class Profiler(object):
    def __init__(self, use_signal=True, timeline=True):
        if use_signal:
            try:
                signal.SIGALRM
            except AttributeError:
                raise SignalUnavailableError()

        self.interval = 0.001
        self.use_signal = use_signal
        self.last_profile_time = 0

        if timeline:
            self.recorder = recorders.TimelineRecorder()
        else:
            self.recorder = recorders.TimeAggregateRecorder()

    def start(self):
        self.last_profile_time = timer()

        if self.use_signal:
            try:
                signal.signal(signal.SIGALRM, self._signal)
                # the following tells the system to restart interrupted system calls if they are
                # interrupted before any data has been transferred. This avoids many of the problems
                # related to signals interrupting system calls, see issue #16
                signal.siginterrupt(signal.SIGALRM, False)
            except ValueError:
                raise NotMainThreadError()

            signal.setitimer(signal.ITIMER_REAL, self.interval, 0.0)
        else:
            print 'using rate_limiter'
            sys.setprofile(RateLimiter(self._profile, self.interval))

    def stop(self):
        if self.use_signal:
            signal.setitimer(signal.ITIMER_REAL, 0.0, 0.0)

            try:
                signal.signal(signal.SIGALRM, signal.SIG_IGN)
            except ValueError:
                raise NotMainThreadError()
        else:
            sys.setprofile(None)

    def _signal(self, signum, frame):
        now = timer()
        time_since_last_signal = now - self.last_profile_time

        self.recorder.record_frame(frame, time_since_last_signal)

        signal.setitimer(signal.ITIMER_REAL, self.interval, 0.0)
        self.last_profile_time = now

    def _profile(self, frame, event, arg):
        now = timer()
        time_since_last_signal = now - self.last_profile_time

        if time_since_last_signal < self.interval:
            return

        if event == 'call':
            frame = frame.f_back

        self.recorder.record_frame(frame, time_since_last_signal)

        self.last_profile_time = now

    def root_frame(self):
        """
        Returns the parsed results in the form of a tree of Frame objects
        """
        if not hasattr(self, '_root_frame'):
            self._root_frame = self.recorder.root_frame()

        return self._root_frame

    def first_interesting_frame(self):
        """
        Traverse down the frame hierarchy until a frame is found with more than one child
        """
        frame = self.root_frame()

        while len(frame.children) <= 1:
            if frame.children:
                frame = frame.children[0]
            else:
                # there are no branches
                return self.root_frame()

        return frame

    def starting_frame(self, root=False):
        if root:
            return self.root_frame()
        else:
            return self.first_interesting_frame()

    def output_text(self, root=False, unicode=False, color=False):
        renderer = renderers.ConsoleRenderer(unicode=unicode, color=color)
        return renderer.render(self.starting_frame(root=root))

    def output_html(self, root=False):
        renderer = renderers.HTMLRenderer()
        return renderer.render(self.starting_frame(root=root))

    def output_flame(self, root=False):
        renderer = renderers.FlameRenderer()
        return renderer.render(self.starting_frame(root=root))
