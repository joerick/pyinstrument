from __future__ import annotations

import contextvars
import sys
import timeit
import types
from typing import Any, Callable, List, Optional, Type

from pyinstrument.low_level.pyi_timing_thread_python import (
    pyi_timing_thread_get_time,
    pyi_timing_thread_subscribe,
    pyi_timing_thread_unsubscribe,
)
from pyinstrument.low_level.types import TimerType
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class PythonStatProfiler:
    await_stack: list[str]
    timing_thread_subscription: int | None = None

    def xǁPythonStatProfilerǁ__init____mutmut_orig(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_1(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = None
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_2(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = None
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_3(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_4(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError(None)
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_5(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("XXnot a context varXX")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_6(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("NOT A CONTEXT VAR")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_7(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = None

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_8(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = None

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_9(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type != "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_10(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "XXwalltimeXX":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_11(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "WALLTIME":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_12(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = None
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_13(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type != "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_14(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "XXwalltime_threadXX":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_15(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "WALLTIME_THREAD":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_16(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = None
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_17(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = None
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_18(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(None)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_19(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type != "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_20(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "XXtimer_funcXX":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_21(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "TIMER_FUNC":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_22(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is not None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_23(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError(None)
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_24(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("XXtimer_func must be provided for timer_func timer_typeXX")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_25(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("TIMER_FUNC MUST BE PROVIDED FOR TIMER_FUNC TIMER_TYPE")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_26(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = None
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_27(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(None)

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_28(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = None

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_29(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = None
        self.await_stack = []

    def xǁPythonStatProfilerǁ__init____mutmut_30(
        self,
        target: Callable[[types.FrameType, str, Any], Any],
        interval: float,
        context_var: contextvars.ContextVar[object | None] | None,
        timer_type: TimerType,
        timer_func: Callable[[], float] | None,
    ):
        self.target = target
        self.interval = interval
        if context_var:
            # raise typeerror to match the C version
            if not isinstance(context_var, contextvars.ContextVar):
                raise TypeError("not a context var")
        self.context_var = context_var

        self.timer_type = timer_type

        if timer_type == "walltime":
            self.get_time = timeit.default_timer
        elif timer_type == "walltime_thread":
            self.get_time = pyi_timing_thread_get_time
            self.timing_thread_subscription = pyi_timing_thread_subscribe(interval)
        elif timer_type == "timer_func":
            if timer_func is None:
                raise TypeError("timer_func must be provided for timer_func timer_type")
            self.get_time = timer_func
        else:
            raise ValueError(f"invalid timer_type '{timer_type}'")

        self.last_invocation = self.get_time()

        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = None
    
    xǁPythonStatProfilerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPythonStatProfilerǁ__init____mutmut_1': xǁPythonStatProfilerǁ__init____mutmut_1, 
        'xǁPythonStatProfilerǁ__init____mutmut_2': xǁPythonStatProfilerǁ__init____mutmut_2, 
        'xǁPythonStatProfilerǁ__init____mutmut_3': xǁPythonStatProfilerǁ__init____mutmut_3, 
        'xǁPythonStatProfilerǁ__init____mutmut_4': xǁPythonStatProfilerǁ__init____mutmut_4, 
        'xǁPythonStatProfilerǁ__init____mutmut_5': xǁPythonStatProfilerǁ__init____mutmut_5, 
        'xǁPythonStatProfilerǁ__init____mutmut_6': xǁPythonStatProfilerǁ__init____mutmut_6, 
        'xǁPythonStatProfilerǁ__init____mutmut_7': xǁPythonStatProfilerǁ__init____mutmut_7, 
        'xǁPythonStatProfilerǁ__init____mutmut_8': xǁPythonStatProfilerǁ__init____mutmut_8, 
        'xǁPythonStatProfilerǁ__init____mutmut_9': xǁPythonStatProfilerǁ__init____mutmut_9, 
        'xǁPythonStatProfilerǁ__init____mutmut_10': xǁPythonStatProfilerǁ__init____mutmut_10, 
        'xǁPythonStatProfilerǁ__init____mutmut_11': xǁPythonStatProfilerǁ__init____mutmut_11, 
        'xǁPythonStatProfilerǁ__init____mutmut_12': xǁPythonStatProfilerǁ__init____mutmut_12, 
        'xǁPythonStatProfilerǁ__init____mutmut_13': xǁPythonStatProfilerǁ__init____mutmut_13, 
        'xǁPythonStatProfilerǁ__init____mutmut_14': xǁPythonStatProfilerǁ__init____mutmut_14, 
        'xǁPythonStatProfilerǁ__init____mutmut_15': xǁPythonStatProfilerǁ__init____mutmut_15, 
        'xǁPythonStatProfilerǁ__init____mutmut_16': xǁPythonStatProfilerǁ__init____mutmut_16, 
        'xǁPythonStatProfilerǁ__init____mutmut_17': xǁPythonStatProfilerǁ__init____mutmut_17, 
        'xǁPythonStatProfilerǁ__init____mutmut_18': xǁPythonStatProfilerǁ__init____mutmut_18, 
        'xǁPythonStatProfilerǁ__init____mutmut_19': xǁPythonStatProfilerǁ__init____mutmut_19, 
        'xǁPythonStatProfilerǁ__init____mutmut_20': xǁPythonStatProfilerǁ__init____mutmut_20, 
        'xǁPythonStatProfilerǁ__init____mutmut_21': xǁPythonStatProfilerǁ__init____mutmut_21, 
        'xǁPythonStatProfilerǁ__init____mutmut_22': xǁPythonStatProfilerǁ__init____mutmut_22, 
        'xǁPythonStatProfilerǁ__init____mutmut_23': xǁPythonStatProfilerǁ__init____mutmut_23, 
        'xǁPythonStatProfilerǁ__init____mutmut_24': xǁPythonStatProfilerǁ__init____mutmut_24, 
        'xǁPythonStatProfilerǁ__init____mutmut_25': xǁPythonStatProfilerǁ__init____mutmut_25, 
        'xǁPythonStatProfilerǁ__init____mutmut_26': xǁPythonStatProfilerǁ__init____mutmut_26, 
        'xǁPythonStatProfilerǁ__init____mutmut_27': xǁPythonStatProfilerǁ__init____mutmut_27, 
        'xǁPythonStatProfilerǁ__init____mutmut_28': xǁPythonStatProfilerǁ__init____mutmut_28, 
        'xǁPythonStatProfilerǁ__init____mutmut_29': xǁPythonStatProfilerǁ__init____mutmut_29, 
        'xǁPythonStatProfilerǁ__init____mutmut_30': xǁPythonStatProfilerǁ__init____mutmut_30
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPythonStatProfilerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁPythonStatProfilerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁPythonStatProfilerǁ__init____mutmut_orig)
    xǁPythonStatProfilerǁ__init____mutmut_orig.__name__ = 'xǁPythonStatProfilerǁ__init__'

    def xǁPythonStatProfilerǁ__del____mutmut_orig(self):
        if self.timing_thread_subscription is not None:
            pyi_timing_thread_unsubscribe(self.timing_thread_subscription)

    def xǁPythonStatProfilerǁ__del____mutmut_1(self):
        if self.timing_thread_subscription is None:
            pyi_timing_thread_unsubscribe(self.timing_thread_subscription)

    def xǁPythonStatProfilerǁ__del____mutmut_2(self):
        if self.timing_thread_subscription is not None:
            pyi_timing_thread_unsubscribe(None)
    
    xǁPythonStatProfilerǁ__del____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPythonStatProfilerǁ__del____mutmut_1': xǁPythonStatProfilerǁ__del____mutmut_1, 
        'xǁPythonStatProfilerǁ__del____mutmut_2': xǁPythonStatProfilerǁ__del____mutmut_2
    }
    
    def __del__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPythonStatProfilerǁ__del____mutmut_orig"), object.__getattribute__(self, "xǁPythonStatProfilerǁ__del____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __del__.__signature__ = _mutmut_signature(xǁPythonStatProfilerǁ__del____mutmut_orig)
    xǁPythonStatProfilerǁ__del____mutmut_orig.__name__ = 'xǁPythonStatProfilerǁ__del__'

    def xǁPythonStatProfilerǁprofile__mutmut_orig(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_1(self, frame: types.FrameType, event: str, arg: Any):
        now = None

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_2(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = None
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_3(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = None

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_4(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_5(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = None
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_6(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event != "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_7(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "XXcallXX" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_8(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "CALL" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_9(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_10(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    None,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_11(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    None,
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_12(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    None,
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_13(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_14(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_15(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_16(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "XXcontext_changedXX",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_17(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "CONTEXT_CHANGED",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_18(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = None

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_19(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" or frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_20(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event != "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_21(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "XXreturnXX" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_22(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "RETURN" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_23(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags | 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_24(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 129:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_25(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(None)
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_26(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(None))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_27(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now <= self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_28(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation - self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_29(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = None
        return self.target(frame, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_30(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(None, event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_31(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, None, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_32(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, None)

    def xǁPythonStatProfilerǁprofile__mutmut_33(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(event, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_34(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, arg)

    def xǁPythonStatProfilerǁprofile__mutmut_35(self, frame: types.FrameType, event: str, arg: Any):
        now = self.get_time()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == "call" else frame
                assert context_change_frame is not None
                self.target(
                    context_change_frame,
                    "context_changed",
                    (context_var_value, last_context_var_value, self.await_stack),
                )
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == "return" and frame.f_code.co_flags & 0x80:
                self.await_stack.append(get_frame_info(frame))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, )
    
    xǁPythonStatProfilerǁprofile__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPythonStatProfilerǁprofile__mutmut_1': xǁPythonStatProfilerǁprofile__mutmut_1, 
        'xǁPythonStatProfilerǁprofile__mutmut_2': xǁPythonStatProfilerǁprofile__mutmut_2, 
        'xǁPythonStatProfilerǁprofile__mutmut_3': xǁPythonStatProfilerǁprofile__mutmut_3, 
        'xǁPythonStatProfilerǁprofile__mutmut_4': xǁPythonStatProfilerǁprofile__mutmut_4, 
        'xǁPythonStatProfilerǁprofile__mutmut_5': xǁPythonStatProfilerǁprofile__mutmut_5, 
        'xǁPythonStatProfilerǁprofile__mutmut_6': xǁPythonStatProfilerǁprofile__mutmut_6, 
        'xǁPythonStatProfilerǁprofile__mutmut_7': xǁPythonStatProfilerǁprofile__mutmut_7, 
        'xǁPythonStatProfilerǁprofile__mutmut_8': xǁPythonStatProfilerǁprofile__mutmut_8, 
        'xǁPythonStatProfilerǁprofile__mutmut_9': xǁPythonStatProfilerǁprofile__mutmut_9, 
        'xǁPythonStatProfilerǁprofile__mutmut_10': xǁPythonStatProfilerǁprofile__mutmut_10, 
        'xǁPythonStatProfilerǁprofile__mutmut_11': xǁPythonStatProfilerǁprofile__mutmut_11, 
        'xǁPythonStatProfilerǁprofile__mutmut_12': xǁPythonStatProfilerǁprofile__mutmut_12, 
        'xǁPythonStatProfilerǁprofile__mutmut_13': xǁPythonStatProfilerǁprofile__mutmut_13, 
        'xǁPythonStatProfilerǁprofile__mutmut_14': xǁPythonStatProfilerǁprofile__mutmut_14, 
        'xǁPythonStatProfilerǁprofile__mutmut_15': xǁPythonStatProfilerǁprofile__mutmut_15, 
        'xǁPythonStatProfilerǁprofile__mutmut_16': xǁPythonStatProfilerǁprofile__mutmut_16, 
        'xǁPythonStatProfilerǁprofile__mutmut_17': xǁPythonStatProfilerǁprofile__mutmut_17, 
        'xǁPythonStatProfilerǁprofile__mutmut_18': xǁPythonStatProfilerǁprofile__mutmut_18, 
        'xǁPythonStatProfilerǁprofile__mutmut_19': xǁPythonStatProfilerǁprofile__mutmut_19, 
        'xǁPythonStatProfilerǁprofile__mutmut_20': xǁPythonStatProfilerǁprofile__mutmut_20, 
        'xǁPythonStatProfilerǁprofile__mutmut_21': xǁPythonStatProfilerǁprofile__mutmut_21, 
        'xǁPythonStatProfilerǁprofile__mutmut_22': xǁPythonStatProfilerǁprofile__mutmut_22, 
        'xǁPythonStatProfilerǁprofile__mutmut_23': xǁPythonStatProfilerǁprofile__mutmut_23, 
        'xǁPythonStatProfilerǁprofile__mutmut_24': xǁPythonStatProfilerǁprofile__mutmut_24, 
        'xǁPythonStatProfilerǁprofile__mutmut_25': xǁPythonStatProfilerǁprofile__mutmut_25, 
        'xǁPythonStatProfilerǁprofile__mutmut_26': xǁPythonStatProfilerǁprofile__mutmut_26, 
        'xǁPythonStatProfilerǁprofile__mutmut_27': xǁPythonStatProfilerǁprofile__mutmut_27, 
        'xǁPythonStatProfilerǁprofile__mutmut_28': xǁPythonStatProfilerǁprofile__mutmut_28, 
        'xǁPythonStatProfilerǁprofile__mutmut_29': xǁPythonStatProfilerǁprofile__mutmut_29, 
        'xǁPythonStatProfilerǁprofile__mutmut_30': xǁPythonStatProfilerǁprofile__mutmut_30, 
        'xǁPythonStatProfilerǁprofile__mutmut_31': xǁPythonStatProfilerǁprofile__mutmut_31, 
        'xǁPythonStatProfilerǁprofile__mutmut_32': xǁPythonStatProfilerǁprofile__mutmut_32, 
        'xǁPythonStatProfilerǁprofile__mutmut_33': xǁPythonStatProfilerǁprofile__mutmut_33, 
        'xǁPythonStatProfilerǁprofile__mutmut_34': xǁPythonStatProfilerǁprofile__mutmut_34, 
        'xǁPythonStatProfilerǁprofile__mutmut_35': xǁPythonStatProfilerǁprofile__mutmut_35
    }
    
    def profile(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPythonStatProfilerǁprofile__mutmut_orig"), object.__getattribute__(self, "xǁPythonStatProfilerǁprofile__mutmut_mutants"), args, kwargs, self)
        return result 
    
    profile.__signature__ = _mutmut_signature(xǁPythonStatProfilerǁprofile__mutmut_orig)
    xǁPythonStatProfilerǁprofile__mutmut_orig.__name__ = 'xǁPythonStatProfilerǁprofile'


"""
A reimplementation of setstatprofile in Python, for prototyping/reference
purposes. Not used in normal execution.
"""


def x_setstatprofile__mutmut_orig(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "walltime",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = PythonStatProfiler(
            target=target,
            interval=interval,
            context_var=context_var,
            timer_type=timer_type,
            timer_func=timer_func,
        )
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)


def x_setstatprofile__mutmut_1(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 1.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "walltime",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = PythonStatProfiler(
            target=target,
            interval=interval,
            context_var=context_var,
            timer_type=timer_type,
            timer_func=timer_func,
        )
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)


def x_setstatprofile__mutmut_2(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "XXwalltimeXX",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = PythonStatProfiler(
            target=target,
            interval=interval,
            context_var=context_var,
            timer_type=timer_type,
            timer_func=timer_func,
        )
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)


def x_setstatprofile__mutmut_3(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "WALLTIME",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = PythonStatProfiler(
            target=target,
            interval=interval,
            context_var=context_var,
            timer_type=timer_type,
            timer_func=timer_func,
        )
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)


def x_setstatprofile__mutmut_4(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "walltime",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = None
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)


def x_setstatprofile__mutmut_5(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "walltime",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = PythonStatProfiler(
            target=None,
            interval=interval,
            context_var=context_var,
            timer_type=timer_type,
            timer_func=timer_func,
        )
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)


def x_setstatprofile__mutmut_6(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "walltime",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = PythonStatProfiler(
            target=target,
            interval=None,
            context_var=context_var,
            timer_type=timer_type,
            timer_func=timer_func,
        )
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)


def x_setstatprofile__mutmut_7(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "walltime",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = PythonStatProfiler(
            target=target,
            interval=interval,
            context_var=None,
            timer_type=timer_type,
            timer_func=timer_func,
        )
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)


def x_setstatprofile__mutmut_8(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "walltime",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = PythonStatProfiler(
            target=target,
            interval=interval,
            context_var=context_var,
            timer_type=None,
            timer_func=timer_func,
        )
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)


def x_setstatprofile__mutmut_9(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "walltime",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = PythonStatProfiler(
            target=target,
            interval=interval,
            context_var=context_var,
            timer_type=timer_type,
            timer_func=None,
        )
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)


def x_setstatprofile__mutmut_10(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "walltime",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = PythonStatProfiler(
            interval=interval,
            context_var=context_var,
            timer_type=timer_type,
            timer_func=timer_func,
        )
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)


def x_setstatprofile__mutmut_11(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "walltime",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = PythonStatProfiler(
            target=target,
            context_var=context_var,
            timer_type=timer_type,
            timer_func=timer_func,
        )
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)


def x_setstatprofile__mutmut_12(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "walltime",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = PythonStatProfiler(
            target=target,
            interval=interval,
            timer_type=timer_type,
            timer_func=timer_func,
        )
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)


def x_setstatprofile__mutmut_13(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "walltime",
    timer_func: Callable[[], float] | None = None,
) -> None:
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


def x_setstatprofile__mutmut_14(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "walltime",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = PythonStatProfiler(
            target=target,
            interval=interval,
            context_var=context_var,
            timer_type=timer_type,
            )
        sys.setprofile(profiler.profile)
    else:
        sys.setprofile(None)


def x_setstatprofile__mutmut_15(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: TimerType = "walltime",
    timer_func: Callable[[], float] | None = None,
) -> None:
    if target:
        profiler = PythonStatProfiler(
            target=target,
            interval=interval,
            context_var=context_var,
            timer_type=timer_type,
            timer_func=timer_func,
        )
        sys.setprofile(None)
    else:
        sys.setprofile(None)

x_setstatprofile__mutmut_mutants : ClassVar[MutantDict] = {
'x_setstatprofile__mutmut_1': x_setstatprofile__mutmut_1, 
    'x_setstatprofile__mutmut_2': x_setstatprofile__mutmut_2, 
    'x_setstatprofile__mutmut_3': x_setstatprofile__mutmut_3, 
    'x_setstatprofile__mutmut_4': x_setstatprofile__mutmut_4, 
    'x_setstatprofile__mutmut_5': x_setstatprofile__mutmut_5, 
    'x_setstatprofile__mutmut_6': x_setstatprofile__mutmut_6, 
    'x_setstatprofile__mutmut_7': x_setstatprofile__mutmut_7, 
    'x_setstatprofile__mutmut_8': x_setstatprofile__mutmut_8, 
    'x_setstatprofile__mutmut_9': x_setstatprofile__mutmut_9, 
    'x_setstatprofile__mutmut_10': x_setstatprofile__mutmut_10, 
    'x_setstatprofile__mutmut_11': x_setstatprofile__mutmut_11, 
    'x_setstatprofile__mutmut_12': x_setstatprofile__mutmut_12, 
    'x_setstatprofile__mutmut_13': x_setstatprofile__mutmut_13, 
    'x_setstatprofile__mutmut_14': x_setstatprofile__mutmut_14, 
    'x_setstatprofile__mutmut_15': x_setstatprofile__mutmut_15
}

def setstatprofile(*args, **kwargs):
    result = _mutmut_trampoline(x_setstatprofile__mutmut_orig, x_setstatprofile__mutmut_mutants, args, kwargs)
    return result 

setstatprofile.__signature__ = _mutmut_signature(x_setstatprofile__mutmut_orig)
x_setstatprofile__mutmut_orig.__name__ = 'x_setstatprofile'


def x_get_frame_info__mutmut_orig(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_1(frame: types.FrameType) -> str:
    frame_info = None

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_2(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" / (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_3(frame: types.FrameType) -> str:
    frame_info = "XX%s\x00%s\x00%iXX" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_4(frame: types.FrameType) -> str:
    frame_info = "%S\x00%S\x00%I" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_5(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = ""
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_6(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = None
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_7(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get(None, None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_8(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get(None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_9(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", )
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_10(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("XXselfXX", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_11(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("SELF", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_12(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") or hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_13(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self or hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_14(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(None, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_15(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, None) and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_16(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr("__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_17(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, ) and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_18(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "XX__class__XX") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_19(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__CLASS__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_20(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(None, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_21(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, None):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_22(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr("__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_23(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, ):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_24(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "XX__qualname__XX"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_25(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__QUALNAME__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_26(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = None
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_27(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = None
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_28(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get(None, None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_29(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get(None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_30(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", )
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_31(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("XXclsXX", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_32(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("CLS", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_33(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls or hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_34(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(None, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_35(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, None):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_36(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr("__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_37(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, ):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_38(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "XX__qualname__XX"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_39(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__QUALNAME__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_40(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = None

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_41(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = None

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_42(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "XX__tracebackhide__XX" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_43(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__TRACEBACKHIDE__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_44(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" not in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_45(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info = "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_46(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info -= "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_47(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" / class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_48(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "XX\x01c%sXX" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_49(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01C%S" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_50(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_51(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info = "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_52(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info -= "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_53(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" / frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_54(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "XX\x01l%iXX" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_55(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01L%I" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_56(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info = "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_57(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info -= "\x01h%i" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_58(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01h%i" / frame_hidden

    return frame_info


def x_get_frame_info__mutmut_59(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "XX\x01h%iXX" % frame_hidden

    return frame_info


def x_get_frame_info__mutmut_60(frame: types.FrameType) -> str:
    frame_info = "%s\x00%s\x00%i" % (
        frame.f_code.co_name,
        frame.f_code.co_filename,
        frame.f_code.co_firstlineno,
    )

    class_name = None
    # try to find self argument for methods
    self = frame.f_locals.get("self", None)
    if self and hasattr(self, "__class__") and hasattr(self.__class__, "__qualname__"):
        class_name = self.__class__.__qualname__
    else:
        # also try to find cls argument for class methods
        cls = frame.f_locals.get("cls", None)
        if cls and hasattr(cls, "__qualname__"):
            class_name = cls.__qualname__

    frame_hidden = "__tracebackhide__" in frame.f_locals

    if class_name:
        frame_info += "\x01c%s" % class_name

    if frame.f_lineno is not None:
        frame_info += "\x01l%i" % frame.f_lineno

    if frame_hidden:
        frame_info += "\x01H%I" % frame_hidden

    return frame_info

x_get_frame_info__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_frame_info__mutmut_1': x_get_frame_info__mutmut_1, 
    'x_get_frame_info__mutmut_2': x_get_frame_info__mutmut_2, 
    'x_get_frame_info__mutmut_3': x_get_frame_info__mutmut_3, 
    'x_get_frame_info__mutmut_4': x_get_frame_info__mutmut_4, 
    'x_get_frame_info__mutmut_5': x_get_frame_info__mutmut_5, 
    'x_get_frame_info__mutmut_6': x_get_frame_info__mutmut_6, 
    'x_get_frame_info__mutmut_7': x_get_frame_info__mutmut_7, 
    'x_get_frame_info__mutmut_8': x_get_frame_info__mutmut_8, 
    'x_get_frame_info__mutmut_9': x_get_frame_info__mutmut_9, 
    'x_get_frame_info__mutmut_10': x_get_frame_info__mutmut_10, 
    'x_get_frame_info__mutmut_11': x_get_frame_info__mutmut_11, 
    'x_get_frame_info__mutmut_12': x_get_frame_info__mutmut_12, 
    'x_get_frame_info__mutmut_13': x_get_frame_info__mutmut_13, 
    'x_get_frame_info__mutmut_14': x_get_frame_info__mutmut_14, 
    'x_get_frame_info__mutmut_15': x_get_frame_info__mutmut_15, 
    'x_get_frame_info__mutmut_16': x_get_frame_info__mutmut_16, 
    'x_get_frame_info__mutmut_17': x_get_frame_info__mutmut_17, 
    'x_get_frame_info__mutmut_18': x_get_frame_info__mutmut_18, 
    'x_get_frame_info__mutmut_19': x_get_frame_info__mutmut_19, 
    'x_get_frame_info__mutmut_20': x_get_frame_info__mutmut_20, 
    'x_get_frame_info__mutmut_21': x_get_frame_info__mutmut_21, 
    'x_get_frame_info__mutmut_22': x_get_frame_info__mutmut_22, 
    'x_get_frame_info__mutmut_23': x_get_frame_info__mutmut_23, 
    'x_get_frame_info__mutmut_24': x_get_frame_info__mutmut_24, 
    'x_get_frame_info__mutmut_25': x_get_frame_info__mutmut_25, 
    'x_get_frame_info__mutmut_26': x_get_frame_info__mutmut_26, 
    'x_get_frame_info__mutmut_27': x_get_frame_info__mutmut_27, 
    'x_get_frame_info__mutmut_28': x_get_frame_info__mutmut_28, 
    'x_get_frame_info__mutmut_29': x_get_frame_info__mutmut_29, 
    'x_get_frame_info__mutmut_30': x_get_frame_info__mutmut_30, 
    'x_get_frame_info__mutmut_31': x_get_frame_info__mutmut_31, 
    'x_get_frame_info__mutmut_32': x_get_frame_info__mutmut_32, 
    'x_get_frame_info__mutmut_33': x_get_frame_info__mutmut_33, 
    'x_get_frame_info__mutmut_34': x_get_frame_info__mutmut_34, 
    'x_get_frame_info__mutmut_35': x_get_frame_info__mutmut_35, 
    'x_get_frame_info__mutmut_36': x_get_frame_info__mutmut_36, 
    'x_get_frame_info__mutmut_37': x_get_frame_info__mutmut_37, 
    'x_get_frame_info__mutmut_38': x_get_frame_info__mutmut_38, 
    'x_get_frame_info__mutmut_39': x_get_frame_info__mutmut_39, 
    'x_get_frame_info__mutmut_40': x_get_frame_info__mutmut_40, 
    'x_get_frame_info__mutmut_41': x_get_frame_info__mutmut_41, 
    'x_get_frame_info__mutmut_42': x_get_frame_info__mutmut_42, 
    'x_get_frame_info__mutmut_43': x_get_frame_info__mutmut_43, 
    'x_get_frame_info__mutmut_44': x_get_frame_info__mutmut_44, 
    'x_get_frame_info__mutmut_45': x_get_frame_info__mutmut_45, 
    'x_get_frame_info__mutmut_46': x_get_frame_info__mutmut_46, 
    'x_get_frame_info__mutmut_47': x_get_frame_info__mutmut_47, 
    'x_get_frame_info__mutmut_48': x_get_frame_info__mutmut_48, 
    'x_get_frame_info__mutmut_49': x_get_frame_info__mutmut_49, 
    'x_get_frame_info__mutmut_50': x_get_frame_info__mutmut_50, 
    'x_get_frame_info__mutmut_51': x_get_frame_info__mutmut_51, 
    'x_get_frame_info__mutmut_52': x_get_frame_info__mutmut_52, 
    'x_get_frame_info__mutmut_53': x_get_frame_info__mutmut_53, 
    'x_get_frame_info__mutmut_54': x_get_frame_info__mutmut_54, 
    'x_get_frame_info__mutmut_55': x_get_frame_info__mutmut_55, 
    'x_get_frame_info__mutmut_56': x_get_frame_info__mutmut_56, 
    'x_get_frame_info__mutmut_57': x_get_frame_info__mutmut_57, 
    'x_get_frame_info__mutmut_58': x_get_frame_info__mutmut_58, 
    'x_get_frame_info__mutmut_59': x_get_frame_info__mutmut_59, 
    'x_get_frame_info__mutmut_60': x_get_frame_info__mutmut_60
}

def get_frame_info(*args, **kwargs):
    result = _mutmut_trampoline(x_get_frame_info__mutmut_orig, x_get_frame_info__mutmut_mutants, args, kwargs)
    return result 

get_frame_info.__signature__ = _mutmut_signature(x_get_frame_info__mutmut_orig)
x_get_frame_info__mutmut_orig.__name__ = 'x_get_frame_info'
