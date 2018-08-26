# -*- coding: utf-8 -*-
import timeit
import warnings

from . import renderers
from pyinstrument.frame import Frame
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
    def __init__(self, interval=0.001, use_signal=None, recorder=None):
        if use_signal is not None:
            warnings.warn('use_signal is deprecated and should no longer be used.', 
                          DeprecationWarning,
                          stacklevel=2)
        if recorder is not None:
            warnings.warn('recorder is deprecated and should no longer be used.',
                          DeprecationWarning,
                          stacklevel=2)

        self.interval = interval
        self.last_profile_time = 0.0
        self.frame_records = []

    def start(self):
        self.last_profile_time = timer()
        setstatprofile(self._profile, self.interval)

    def stop(self):
        setstatprofile(None)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    # pylint: disable=W0613
    def _profile(self, frame, event, arg):
        now = timer()
        time_since_last_profile = now - self.last_profile_time

        if time_since_last_profile < self.interval:
            return

        if event == 'call':
            frame = frame.f_back

        self._record_frame(frame, time_since_last_profile)

        self.last_profile_time = now

    def _record_frame(self, frame, time):
        call_stack = []

        while frame is not None:
            identifier = '%s\x00%s\x00%i' % (
                frame.f_code.co_name, frame.f_code.co_filename, frame.f_code.co_firstlineno
            )
            call_stack.append(identifier)
            frame = frame.f_back

        # we iterated from the leaf to the root, we actually want the call stack
        # starting at the root, so reverse this array
        call_stack.reverse()
        self.frame_records.append((call_stack, time))

    def root_frame(self):
        ''' 
        Parses the internal frame records and returns a tree of Frame objects
        '''
        root_frame = Frame()

        frame_stack = []

        for frame_tuple in self.frame_records:
            identifier_stack = frame_tuple[0]
            time = frame_tuple[1]

            # now we must create a stack of frame objects and assign this time to the leaf
            for stack_depth, frame_identifier in enumerate(identifier_stack):
                if stack_depth < len(frame_stack):
                    if frame_identifier != frame_stack[stack_depth].identifier:
                        # trim any frames after and including this one
                        del frame_stack[stack_depth:]

                if stack_depth >= len(frame_stack):
                    if stack_depth == 0:
                        parent = root_frame
                    else:
                        parent = frame_stack[stack_depth-1]

                    frame = Frame(frame_identifier)
                    parent.add_child(frame)
                    frame_stack.append(frame)

            # trim any extra frames
            del frame_stack[stack_depth+1:]

            # assign the time to the final frame
            frame_stack[-1].self_time += time

        return root_frame

    def first_interesting_frame(self):
        """
        Traverse down the frame hierarchy until a frame is found with more than one child
        """
        root_frame = self.root_frame()
        frame = root_frame

        while len(frame.children) <= 1:
            if frame.children:
                frame = frame.children[0]
            else:
                # there are no branches
                return root_frame

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
        if not isinstance(renderer, renderers.Renderer):
            renderer_class = get_renderer_class(renderer)
            renderer = renderer_class(**renderer_kwargs)

        return renderer.render(self.starting_frame(root=root))


def get_renderer_class(renderer):
    if callable(renderer):
        # allow just passing the class object itself
        return renderer

    if renderer == 'text':
        return renderers.ConsoleRenderer
    elif renderer == 'html':
        return renderers.HTMLRenderer
    elif renderer == 'json':
        return renderers.JSONRenderer
    else:
        return object_with_import_path(renderer)
