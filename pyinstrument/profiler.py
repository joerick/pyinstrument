# -*- coding: utf-8 -*-
from typing import Union
from pyinstrument.stack_sampler import build_call_stack, get_stack_sampler
import timeit, time, sys, inspect
from contextvars import ContextVar
from pyinstrument import renderers
from pyinstrument.session import ProfilerSession
from pyinstrument.util import file_supports_color, file_supports_unicode

try:
    from time import process_time
except ImportError:
    process_time = None

timer = timeit.default_timer


active_profiler_context_var: ContextVar[Union['Profiler', None]] = ContextVar('active_profiler_context_var', default=None)


class Profiler(object):
    def __init__(self, interval=0.001):
        self.interval = interval
        self.last_profile_time = 0.0
        self.frame_records = []
        self._start_time = None
        self._start_process_time = None
        self.last_session = None
        self.context_var_token = None

    def start(self, caller_frame=None):
        if active_profiler_context_var.get() is not None:
            raise RuntimeError(
                'A profiler is already running. Running multiple profilers on the same thead is not '
                'supported, unless they\'re in different async contexts.'
            )

        self._start_time = time.time()

        if process_time:
            self._start_process_time = process_time()
        if caller_frame is None:
            caller_frame = inspect.currentframe().f_back

        self._start_call_stack = build_call_stack(caller_frame, 'initial', None)

        self.context_var_token = active_profiler_context_var.set(self)
        get_stack_sampler().subscribe(self._sampler_saw_call_stack, self.interval)

    def stop(self):
        get_stack_sampler().unsubscribe(self._sampler_saw_call_stack)
        active_profiler_context_var.reset(self.context_var_token)

        if process_time:
            cpu_time = process_time() - self._start_process_time
            self._start_process_time = None
        else:
            cpu_time = None

        self.last_session = ProfilerSession(
            frame_records=self.frame_records,
            start_time=self._start_time,
            duration=time.time() - self._start_time,
            sample_count=len(self.frame_records),
            program=' '.join(sys.argv),
            start_call_stack=self._start_call_stack,
            cpu_time=cpu_time,
        )

        return self.last_session

    def __enter__(self):
        self.start(caller_frame=inspect.currentframe().f_back)
        return self

    def __exit__(self, *args):
        self.stop()

    # pylint: disable=W0613
    def _sampler_saw_call_stack(self, call_stack, time_since_last_sample):
        if active_profiler_context_var.get() is self:
            self.frame_records.append((call_stack, time_since_last_sample))
        else:
            # we have left the async context where this profiler was started.
            self.frame_records.append(([Profiler.OUT_OF_CONTEXT_FRAME_IDENTIFIER], time_since_last_sample))

    OUT_OF_CONTEXT_FRAME_IDENTIFIER = '<out-of-context>\x00<out-of-context>\x000'

    def print(self, file=sys.stdout, unicode=None, color=None, show_all=False, timeline=False):
        if unicode is None:
            unicode = file_supports_unicode(file)
        if color is None:
            color = file_supports_color(file)

        print(
            self.output_text(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
            ),
            file=file,
        )

    def output_text(self, unicode=False, color=False, show_all=False, timeline=False):
        return renderers.ConsoleRenderer(unicode=unicode, color=color, show_all=show_all, timeline=timeline).render(self.last_session)

    def output_html(self, timeline=False):
        return renderers.HTMLRenderer(timeline=timeline).render(self.last_session)

    def open_in_browser(self, timeline=False):
        return renderers.HTMLRenderer(timeline=timeline).open_in_browser(self.last_session)

    def output(self, renderer):
        return renderer.render(self.last_session)
