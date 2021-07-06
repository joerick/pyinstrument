import contextvars
import sys
import timeit
import types
from typing import Any, Callable, List, Optional, Type


class PythonStatProfiler:
    await_stack: List[str]

    def __init__(self, target, interval, context_var, timer_func):
        self.target = target
        self.interval = interval
        self.timer_func = timer_func or timeit.default_timer
        self.last_invocation = self.timer_func()

        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")

        self.context_var = context_var
        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def profile(self, frame: types.FrameType, event: str, arg: Any):
        now = self.timer_func()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(
                    "%s\x00%s\x00%i"
                    % (
                        frame.f_code.co_name,
                        frame.f_code.co_filename,
                        frame.f_code.co_firstlineno,
                    )
                )
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)


"""
A reimplementation of setstatprofile in Python, for prototyping/reference
purposes. Not used in normal execution.
"""


def setstatprofile(target, interval=0.001, context_var=None, timer_func=None):
    if target:
        profiler = PythonStatProfiler(
            target=target,
            interval=interval,
            context_var=context_var,
            timer_func=timer_func,
        )
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)
