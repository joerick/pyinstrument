from __future__ import annotations

import inspect
import sys
import time
import types
from time import process_time
from typing import IO, Any

from pyinstrument import renderers
from pyinstrument.frame import AWAIT_FRAME_IDENTIFIER, OUT_OF_CONTEXT_FRAME_IDENTIFIER
from pyinstrument.session import Session
from pyinstrument.stack_sampler import AsyncState, StackSampler, build_call_stack, get_stack_sampler
from pyinstrument.typing import LiteralStr
from pyinstrument.util import file_supports_color, file_supports_unicode

# pyright: strict


class ActiveProfilerSession:
    frame_records: list[tuple[list[str], float]]

    def __init__(
        self,
        start_time: float,
        start_process_time: float,
        start_call_stack: list[str],
    ) -> None:
        self.start_time = start_time
        self.start_process_time = start_process_time
        self.start_call_stack = start_call_stack
        self.frame_records = []


AsyncMode = LiteralStr["enabled", "disabled", "strict"]


class Profiler:
    """
    The profiler - this is the main way to use pyinstrument.
    """

    _last_session: Session | None
    _active_session: ActiveProfilerSession | None
    _interval: float
    _async_mode: AsyncMode

    def __init__(self, interval: float = 0.001, async_mode: AsyncMode = "enabled"):
        """
        Note the profiling will not start until :func:`start` is called.

        :param interval: See :attr:`interval`.
        :param async_mode: See :attr:`async_mode`.
        """
        self._interval = interval
        self._last_session = None
        self._active_session = None
        self._async_mode = async_mode

    @property
    def interval(self) -> float:
        """
        The minimum time, in seconds, between each stack sample. This translates into the
        resolution of the sampling.
        """
        return self._interval

    @property
    def async_mode(self) -> AsyncMode:
        """
        Configures how this Profiler tracks time in a program that uses
        async/await.

        ``enabled``
            When this profiler sees an ``await``, time is logged in the function
            that awaited, rather than observing other coroutines or the event
            loop.

        ``disabled``
            This profiler doesn't attempt to track ``await``. In a program that
            uses async/await, this will interleave other coroutines and event
            loop machinery in the profile. Use this option if async support is
            causing issues in your use case, or if you want to run multiple
            profilers at once.

        ``strict``
            Instructs the profiler to only profile the current
            `async context <https://docs.python.org/3/library/contextvars.html>`_.
            Frames that are observed in an other context are ignored, tracked
            instead as ``<out-of-context>``.
        """
        return self._async_mode

    @property
    def last_session(self) -> Session | None:
        """
        The previous session recorded by the Profiler.
        """
        return self._last_session

    def start(self, caller_frame: types.FrameType | None = None):
        """
        Instructs the profiler to start - to begin observing the program's execution and recording
        frames.

        The normal way to invoke ``start()`` is with a new instance, but you can restart a Profiler
        that was previously running, too. The sessions are combined.

        :param caller_frame: Set this to override the default behaviour of treating the caller of
            ``start()`` as the 'start_call_stack' - the instigator of the profile. Most
            renderers will trim the 'root' from the call stack up to this frame, to
            present a simpler output.

            You might want to set this to ``inspect.currentframe().f_back`` if you are
            writing a library that wraps pyinstrument.
        """

        if caller_frame is None:
            caller_frame = inspect.currentframe().f_back  # type: ignore

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack, self.interval, use_async_context
            )
        except:
            self._active_session = None
            raise

    def stop(self) -> Session:
        """
        Stops the profiler observing, and sets :attr:`last_session`
        to the captured session.

        :return: The captured session.
        """
        if not self._active_session:
            raise RuntimeError("This profiler is not currently running.")

        try:
            get_stack_sampler().unsubscribe(self._sampler_saw_call_stack)
        except StackSampler.SubscriberNotFound:
            raise RuntimeError(
                "Failed to stop profiling. Make sure that you start/stop profiling on the same thread."
            )

        cpu_time = process_time() - self._active_session.start_process_time

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

        .. code-block:: python

            with Profiler() as p:
                # your code here...
                do_some_work()

            # profiling has ended. let's print the output.
            p.print()
        """
        self.start(caller_frame=inspect.currentframe().f_back)  # type: ignore
        return self

    def __exit__(self, *args: Any):
        self.stop()

    # pylint: disable=W0613
    def _sampler_saw_call_stack(
        self,
        call_stack: list[str],
        time_since_last_sample: float,
        async_state: AsyncState | None,
    ):
        if not self._active_session:
            raise RuntimeError(
                "Received a call stack without an active session. Please file an issue on pyinstrument Github describing how you made this happen!"
            )

        if (
            async_state
            and async_state.state == "out_of_context_awaited"
            and self._async_mode in ["enabled", "strict"]
        ):
            awaiting_coroutine_stack = async_state.info
            self._active_session.frame_records.append(
                (
                    awaiting_coroutine_stack + [AWAIT_FRAME_IDENTIFIER],
                    time_since_last_sample,
                )
            )
        elif (
            async_state
            and async_state.state == "out_of_context_unknown"
            and self._async_mode == "strict"
        ):
            context_exit_frame = async_state.info
            self._active_session.frame_records.append(
                (
                    context_exit_frame + [OUT_OF_CONTEXT_FRAME_IDENTIFIER],
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

    def output_text(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode, color=color, show_all=show_all, timeline=timeline
            )
        )

    def output_html(self, timeline: bool = False) -> str:
        """
        Return the profile output as HTML, as rendered by :class:`HTMLRenderer`
        """
        return self.output(renderer=renderers.HTMLRenderer(timeline=timeline))

    def open_in_browser(self, timeline: bool = False):
        """
        Opens the last profile session in your web browser.
        """
        session = self._get_last_session_or_fail()

        return renderers.HTMLRenderer(timeline=timeline).open_in_browser(session)

    def output(self, renderer: renderers.Renderer) -> str:
        """
        Returns the last profile session, as rendered by ``renderer``.

        :param renderer: The renderer to use.
        """
        session = self._get_last_session_or_fail()

        return renderer.render(session)

    def _get_last_session_or_fail(self) -> Session:
        if self.is_running:
            raise Exception("can't render profile output because this profiler is still running")

        if self.last_session is None:
            raise Exception(
                "can't render profile output because this profiler has not completed a profile session yet"
            )

        return self.last_session
