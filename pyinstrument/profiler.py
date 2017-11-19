# -*- coding: utf-8 -*-
import timeit
import warnings

from . import recorders
from . import renderers
from .util import object_with_import_path
from pyinstrument_cext import setstatprofile

timer = timeit.default_timer


class NotMainThreadError(Exception):
    '''deprecated as of 0.14'''
    pass


class SignalUnavailableError(Exception):
    '''deprecated as of 0.14'''
    pass


class Profiler(object):
    def __init__(self, use_signal=None, recorder='time_aggregating'):
        if use_signal is not None:
            warnings.warn('use_signal is deprecated and should no longer be used.', DeprecationWarning, stacklevel=2)

        self.interval = 0.001
        self.last_profile_time = 0

        self.recorder = get_recorder_class(recorder)()

    def start(self):
        self.last_profile_time = timer()
        setstatprofile(self._profile, self.interval)

    def stop(self):
        setstatprofile(None)

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
        return self.output(renderer='text', root=root, unicode=unicode, color=color)

    def output_html(self, root=False):
        return self.output(renderer='html', root=root)

    def output(self, renderer, root=False, **renderer_kwargs):
        renderer_class = get_renderer_class(renderer)
        renderer = renderer_class(**renderer_kwargs)
        return renderer.render(self.starting_frame(root=root))


def get_recorder_class(name):
    if name == 'time_aggregating':
        return recorders.TimeAggregatingRecorder
    elif name == 'timeline':
        return recorders.TimelineRecorder
    else:
        return object_with_import_path(name)


def get_renderer_class(name):
    if name == 'text':
        return renderers.ConsoleRenderer
    elif name == 'html':
        return renderers.HTMLRenderer
    else:
        return object_with_import_path(name)
