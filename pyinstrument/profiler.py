from __future__ import annotations

import inspect
import sys
import time
import timeit
import types
from contextvars import ContextVar, Token
from time import process_time
from typing import IO, List, Optional, Tuple

from pyinstrument import renderers
from pyinstrument.frame import AWAIT_FRAME_IDENTIFIER
from pyinstrument.session import Session
from pyinstrument.stack_sampler import build_call_stack, get_stack_sampler
from pyinstrument.util import file_supports_color, file_supports_unicode

timer = timeit.default_timer


active_profiler_context_var: ContextVar[Profiler | None] = ContextVar(
    "active_profiler_context_var", default=None
)


class ActiveProfilerSession:
    frame_records: list[tuple[list[str], float]]

    def __init__(
        self,
        context_var_token: Token,
        start_time: float,
        start_process_time: float | None,
        start_call_stack: list[str],
    ) -> None:
        self.context_var_token = context_var_token
        self.start_time = start_time
        self.start_process_time = start_process_time
        self.start_call_stack = start_call_stack
        self.frame_records = []


class Profiler:
    """
    The profiler - this is the main way to use pyinstrument.
    """

    _last_session: Session | None
    _active_session: ActiveProfilerSession | None
    _interval: float

    def __init__(self, interval: float = 0.001):
        """
        Create the profiler.

        Note the profiling will not start until :func:`start` is called.

        Arguments:
            interval: See :attr:`interval` for details.
        """
        self._interval = interval
        self._last_session = None
        self._active_session = None

    @property
    def interval(self):
        """
        The minimum time, in seconds, between each stack sample. This translates into the
        resolution of the sampling.
        """
        return self._interval

    @property
    def last_session(self) -> Session | None:
        """
        The previous session recorded by the Profiler.
        """
        return self._last_session

    def start(self, caller_frame: types.FrameType = None):
        """
        Instructs the profiler to start - to begin observing the program's execution and recording
        frames.

        The normal way to invoke ``start()`` is with a new instance, but you can restart a Profiler
        that was previously running, too. The sessions are combined.

        :param types.FrameType caller_frame: Set this to override the default behaviour of treating the caller of
            ``start()`` as the 'start_call_stack' - the instigator of the profile. Most
            renderers will trim the 'root' from the call stack up to this frame, to
            present a simpler output.

            You might want to set this to ``inspect.currentframe().f_back`` if you are
            writing a library that wraps pyinstrument.
        """
        if active_profiler_context_var.get() is not None:
            raise RuntimeError(
                "A profiler is already running. Running multiple profilers on the same thead is "
                "not supported, unless they're in different async contexts."
            )

        if caller_frame is None:
            caller_frame = inspect.currentframe().f_back  # type: ignore

        self._active_session = ActiveProfilerSession(
            start_time=time.time(),
            context_var_token=active_profiler_context_var.set(self),
            start_process_time=process_time(),
            start_call_stack=build_call_stack(caller_frame, "initial", None),
        )

        get_stack_sampler().subscribe(self._sampler_saw_call_stack, self.interval)

    def stop(self) -> Session:
        """
        Stops the profiler observing, and sets :attr:`last_session`
        to the captured session.

        Returns The captured session.
        """
        if not self._active_session:
            raise RuntimeError("This profiler is not currently running.")

        get_stack_sampler().unsubscribe(self._sampler_saw_call_stack)
        active_profiler_context_var.reset(self._active_session.context_var_token)

        if self._active_session.start_process_time:
            cpu_time = process_time() - self._active_session.start_process_time
        else:
            cpu_time = None

        session = Session(
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
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    @property
    def is_running(self):
        """
        Returns `True` if this profiler is running - i.e. observing the program execution.
        """
        return self._active_session is not None

    def reset(self):
        """
        Resets the Profiler, clearing the `last_session`.
        """
        if self.is_running:
            self.stop()

        self._last_session = None

    def __enter__(self):
        """
        Context manager support.

        Profilers can be used in `with` blocks! See this example:

        ```
        with Profiler() as p:
            # your code here...
            do_some_work()

        # profiling has ended. let's print the output.
        p.print()
        ```
        """
        self.start(caller_frame=inspect.currentframe().f_back)  # type: ignore
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
                    awaiting_coroutine_stack + [AWAIT_FRAME_IDENTIFIER],
                    time_since_last_sample,
                )
            )
        else:
            # regular sync code
            self._active_session.frame_records.append((call_stack, time_since_last_sample))

    def print(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False)

        Print the captured profile to the console.

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.
        :param unicode: Override unicode support detection.
        :param color: Override ANSI color support detection.
        :param show_all: Sets the ``show_all`` parameter on the renderer.
        :param timeline: Sets the ``timeline`` parameter on the renderer.
        """
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

    def output_text(self, unicode=False, color=False, show_all=False, timeline=False) -> str:
        """
        Return the profile output as text, as rendered by [ConsoleRenderer][pyinstrument.renderers.ConsoleRenderer]
        """
        return renderers.ConsoleRenderer(
            unicode=unicode, color=color, show_all=show_all, timeline=timeline
        ).render(self.last_session)

    def output_html(self, timeline=False) -> str:
        """
        Return the profile output as HTML, as rendered by [HTMLRenderer][pyinstrument.renderers.HTMLRenderer]
        """
        return renderers.HTMLRenderer(timeline=timeline).render(self.last_session)

    def open_in_browser(self, timeline=False):
        """
        Opens the last profile session in your web browser.
        """
        return renderers.HTMLRenderer(timeline=timeline).open_in_browser(self.last_session)

    def output(self, renderer) -> str:
        """
        Returns the last profile session, as rendered by `renderer`

        Arguments:
            renderer: The renderer to use.
        """
        return renderer.render(self.last_session)
