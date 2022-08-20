from __future__ import annotations

import threading
import timeit
import types
from contextvars import ContextVar
from typing import Any, Callable, List, NamedTuple, Optional

from pyinstrument.low_level.stat_profile import get_frame_info, setstatprofile
from pyinstrument.typing import LiteralStr

# pyright: strict


thread_locals = threading.local()

StackSamplerSubscriberTarget = Callable[[List[str], float, Optional["AsyncState"]], None]


class StackSamplerSubscriber:
    def __init__(
        self,
        *,
        target: StackSamplerSubscriberTarget,
        desired_interval: float,
        bound_to_async_context: bool,
        async_state: AsyncState | None,
    ) -> None:
        self.target = target
        self.desired_interval = desired_interval
        self.bound_to_async_context = bound_to_async_context
        self.async_state = async_state


active_profiler_context_var: ContextVar[object | None] = ContextVar(
    "active_profiler_context_var", default=None
)


class StackSampler:
    """Manages setstatprofile for Profilers on a single thread"""

    subscribers: list[StackSamplerSubscriber]
    current_sampling_interval: float | None
    last_profile_time: float
    timer_func: Callable[[], float] | None

    def __init__(self) -> None:
        self.subscribers = []
        self.current_sampling_interval = None
        self.last_profile_time = 0.0
        self.timer_func = None

    def subscribe(
        self,
        target: StackSamplerSubscriberTarget,
        desired_interval: float,
        use_async_context: bool,
    ):
        if use_async_context:
            if active_profiler_context_var.get() is not None:
                raise RuntimeError(
                    "There is already a profiler running. You cannot run multiple profilers in the same thread or async context, unless you disable async support."
                )
            active_profiler_context_var.set(target)

        self.subscribers.append(
            StackSamplerSubscriber(
                target=target,
                desired_interval=desired_interval,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def unsubscribe(self, target: StackSamplerSubscriberTarget):
        try:
            subscriber = next(s for s in self.subscribers if s.target == target)  # type: ignore
        except StopIteration:
            raise StackSampler.SubscriberNotFound()

        if subscriber.bound_to_async_context:
            # (don't need to use context_var.reset() because we verified it was
            # None before we started)
            active_profiler_context_var.set(None)

        self.subscribers.remove(subscriber)

        self._update()

    def _update(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(interval=min_subscribers_interval)

    def _start_sampling(self, interval: float):
        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()
        setstatprofile(self._sample, interval, active_profiler_context_var, self.timer_func)

    def _stop_sampling(self):
        setstatprofile(None)
        self.current_sampling_interval = None
        self.last_profile_time = 0.0

    def _sample(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(frame, event, arg)
                    if coroutine_stack:
                        full_stack.extend(reversed(coroutine_stack))
                        subscriber.async_state = AsyncState(
                            "out_of_context_awaited", info=full_stack
                        )
                    else:
                        subscriber.async_state = AsyncState(
                            "out_of_context_unknown", info=full_stack
                        )
                elif subscriber.target == new:
                    assert subscriber.bound_to_async_context
                    subscriber.async_state = AsyncState("in_context")
        else:
            now = self._timer()
            time_since_last_sample = now - self.last_profile_time

            call_stack = build_call_stack(frame, event, arg)

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def _timer(self):
        if self.timer_func:
            return self.timer_func()
        else:
            return timeit.default_timer()

    class SubscriberNotFound(Exception):
        pass


def get_stack_sampler() -> StackSampler:
    """
    Gets the stack sampler for the current thread, creating it if necessary
    """
    if not hasattr(thread_locals, "stack_sampler"):
        thread_locals.stack_sampler = StackSampler()
    return thread_locals.stack_sampler


def build_call_stack(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "c_exception":
        # if we're exiting a C function, we should add a frame before
        # any Python frames that attributes the time to that C function
        c_frame_identifier = "%s\x00%s\x00%i" % (
            getattr(arg, "__qualname__", arg.__name__),
            "<built-in>",
            0,
        )
        call_stack.append(c_frame_identifier)

    while frame is not None:
        call_stack.append(get_frame_info(frame))
        frame = frame.f_back

    thread = threading.current_thread()
    thread_identifier = "%s\x00%s\x00%i" % (thread.name, "<thread>", thread.ident)
    call_stack.append(thread_identifier)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack


class AsyncState(NamedTuple):
    state: LiteralStr["in_context", "out_of_context_awaited", "out_of_context_unknown"]
    """
    Definitions:
      ``in_context``: indicates that the sample comes from the subscriber's
      context.

      ``out_of_context_awaited``: the sample comes from outside the
      subscriber's context, but we tracked the await that happened before the
      context exited. :attr:`info` contains the call stack of the await.

      ``out_of_context_unknown``: the sample comes from outside the
      subscriber's context, but the change of context didn't look like an
      await. :attr:`info` contains the call stack when the context changed.
    """

    info: Any = None
