import inspect
import sys
import time
import timeit
from contextvars import ContextVar, Token
from typing import List, Optional, Tuple

from pyinstrument import renderers
from pyinstrument.session import ProfilerSession
from pyinstrument.stack_sampler import build_call_stack, get_stack_sampler
from pyinstrument.util import file_supports_color, file_supports_unicode

try:
    from time import process_time
except ImportError:
    process_time = lambda: None

timer = timeit.default_timer


active_profiler_context_var: ContextVar[Optional["Profiler"]] = ContextVar(
    "active_profiler_context_var", default=None
)


class ActiveProfilerSession:
    frame_records: List[Tuple[List[str], float]]

    def __init__(
        self,
        context_var_token: Token,
        start_time: float,
        start_process_time: Optional[float],
        start_call_stack: List[str],
    ) -> None:
        self.context_var_token = context_var_token
        self.start_time = start_time
        self.start_process_time = start_process_time
        self.start_call_stack = start_call_stack
        self.frame_records = []


class Profiler:
    last_session: Optional[ProfilerSession]
    _active_session: Optional[ActiveProfilerSession]

    def __init__(self, interval=0.001):
        self.interval = interval
        self.last_session = None
        self._active_session = None

    def start(self, caller_frame=None):
        if active_profiler_context_var.get() is not None:
            raise RuntimeError(
                "A profiler is already running. Running multiple profilers on the same thead is "
                "not supported, unless they're in different async contexts."
            )

        if caller_frame is None:
            caller_frame = inspect.currentframe().f_back

        self._active_session = ActiveProfilerSession(
            start_time=time.time(),
            context_var_token=active_profiler_context_var.set(self),
            start_process_time=process_time(),
            start_call_stack=build_call_stack(caller_frame, "initial", None),
        )

        get_stack_sampler().subscribe(self._sampler_saw_call_stack, self.interval)

    def stop(self):
        if not self._active_session:
            raise RuntimeError("This profiler is not currently running.")

        get_stack_sampler().unsubscribe(self._sampler_saw_call_stack)
        active_profiler_context_var.reset(self._active_session.context_var_token)

        if self._active_session.start_process_time:
            cpu_time = process_time() - self._active_session.start_process_time
        else:
            cpu_time = None

        session = ProfilerSession(
            frame_records=self._active_session.frame_records,
            start_time=self._active_session.start_time,
            duration=time.time() - self._active_session.start_time,
            sample_count=len(self._active_session.frame_records),
            program=" ".join(sys.argv),
            start_call_stack=self._active_session.start_call_stack,
            cpu_time=cpu_time,
        )
        self._active_session = None

        if self.last_session is not None:
            # include the previous session's data too
            session = ProfilerSession.combine(self.last_session, session)

        self.last_session = session

        return session

    @property
    def is_running(self):
        return self._active_session is not None

    def reset(self):
        if self.is_running:
            self.stop()

        self.last_session = None

    def __enter__(self):
        self.start(caller_frame=inspect.currentframe().f_back)
        return self

    def __exit__(self, *args):
        self.stop()

    # pylint: disable=W0613
    def _sampler_saw_call_stack(self, call_stack, time_since_last_sample, awaiting_coroutine_stack):
        if not self._active_session:
            raise RuntimeError("Received a call stack without an active session")

        if awaiting_coroutine_stack is not None:
            # we are in an 'await' - we have left the profiler's context
            self._active_session.frame_records.append(
                (
                    awaiting_coroutine_stack + [Profiler.AWAIT_FRAME_IDENTIFIER],
                    time_since_last_sample,
                )
            )
        else:
            # regular sync code
            self._active_session.frame_records.append((call_stack, time_since_last_sample))

    OUT_OF_CONTEXT_FRAME_IDENTIFIER = "[out-of-context]\x00<out-of-context>\x000"
    AWAIT_FRAME_IDENTIFIER = "[await]\x00<await>\x000"

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
        return renderers.ConsoleRenderer(
            unicode=unicode, color=color, show_all=show_all, timeline=timeline
        ).render(self.last_session)

    def output_html(self, timeline=False):
        return renderers.HTMLRenderer(timeline=timeline).render(self.last_session)

    def open_in_browser(self, timeline=False):
        return renderers.HTMLRenderer(timeline=timeline).open_in_browser(self.last_session)

    def output(self, renderer):
        return renderer.render(self.last_session)
