from contextvars import ContextVar, Token
import sys
import threading
from time import time
import timeit
import types
import pprint
from typing import Any, Callable, List, NamedTuple, Optional, Union

from pyinstrument_cext import setstatprofile

thread_locals = threading.local()
timer = timeit.default_timer


class StackSamplerSubscriber:
    def __init__(
        self,
        target: Callable[[List[str], float, Optional[List[str]]], None],
        desired_interval: float,
        context_token: Token,
        await_call_stack: Optional[List[str]],
    ) -> None:
        self.target = target
        self.desired_interval = desired_interval
        self.context_token = context_token
        self.await_call_stack = await_call_stack


active_profiler_context_var: ContextVar[Optional[object]] = ContextVar('active_profiler_context_var', default=None)

class StackSampler:
    """ Manages setstatprofile for Profilers on a single thread """

    subscribers: List[StackSamplerSubscriber]
    current_sampling_interval: Optional[float]
    last_profile_time: float

    def __init__(self) -> None:
        self.subscribers = []
        self.current_sampling_interval = None
        self.last_profile_time = 0.0

    def subscribe(self, target, desired_interval):
        if active_profiler_context_var.get() is not None:
            raise RuntimeError(
                'There is already a profiler running. You cannot run multiple profilers in the same thread or async context.'
            )
        context_token = active_profiler_context_var.set(target)

        self.subscribers.append(
            StackSamplerSubscriber(
                target=target,
                desired_interval=desired_interval,
                context_token=context_token,
                await_call_stack=None,
            )
        )
        self._update()

    def unsubscribe(self, target):
        try:
            subscriber = next(s for s in self.subscribers if s.target == target)
        except StopIteration:
            raise ValueError('target not found in subscribers')

        active_profiler_context_var.reset(subscriber.context_token)
        self.subscribers.remove(subscriber)

        self._update()

    def _update(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(interval=min_subscribers_interval)

    def _start_sampling(self, interval):
        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = timer()
        setstatprofile(self._sample, interval, active_profiler_context_var)

    def _stop_sampling(self):
        setstatprofile(None)
        self.current_sampling_interval = None
        self.last_profile_time = 0.0

    def _sample(self, frame, event, arg):
        if event == 'context_changed':
            new, old, stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    full_stack = build_call_stack(frame, event, arg)
                    full_stack.extend(reversed(stack))
                    subscriber.await_call_stack = full_stack
                elif subscriber.target == new:
                    subscriber.await_call_stack = None
                else:
                    assert subscriber.target is not None
        else:
            # active_profiler = active_profiler_context_var.get()
            now = timer()
            time_since_last_sample = now - self.last_profile_time

            call_stack = build_call_stack(frame, event, arg)

            for subscriber in self.subscribers:
                if subscriber.await_call_stack is None:
                    subscriber.target(call_stack, time_since_last_sample, None)
                else:
                    subscriber.target(call_stack, time_since_last_sample, subscriber.await_call_stack)

            self.last_profile_time = now


def get_stack_sampler() -> StackSampler:
    """
    Gets the stack sampler for the current thread, creating it if necessary
    """
    if not hasattr(thread_locals, "stack_sampler"):
        thread_locals.stack_sampler = StackSampler()
    return thread_locals.stack_sampler


def build_call_stack(
    frame: Union[types.FrameType, None], event: str, arg: Any
) -> List[str]:
    call_stack = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back
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
        identifier = "%s\x00%s\x00%i" % (
            frame.f_code.co_name,
            frame.f_code.co_filename,
            frame.f_code.co_firstlineno,
        )
        call_stack.append(identifier)
        frame = frame.f_back

    thread = threading.current_thread()
    thread_identifier = "%s\x00%s\x00%i" % (thread.name, "<thread>", thread.ident)
    call_stack.append(thread_identifier)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack


class PythonStatProfiler:
    await_stack: List[str]

    def __init__(self, target, interval, context_var):
        self.target = target
        self.interval = interval
        self.last_invocation = timer()
        self.context_var = context_var
        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def profile(self, frame: types.FrameType, event: str, arg: Any):
        now = timer()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == 'call' else frame
                self.target(context_change_frame, 'context_changed', (context_var_value, last_context_var_value, self.await_stack))
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == 'return' and frame.f_code.co_flags & 0x80:
                self.await_stack.append("%s\x00%s\x00%i" % (
                    frame.f_code.co_name,
                    frame.f_code.co_filename,
                    frame.f_code.co_firstlineno,
                ))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)


# def setstatprofile(target, interval=0.001, context_var=None):
#     if target:
#         sys.setprofile(PythonStatProfiler(target, interval, context_var).profile)
#     else:
#         sys.setprofile(None)
