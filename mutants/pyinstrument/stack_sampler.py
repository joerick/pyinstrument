from __future__ import annotations

import os
import sys
import textwrap
import threading
import timeit
import types
from contextvars import ContextVar
from typing import Any, Callable, List, NamedTuple, Optional

from pyinstrument.low_level.stat_profile import (
    get_frame_info,
    measure_timing_overhead,
    setstatprofile,
    walltime_coarse_resolution,
)
from pyinstrument.low_level.types import TimerType
from pyinstrument.typing import LiteralStr
from pyinstrument.util import format_float_with_sig_figs, strtobool, unwrap

# pyright: strict


thread_locals = threading.local()

StackSamplerSubscriberTarget = Callable[[List[str], float, Optional["AsyncState"]], None]

IGNORE_OVERHEAD_WARNING = strtobool(os.environ.get("PYINSTRUMENT_IGNORE_OVERHEAD_WARNING", "0"))
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


class StackSamplerSubscriber:
    def xǁStackSamplerSubscriberǁ__init____mutmut_orig(
        self,
        *,
        target: StackSamplerSubscriberTarget,
        desired_interval: float,
        bound_to_async_context: bool,
        async_state: AsyncState | None,
        use_timing_thread: bool | None = None,
    ) -> None:
        self.target = target
        self.desired_interval = desired_interval
        self.use_timing_thread = use_timing_thread
        self.bound_to_async_context = bound_to_async_context
        self.async_state = async_state
    def xǁStackSamplerSubscriberǁ__init____mutmut_1(
        self,
        *,
        target: StackSamplerSubscriberTarget,
        desired_interval: float,
        bound_to_async_context: bool,
        async_state: AsyncState | None,
        use_timing_thread: bool | None = None,
    ) -> None:
        self.target = None
        self.desired_interval = desired_interval
        self.use_timing_thread = use_timing_thread
        self.bound_to_async_context = bound_to_async_context
        self.async_state = async_state
    def xǁStackSamplerSubscriberǁ__init____mutmut_2(
        self,
        *,
        target: StackSamplerSubscriberTarget,
        desired_interval: float,
        bound_to_async_context: bool,
        async_state: AsyncState | None,
        use_timing_thread: bool | None = None,
    ) -> None:
        self.target = target
        self.desired_interval = None
        self.use_timing_thread = use_timing_thread
        self.bound_to_async_context = bound_to_async_context
        self.async_state = async_state
    def xǁStackSamplerSubscriberǁ__init____mutmut_3(
        self,
        *,
        target: StackSamplerSubscriberTarget,
        desired_interval: float,
        bound_to_async_context: bool,
        async_state: AsyncState | None,
        use_timing_thread: bool | None = None,
    ) -> None:
        self.target = target
        self.desired_interval = desired_interval
        self.use_timing_thread = None
        self.bound_to_async_context = bound_to_async_context
        self.async_state = async_state
    def xǁStackSamplerSubscriberǁ__init____mutmut_4(
        self,
        *,
        target: StackSamplerSubscriberTarget,
        desired_interval: float,
        bound_to_async_context: bool,
        async_state: AsyncState | None,
        use_timing_thread: bool | None = None,
    ) -> None:
        self.target = target
        self.desired_interval = desired_interval
        self.use_timing_thread = use_timing_thread
        self.bound_to_async_context = None
        self.async_state = async_state
    def xǁStackSamplerSubscriberǁ__init____mutmut_5(
        self,
        *,
        target: StackSamplerSubscriberTarget,
        desired_interval: float,
        bound_to_async_context: bool,
        async_state: AsyncState | None,
        use_timing_thread: bool | None = None,
    ) -> None:
        self.target = target
        self.desired_interval = desired_interval
        self.use_timing_thread = use_timing_thread
        self.bound_to_async_context = bound_to_async_context
        self.async_state = None
    
    xǁStackSamplerSubscriberǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStackSamplerSubscriberǁ__init____mutmut_1': xǁStackSamplerSubscriberǁ__init____mutmut_1, 
        'xǁStackSamplerSubscriberǁ__init____mutmut_2': xǁStackSamplerSubscriberǁ__init____mutmut_2, 
        'xǁStackSamplerSubscriberǁ__init____mutmut_3': xǁStackSamplerSubscriberǁ__init____mutmut_3, 
        'xǁStackSamplerSubscriberǁ__init____mutmut_4': xǁStackSamplerSubscriberǁ__init____mutmut_4, 
        'xǁStackSamplerSubscriberǁ__init____mutmut_5': xǁStackSamplerSubscriberǁ__init____mutmut_5
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStackSamplerSubscriberǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁStackSamplerSubscriberǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁStackSamplerSubscriberǁ__init____mutmut_orig)
    xǁStackSamplerSubscriberǁ__init____mutmut_orig.__name__ = 'xǁStackSamplerSubscriberǁ__init__'


active_profiler_context_var: ContextVar[object | None] = ContextVar(
    "active_profiler_context_var", default=None
)


class StackSampler:
    """Manages setstatprofile for Profilers on a single thread"""

    subscribers: list[StackSamplerSubscriber]
    current_sampling_interval: float | None
    last_profile_time: float
    timer_func: Callable[[], float] | None
    has_warned_about_timing_overhead: bool

    def xǁStackSamplerǁ__init____mutmut_orig(self) -> None:
        self.subscribers = []
        self.current_sampling_interval = None
        self.last_profile_time = 0.0
        self.timer_func = None
        self.has_warned_about_timing_overhead = False

    def xǁStackSamplerǁ__init____mutmut_1(self) -> None:
        self.subscribers = None
        self.current_sampling_interval = None
        self.last_profile_time = 0.0
        self.timer_func = None
        self.has_warned_about_timing_overhead = False

    def xǁStackSamplerǁ__init____mutmut_2(self) -> None:
        self.subscribers = []
        self.current_sampling_interval = ""
        self.last_profile_time = 0.0
        self.timer_func = None
        self.has_warned_about_timing_overhead = False

    def xǁStackSamplerǁ__init____mutmut_3(self) -> None:
        self.subscribers = []
        self.current_sampling_interval = None
        self.last_profile_time = None
        self.timer_func = None
        self.has_warned_about_timing_overhead = False

    def xǁStackSamplerǁ__init____mutmut_4(self) -> None:
        self.subscribers = []
        self.current_sampling_interval = None
        self.last_profile_time = 1.0
        self.timer_func = None
        self.has_warned_about_timing_overhead = False

    def xǁStackSamplerǁ__init____mutmut_5(self) -> None:
        self.subscribers = []
        self.current_sampling_interval = None
        self.last_profile_time = 0.0
        self.timer_func = ""
        self.has_warned_about_timing_overhead = False

    def xǁStackSamplerǁ__init____mutmut_6(self) -> None:
        self.subscribers = []
        self.current_sampling_interval = None
        self.last_profile_time = 0.0
        self.timer_func = None
        self.has_warned_about_timing_overhead = None

    def xǁStackSamplerǁ__init____mutmut_7(self) -> None:
        self.subscribers = []
        self.current_sampling_interval = None
        self.last_profile_time = 0.0
        self.timer_func = None
        self.has_warned_about_timing_overhead = True
    
    xǁStackSamplerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStackSamplerǁ__init____mutmut_1': xǁStackSamplerǁ__init____mutmut_1, 
        'xǁStackSamplerǁ__init____mutmut_2': xǁStackSamplerǁ__init____mutmut_2, 
        'xǁStackSamplerǁ__init____mutmut_3': xǁStackSamplerǁ__init____mutmut_3, 
        'xǁStackSamplerǁ__init____mutmut_4': xǁStackSamplerǁ__init____mutmut_4, 
        'xǁStackSamplerǁ__init____mutmut_5': xǁStackSamplerǁ__init____mutmut_5, 
        'xǁStackSamplerǁ__init____mutmut_6': xǁStackSamplerǁ__init____mutmut_6, 
        'xǁStackSamplerǁ__init____mutmut_7': xǁStackSamplerǁ__init____mutmut_7
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStackSamplerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁStackSamplerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁStackSamplerǁ__init____mutmut_orig)
    xǁStackSamplerǁ__init____mutmut_orig.__name__ = 'xǁStackSamplerǁ__init__'

    def xǁStackSamplerǁsubscribe__mutmut_orig(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
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
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_1(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
        use_async_context: bool,
    ):
        if use_async_context:
            if active_profiler_context_var.get() is None:
                raise RuntimeError(
                    "There is already a profiler running. You cannot run multiple profilers in the same thread or async context, unless you disable async support."
                )
            active_profiler_context_var.set(target)

        self.subscribers.append(
            StackSamplerSubscriber(
                target=target,
                desired_interval=desired_interval,
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_2(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
        use_async_context: bool,
    ):
        if use_async_context:
            if active_profiler_context_var.get() is not None:
                raise RuntimeError(
                    None
                )
            active_profiler_context_var.set(target)

        self.subscribers.append(
            StackSamplerSubscriber(
                target=target,
                desired_interval=desired_interval,
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_3(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
        use_async_context: bool,
    ):
        if use_async_context:
            if active_profiler_context_var.get() is not None:
                raise RuntimeError(
                    "XXThere is already a profiler running. You cannot run multiple profilers in the same thread or async context, unless you disable async support.XX"
                )
            active_profiler_context_var.set(target)

        self.subscribers.append(
            StackSamplerSubscriber(
                target=target,
                desired_interval=desired_interval,
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_4(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
        use_async_context: bool,
    ):
        if use_async_context:
            if active_profiler_context_var.get() is not None:
                raise RuntimeError(
                    "there is already a profiler running. you cannot run multiple profilers in the same thread or async context, unless you disable async support."
                )
            active_profiler_context_var.set(target)

        self.subscribers.append(
            StackSamplerSubscriber(
                target=target,
                desired_interval=desired_interval,
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_5(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
        use_async_context: bool,
    ):
        if use_async_context:
            if active_profiler_context_var.get() is not None:
                raise RuntimeError(
                    "THERE IS ALREADY A PROFILER RUNNING. YOU CANNOT RUN MULTIPLE PROFILERS IN THE SAME THREAD OR ASYNC CONTEXT, UNLESS YOU DISABLE ASYNC SUPPORT."
                )
            active_profiler_context_var.set(target)

        self.subscribers.append(
            StackSamplerSubscriber(
                target=target,
                desired_interval=desired_interval,
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_6(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
        use_async_context: bool,
    ):
        if use_async_context:
            if active_profiler_context_var.get() is not None:
                raise RuntimeError(
                    "There is already a profiler running. You cannot run multiple profilers in the same thread or async context, unless you disable async support."
                )
            active_profiler_context_var.set(None)

        self.subscribers.append(
            StackSamplerSubscriber(
                target=target,
                desired_interval=desired_interval,
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_7(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
        use_async_context: bool,
    ):
        if use_async_context:
            if active_profiler_context_var.get() is not None:
                raise RuntimeError(
                    "There is already a profiler running. You cannot run multiple profilers in the same thread or async context, unless you disable async support."
                )
            active_profiler_context_var.set(target)

        self.subscribers.append(
            None
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_8(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
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
                target=None,
                desired_interval=desired_interval,
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_9(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
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
                desired_interval=None,
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_10(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
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
                use_timing_thread=None,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_11(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
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
                use_timing_thread=use_timing_thread,
                bound_to_async_context=None,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_12(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
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
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_13(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
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
                desired_interval=desired_interval,
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_14(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
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
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_15(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
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

    def xǁStackSamplerǁsubscribe__mutmut_16(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
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
                use_timing_thread=use_timing_thread,
                async_state=AsyncState("in_context") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_17(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
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
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_18(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
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
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=AsyncState(None) if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_19(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
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
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("XXin_contextXX") if use_async_context else None,
            )
        )
        self._update()

    def xǁStackSamplerǁsubscribe__mutmut_20(
        self,
        target: StackSamplerSubscriberTarget,
        *,
        desired_interval: float,
        use_timing_thread: bool | None = None,
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
                use_timing_thread=use_timing_thread,
                bound_to_async_context=use_async_context,
                async_state=AsyncState("IN_CONTEXT") if use_async_context else None,
            )
        )
        self._update()
    
    xǁStackSamplerǁsubscribe__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStackSamplerǁsubscribe__mutmut_1': xǁStackSamplerǁsubscribe__mutmut_1, 
        'xǁStackSamplerǁsubscribe__mutmut_2': xǁStackSamplerǁsubscribe__mutmut_2, 
        'xǁStackSamplerǁsubscribe__mutmut_3': xǁStackSamplerǁsubscribe__mutmut_3, 
        'xǁStackSamplerǁsubscribe__mutmut_4': xǁStackSamplerǁsubscribe__mutmut_4, 
        'xǁStackSamplerǁsubscribe__mutmut_5': xǁStackSamplerǁsubscribe__mutmut_5, 
        'xǁStackSamplerǁsubscribe__mutmut_6': xǁStackSamplerǁsubscribe__mutmut_6, 
        'xǁStackSamplerǁsubscribe__mutmut_7': xǁStackSamplerǁsubscribe__mutmut_7, 
        'xǁStackSamplerǁsubscribe__mutmut_8': xǁStackSamplerǁsubscribe__mutmut_8, 
        'xǁStackSamplerǁsubscribe__mutmut_9': xǁStackSamplerǁsubscribe__mutmut_9, 
        'xǁStackSamplerǁsubscribe__mutmut_10': xǁStackSamplerǁsubscribe__mutmut_10, 
        'xǁStackSamplerǁsubscribe__mutmut_11': xǁStackSamplerǁsubscribe__mutmut_11, 
        'xǁStackSamplerǁsubscribe__mutmut_12': xǁStackSamplerǁsubscribe__mutmut_12, 
        'xǁStackSamplerǁsubscribe__mutmut_13': xǁStackSamplerǁsubscribe__mutmut_13, 
        'xǁStackSamplerǁsubscribe__mutmut_14': xǁStackSamplerǁsubscribe__mutmut_14, 
        'xǁStackSamplerǁsubscribe__mutmut_15': xǁStackSamplerǁsubscribe__mutmut_15, 
        'xǁStackSamplerǁsubscribe__mutmut_16': xǁStackSamplerǁsubscribe__mutmut_16, 
        'xǁStackSamplerǁsubscribe__mutmut_17': xǁStackSamplerǁsubscribe__mutmut_17, 
        'xǁStackSamplerǁsubscribe__mutmut_18': xǁStackSamplerǁsubscribe__mutmut_18, 
        'xǁStackSamplerǁsubscribe__mutmut_19': xǁStackSamplerǁsubscribe__mutmut_19, 
        'xǁStackSamplerǁsubscribe__mutmut_20': xǁStackSamplerǁsubscribe__mutmut_20
    }
    
    def subscribe(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStackSamplerǁsubscribe__mutmut_orig"), object.__getattribute__(self, "xǁStackSamplerǁsubscribe__mutmut_mutants"), args, kwargs, self)
        return result 
    
    subscribe.__signature__ = _mutmut_signature(xǁStackSamplerǁsubscribe__mutmut_orig)
    xǁStackSamplerǁsubscribe__mutmut_orig.__name__ = 'xǁStackSamplerǁsubscribe'

    def xǁStackSamplerǁunsubscribe__mutmut_orig(self, target: StackSamplerSubscriberTarget):
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

    def xǁStackSamplerǁunsubscribe__mutmut_1(self, target: StackSamplerSubscriberTarget):
        try:
            subscriber = None  # type: ignore
        except StopIteration:
            raise StackSampler.SubscriberNotFound()

        if subscriber.bound_to_async_context:
            # (don't need to use context_var.reset() because we verified it was
            # None before we started)
            active_profiler_context_var.set(None)

        self.subscribers.remove(subscriber)

        self._update()

    def xǁStackSamplerǁunsubscribe__mutmut_2(self, target: StackSamplerSubscriberTarget):
        try:
            subscriber = next(None)  # type: ignore
        except StopIteration:
            raise StackSampler.SubscriberNotFound()

        if subscriber.bound_to_async_context:
            # (don't need to use context_var.reset() because we verified it was
            # None before we started)
            active_profiler_context_var.set(None)

        self.subscribers.remove(subscriber)

        self._update()

    def xǁStackSamplerǁunsubscribe__mutmut_3(self, target: StackSamplerSubscriberTarget):
        try:
            subscriber = next(s for s in self.subscribers if s.target != target)  # type: ignore
        except StopIteration:
            raise StackSampler.SubscriberNotFound()

        if subscriber.bound_to_async_context:
            # (don't need to use context_var.reset() because we verified it was
            # None before we started)
            active_profiler_context_var.set(None)

        self.subscribers.remove(subscriber)

        self._update()

    def xǁStackSamplerǁunsubscribe__mutmut_4(self, target: StackSamplerSubscriberTarget):
        try:
            subscriber = next(s for s in self.subscribers if s.target == target)  # type: ignore
        except StopIteration:
            raise StackSampler.SubscriberNotFound()

        if subscriber.bound_to_async_context:
            # (don't need to use context_var.reset() because we verified it was
            # None before we started)
            active_profiler_context_var.set(None)

        self.subscribers.remove(None)

        self._update()
    
    xǁStackSamplerǁunsubscribe__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStackSamplerǁunsubscribe__mutmut_1': xǁStackSamplerǁunsubscribe__mutmut_1, 
        'xǁStackSamplerǁunsubscribe__mutmut_2': xǁStackSamplerǁunsubscribe__mutmut_2, 
        'xǁStackSamplerǁunsubscribe__mutmut_3': xǁStackSamplerǁunsubscribe__mutmut_3, 
        'xǁStackSamplerǁunsubscribe__mutmut_4': xǁStackSamplerǁunsubscribe__mutmut_4
    }
    
    def unsubscribe(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStackSamplerǁunsubscribe__mutmut_orig"), object.__getattribute__(self, "xǁStackSamplerǁunsubscribe__mutmut_mutants"), args, kwargs, self)
        return result 
    
    unsubscribe.__signature__ = _mutmut_signature(xǁStackSamplerǁunsubscribe__mutmut_orig)
    xǁStackSamplerǁunsubscribe__mutmut_orig.__name__ = 'xǁStackSamplerǁunsubscribe'

    def xǁStackSamplerǁ_update__mutmut_orig(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_1(self):
        if len(self.subscribers) != 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_2(self):
        if len(self.subscribers) == 1:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_3(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = None
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_4(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(None)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_5(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = None
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_6(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_7(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_8(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) >= 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_9(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 2:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_10(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                None
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_11(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = None

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_12(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(None, False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_13(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), None)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_14(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_15(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), )

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_16(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(None), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_17(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), True)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_18(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval == min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_19(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=None, use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_20(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, use_timing_thread=None
            )

    def xǁStackSamplerǁ_update__mutmut_21(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                use_timing_thread=use_timing_thread
            )

    def xǁStackSamplerǁ_update__mutmut_22(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)
        timing_thread_preferences = set(
            s.use_timing_thread for s in self.subscribers if s.use_timing_thread is not None
        )
        if len(timing_thread_preferences) > 1:
            raise ValueError(
                f"Profiler requested different timing thread preferences from a profiler that is already running."
            )

        use_timing_thread = next(iter(timing_thread_preferences), False)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(
                interval=min_subscribers_interval, )
    
    xǁStackSamplerǁ_update__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStackSamplerǁ_update__mutmut_1': xǁStackSamplerǁ_update__mutmut_1, 
        'xǁStackSamplerǁ_update__mutmut_2': xǁStackSamplerǁ_update__mutmut_2, 
        'xǁStackSamplerǁ_update__mutmut_3': xǁStackSamplerǁ_update__mutmut_3, 
        'xǁStackSamplerǁ_update__mutmut_4': xǁStackSamplerǁ_update__mutmut_4, 
        'xǁStackSamplerǁ_update__mutmut_5': xǁStackSamplerǁ_update__mutmut_5, 
        'xǁStackSamplerǁ_update__mutmut_6': xǁStackSamplerǁ_update__mutmut_6, 
        'xǁStackSamplerǁ_update__mutmut_7': xǁStackSamplerǁ_update__mutmut_7, 
        'xǁStackSamplerǁ_update__mutmut_8': xǁStackSamplerǁ_update__mutmut_8, 
        'xǁStackSamplerǁ_update__mutmut_9': xǁStackSamplerǁ_update__mutmut_9, 
        'xǁStackSamplerǁ_update__mutmut_10': xǁStackSamplerǁ_update__mutmut_10, 
        'xǁStackSamplerǁ_update__mutmut_11': xǁStackSamplerǁ_update__mutmut_11, 
        'xǁStackSamplerǁ_update__mutmut_12': xǁStackSamplerǁ_update__mutmut_12, 
        'xǁStackSamplerǁ_update__mutmut_13': xǁStackSamplerǁ_update__mutmut_13, 
        'xǁStackSamplerǁ_update__mutmut_14': xǁStackSamplerǁ_update__mutmut_14, 
        'xǁStackSamplerǁ_update__mutmut_15': xǁStackSamplerǁ_update__mutmut_15, 
        'xǁStackSamplerǁ_update__mutmut_16': xǁStackSamplerǁ_update__mutmut_16, 
        'xǁStackSamplerǁ_update__mutmut_17': xǁStackSamplerǁ_update__mutmut_17, 
        'xǁStackSamplerǁ_update__mutmut_18': xǁStackSamplerǁ_update__mutmut_18, 
        'xǁStackSamplerǁ_update__mutmut_19': xǁStackSamplerǁ_update__mutmut_19, 
        'xǁStackSamplerǁ_update__mutmut_20': xǁStackSamplerǁ_update__mutmut_20, 
        'xǁStackSamplerǁ_update__mutmut_21': xǁStackSamplerǁ_update__mutmut_21, 
        'xǁStackSamplerǁ_update__mutmut_22': xǁStackSamplerǁ_update__mutmut_22
    }
    
    def _update(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStackSamplerǁ_update__mutmut_orig"), object.__getattribute__(self, "xǁStackSamplerǁ_update__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _update.__signature__ = _mutmut_signature(xǁStackSamplerǁ_update__mutmut_orig)
    xǁStackSamplerǁ_update__mutmut_orig.__name__ = 'xǁStackSamplerǁ_update'

    def xǁStackSamplerǁ_start_sampling__mutmut_orig(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_1(self, interval: float, use_timing_thread: bool):
        if use_timing_thread or self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_2(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_3(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                None
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_4(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = None
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_5(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "XXtimer_funcXX"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_6(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "TIMER_FUNC"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_7(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = None
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_8(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "XXwalltime_threadXX"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_9(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "WALLTIME_THREAD"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_10(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = None
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_11(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None or coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_12(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_13(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution < interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_14(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = None
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_15(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "XXwalltime_coarseXX"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_16(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "WALLTIME_COARSE"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_17(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = None

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_18(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "XXwalltimeXX"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_19(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "WALLTIME"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_20(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=None, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_21(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=None)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_22(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_23(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, )

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_24(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = None
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_25(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time != 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_26(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 1.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_27(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = None

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_28(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=None,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_29(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=None,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_30(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=None,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_31(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=None,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_32(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=None,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_33(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_34(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_35(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            timer_type=timer_type,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_36(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_func=self.timer_func,
        )

    def xǁStackSamplerǁ_start_sampling__mutmut_37(self, interval: float, use_timing_thread: bool):
        if use_timing_thread and self.timer_func is not None:
            raise ValueError(
                f"Profiler requested to use the timing thread but this stack sampler is already using a custom timer function."
            )

        timer_type: TimerType

        if self.timer_func:
            timer_type = "timer_func"
        elif use_timing_thread:
            timer_type = "walltime_thread"
        else:
            coarse_resolution = walltime_coarse_resolution()
            if coarse_resolution is not None and coarse_resolution <= interval:
                timer_type = "walltime_coarse"
            else:
                timer_type = "walltime"

        self._check_timing_overhead(interval=interval, timer_type=timer_type)

        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = self._timer()

        setstatprofile(
            target=self._sample,
            interval=interval,
            context_var=active_profiler_context_var,
            timer_type=timer_type,
            )
    
    xǁStackSamplerǁ_start_sampling__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStackSamplerǁ_start_sampling__mutmut_1': xǁStackSamplerǁ_start_sampling__mutmut_1, 
        'xǁStackSamplerǁ_start_sampling__mutmut_2': xǁStackSamplerǁ_start_sampling__mutmut_2, 
        'xǁStackSamplerǁ_start_sampling__mutmut_3': xǁStackSamplerǁ_start_sampling__mutmut_3, 
        'xǁStackSamplerǁ_start_sampling__mutmut_4': xǁStackSamplerǁ_start_sampling__mutmut_4, 
        'xǁStackSamplerǁ_start_sampling__mutmut_5': xǁStackSamplerǁ_start_sampling__mutmut_5, 
        'xǁStackSamplerǁ_start_sampling__mutmut_6': xǁStackSamplerǁ_start_sampling__mutmut_6, 
        'xǁStackSamplerǁ_start_sampling__mutmut_7': xǁStackSamplerǁ_start_sampling__mutmut_7, 
        'xǁStackSamplerǁ_start_sampling__mutmut_8': xǁStackSamplerǁ_start_sampling__mutmut_8, 
        'xǁStackSamplerǁ_start_sampling__mutmut_9': xǁStackSamplerǁ_start_sampling__mutmut_9, 
        'xǁStackSamplerǁ_start_sampling__mutmut_10': xǁStackSamplerǁ_start_sampling__mutmut_10, 
        'xǁStackSamplerǁ_start_sampling__mutmut_11': xǁStackSamplerǁ_start_sampling__mutmut_11, 
        'xǁStackSamplerǁ_start_sampling__mutmut_12': xǁStackSamplerǁ_start_sampling__mutmut_12, 
        'xǁStackSamplerǁ_start_sampling__mutmut_13': xǁStackSamplerǁ_start_sampling__mutmut_13, 
        'xǁStackSamplerǁ_start_sampling__mutmut_14': xǁStackSamplerǁ_start_sampling__mutmut_14, 
        'xǁStackSamplerǁ_start_sampling__mutmut_15': xǁStackSamplerǁ_start_sampling__mutmut_15, 
        'xǁStackSamplerǁ_start_sampling__mutmut_16': xǁStackSamplerǁ_start_sampling__mutmut_16, 
        'xǁStackSamplerǁ_start_sampling__mutmut_17': xǁStackSamplerǁ_start_sampling__mutmut_17, 
        'xǁStackSamplerǁ_start_sampling__mutmut_18': xǁStackSamplerǁ_start_sampling__mutmut_18, 
        'xǁStackSamplerǁ_start_sampling__mutmut_19': xǁStackSamplerǁ_start_sampling__mutmut_19, 
        'xǁStackSamplerǁ_start_sampling__mutmut_20': xǁStackSamplerǁ_start_sampling__mutmut_20, 
        'xǁStackSamplerǁ_start_sampling__mutmut_21': xǁStackSamplerǁ_start_sampling__mutmut_21, 
        'xǁStackSamplerǁ_start_sampling__mutmut_22': xǁStackSamplerǁ_start_sampling__mutmut_22, 
        'xǁStackSamplerǁ_start_sampling__mutmut_23': xǁStackSamplerǁ_start_sampling__mutmut_23, 
        'xǁStackSamplerǁ_start_sampling__mutmut_24': xǁStackSamplerǁ_start_sampling__mutmut_24, 
        'xǁStackSamplerǁ_start_sampling__mutmut_25': xǁStackSamplerǁ_start_sampling__mutmut_25, 
        'xǁStackSamplerǁ_start_sampling__mutmut_26': xǁStackSamplerǁ_start_sampling__mutmut_26, 
        'xǁStackSamplerǁ_start_sampling__mutmut_27': xǁStackSamplerǁ_start_sampling__mutmut_27, 
        'xǁStackSamplerǁ_start_sampling__mutmut_28': xǁStackSamplerǁ_start_sampling__mutmut_28, 
        'xǁStackSamplerǁ_start_sampling__mutmut_29': xǁStackSamplerǁ_start_sampling__mutmut_29, 
        'xǁStackSamplerǁ_start_sampling__mutmut_30': xǁStackSamplerǁ_start_sampling__mutmut_30, 
        'xǁStackSamplerǁ_start_sampling__mutmut_31': xǁStackSamplerǁ_start_sampling__mutmut_31, 
        'xǁStackSamplerǁ_start_sampling__mutmut_32': xǁStackSamplerǁ_start_sampling__mutmut_32, 
        'xǁStackSamplerǁ_start_sampling__mutmut_33': xǁStackSamplerǁ_start_sampling__mutmut_33, 
        'xǁStackSamplerǁ_start_sampling__mutmut_34': xǁStackSamplerǁ_start_sampling__mutmut_34, 
        'xǁStackSamplerǁ_start_sampling__mutmut_35': xǁStackSamplerǁ_start_sampling__mutmut_35, 
        'xǁStackSamplerǁ_start_sampling__mutmut_36': xǁStackSamplerǁ_start_sampling__mutmut_36, 
        'xǁStackSamplerǁ_start_sampling__mutmut_37': xǁStackSamplerǁ_start_sampling__mutmut_37
    }
    
    def _start_sampling(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStackSamplerǁ_start_sampling__mutmut_orig"), object.__getattribute__(self, "xǁStackSamplerǁ_start_sampling__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _start_sampling.__signature__ = _mutmut_signature(xǁStackSamplerǁ_start_sampling__mutmut_orig)
    xǁStackSamplerǁ_start_sampling__mutmut_orig.__name__ = 'xǁStackSamplerǁ_start_sampling'

    def xǁStackSamplerǁ_stop_sampling__mutmut_orig(self):
        setstatprofile(None)
        self.current_sampling_interval = None
        self.last_profile_time = 0.0

    def xǁStackSamplerǁ_stop_sampling__mutmut_1(self):
        setstatprofile(None)
        self.current_sampling_interval = ""
        self.last_profile_time = 0.0

    def xǁStackSamplerǁ_stop_sampling__mutmut_2(self):
        setstatprofile(None)
        self.current_sampling_interval = None
        self.last_profile_time = None

    def xǁStackSamplerǁ_stop_sampling__mutmut_3(self):
        setstatprofile(None)
        self.current_sampling_interval = None
        self.last_profile_time = 1.0
    
    xǁStackSamplerǁ_stop_sampling__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStackSamplerǁ_stop_sampling__mutmut_1': xǁStackSamplerǁ_stop_sampling__mutmut_1, 
        'xǁStackSamplerǁ_stop_sampling__mutmut_2': xǁStackSamplerǁ_stop_sampling__mutmut_2, 
        'xǁStackSamplerǁ_stop_sampling__mutmut_3': xǁStackSamplerǁ_stop_sampling__mutmut_3
    }
    
    def _stop_sampling(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStackSamplerǁ_stop_sampling__mutmut_orig"), object.__getattribute__(self, "xǁStackSamplerǁ_stop_sampling__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _stop_sampling.__signature__ = _mutmut_signature(xǁStackSamplerǁ_stop_sampling__mutmut_orig)
    xǁStackSamplerǁ_stop_sampling__mutmut_orig.__name__ = 'xǁStackSamplerǁ_stop_sampling'

    def xǁStackSamplerǁ_sample__mutmut_orig(self, frame: types.FrameType, event: str, arg: Any):
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

    def xǁStackSamplerǁ_sample__mutmut_1(self, frame: types.FrameType, event: str, arg: Any):
        if event != "context_changed":
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

    def xǁStackSamplerǁ_sample__mutmut_2(self, frame: types.FrameType, event: str, arg: Any):
        if event == "XXcontext_changedXX":
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

    def xǁStackSamplerǁ_sample__mutmut_3(self, frame: types.FrameType, event: str, arg: Any):
        if event == "CONTEXT_CHANGED":
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

    def xǁStackSamplerǁ_sample__mutmut_4(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = None

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

    def xǁStackSamplerǁ_sample__mutmut_5(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target != old:
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

    def xǁStackSamplerǁ_sample__mutmut_6(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = None
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

    def xǁStackSamplerǁ_sample__mutmut_7(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(None, event, arg)
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

    def xǁStackSamplerǁ_sample__mutmut_8(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(frame, None, arg)
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

    def xǁStackSamplerǁ_sample__mutmut_9(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(frame, event, None)
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

    def xǁStackSamplerǁ_sample__mutmut_10(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(event, arg)
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

    def xǁStackSamplerǁ_sample__mutmut_11(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(frame, arg)
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

    def xǁStackSamplerǁ_sample__mutmut_12(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(frame, event, )
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

    def xǁStackSamplerǁ_sample__mutmut_13(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(frame, event, arg)
                    if coroutine_stack:
                        full_stack.extend(None)
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

    def xǁStackSamplerǁ_sample__mutmut_14(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(frame, event, arg)
                    if coroutine_stack:
                        full_stack.extend(reversed(None))
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

    def xǁStackSamplerǁ_sample__mutmut_15(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(frame, event, arg)
                    if coroutine_stack:
                        full_stack.extend(reversed(coroutine_stack))
                        subscriber.async_state = None
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

    def xǁStackSamplerǁ_sample__mutmut_16(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(frame, event, arg)
                    if coroutine_stack:
                        full_stack.extend(reversed(coroutine_stack))
                        subscriber.async_state = AsyncState(
                            None, info=full_stack
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

    def xǁStackSamplerǁ_sample__mutmut_17(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(frame, event, arg)
                    if coroutine_stack:
                        full_stack.extend(reversed(coroutine_stack))
                        subscriber.async_state = AsyncState(
                            "out_of_context_awaited", info=None
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

    def xǁStackSamplerǁ_sample__mutmut_18(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(frame, event, arg)
                    if coroutine_stack:
                        full_stack.extend(reversed(coroutine_stack))
                        subscriber.async_state = AsyncState(
                            info=full_stack
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

    def xǁStackSamplerǁ_sample__mutmut_19(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(frame, event, arg)
                    if coroutine_stack:
                        full_stack.extend(reversed(coroutine_stack))
                        subscriber.async_state = AsyncState(
                            "out_of_context_awaited", )
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

    def xǁStackSamplerǁ_sample__mutmut_20(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(frame, event, arg)
                    if coroutine_stack:
                        full_stack.extend(reversed(coroutine_stack))
                        subscriber.async_state = AsyncState(
                            "XXout_of_context_awaitedXX", info=full_stack
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

    def xǁStackSamplerǁ_sample__mutmut_21(self, frame: types.FrameType, event: str, arg: Any):
        if event == "context_changed":
            new, old, coroutine_stack = arg

            for subscriber in self.subscribers:
                if subscriber.target == old:
                    assert subscriber.bound_to_async_context
                    full_stack = build_call_stack(frame, event, arg)
                    if coroutine_stack:
                        full_stack.extend(reversed(coroutine_stack))
                        subscriber.async_state = AsyncState(
                            "OUT_OF_CONTEXT_AWAITED", info=full_stack
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

    def xǁStackSamplerǁ_sample__mutmut_22(self, frame: types.FrameType, event: str, arg: Any):
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
                        subscriber.async_state = None
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

    def xǁStackSamplerǁ_sample__mutmut_23(self, frame: types.FrameType, event: str, arg: Any):
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
                            None, info=full_stack
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

    def xǁStackSamplerǁ_sample__mutmut_24(self, frame: types.FrameType, event: str, arg: Any):
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
                            "out_of_context_unknown", info=None
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

    def xǁStackSamplerǁ_sample__mutmut_25(self, frame: types.FrameType, event: str, arg: Any):
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
                            info=full_stack
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

    def xǁStackSamplerǁ_sample__mutmut_26(self, frame: types.FrameType, event: str, arg: Any):
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
                            "out_of_context_unknown", )
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

    def xǁStackSamplerǁ_sample__mutmut_27(self, frame: types.FrameType, event: str, arg: Any):
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
                            "XXout_of_context_unknownXX", info=full_stack
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

    def xǁStackSamplerǁ_sample__mutmut_28(self, frame: types.FrameType, event: str, arg: Any):
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
                            "OUT_OF_CONTEXT_UNKNOWN", info=full_stack
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

    def xǁStackSamplerǁ_sample__mutmut_29(self, frame: types.FrameType, event: str, arg: Any):
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
                elif subscriber.target != new:
                    assert subscriber.bound_to_async_context
                    subscriber.async_state = AsyncState("in_context")
        else:
            now = self._timer()
            time_since_last_sample = now - self.last_profile_time

            call_stack = build_call_stack(frame, event, arg)

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_30(self, frame: types.FrameType, event: str, arg: Any):
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
                    subscriber.async_state = None
        else:
            now = self._timer()
            time_since_last_sample = now - self.last_profile_time

            call_stack = build_call_stack(frame, event, arg)

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_31(self, frame: types.FrameType, event: str, arg: Any):
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
                    subscriber.async_state = AsyncState(None)
        else:
            now = self._timer()
            time_since_last_sample = now - self.last_profile_time

            call_stack = build_call_stack(frame, event, arg)

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_32(self, frame: types.FrameType, event: str, arg: Any):
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
                    subscriber.async_state = AsyncState("XXin_contextXX")
        else:
            now = self._timer()
            time_since_last_sample = now - self.last_profile_time

            call_stack = build_call_stack(frame, event, arg)

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_33(self, frame: types.FrameType, event: str, arg: Any):
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
                    subscriber.async_state = AsyncState("IN_CONTEXT")
        else:
            now = self._timer()
            time_since_last_sample = now - self.last_profile_time

            call_stack = build_call_stack(frame, event, arg)

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_34(self, frame: types.FrameType, event: str, arg: Any):
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
            now = None
            time_since_last_sample = now - self.last_profile_time

            call_stack = build_call_stack(frame, event, arg)

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_35(self, frame: types.FrameType, event: str, arg: Any):
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
            time_since_last_sample = None

            call_stack = build_call_stack(frame, event, arg)

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_36(self, frame: types.FrameType, event: str, arg: Any):
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
            time_since_last_sample = now + self.last_profile_time

            call_stack = build_call_stack(frame, event, arg)

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_37(self, frame: types.FrameType, event: str, arg: Any):
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

            call_stack = None

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_38(self, frame: types.FrameType, event: str, arg: Any):
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

            call_stack = build_call_stack(None, event, arg)

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_39(self, frame: types.FrameType, event: str, arg: Any):
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

            call_stack = build_call_stack(frame, None, arg)

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_40(self, frame: types.FrameType, event: str, arg: Any):
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

            call_stack = build_call_stack(frame, event, None)

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_41(self, frame: types.FrameType, event: str, arg: Any):
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

            call_stack = build_call_stack(event, arg)

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_42(self, frame: types.FrameType, event: str, arg: Any):
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

            call_stack = build_call_stack(frame, arg)

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_43(self, frame: types.FrameType, event: str, arg: Any):
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

            call_stack = build_call_stack(frame, event, )

            for subscriber in self.subscribers:
                subscriber.target(call_stack, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_44(self, frame: types.FrameType, event: str, arg: Any):
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
                subscriber.target(None, time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_45(self, frame: types.FrameType, event: str, arg: Any):
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
                subscriber.target(call_stack, None, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_46(self, frame: types.FrameType, event: str, arg: Any):
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
                subscriber.target(call_stack, time_since_last_sample, None)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_47(self, frame: types.FrameType, event: str, arg: Any):
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
                subscriber.target(time_since_last_sample, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_48(self, frame: types.FrameType, event: str, arg: Any):
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
                subscriber.target(call_stack, subscriber.async_state)

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_49(self, frame: types.FrameType, event: str, arg: Any):
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
                subscriber.target(call_stack, time_since_last_sample, )

            self.last_profile_time = now

    def xǁStackSamplerǁ_sample__mutmut_50(self, frame: types.FrameType, event: str, arg: Any):
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

            self.last_profile_time = None
    
    xǁStackSamplerǁ_sample__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStackSamplerǁ_sample__mutmut_1': xǁStackSamplerǁ_sample__mutmut_1, 
        'xǁStackSamplerǁ_sample__mutmut_2': xǁStackSamplerǁ_sample__mutmut_2, 
        'xǁStackSamplerǁ_sample__mutmut_3': xǁStackSamplerǁ_sample__mutmut_3, 
        'xǁStackSamplerǁ_sample__mutmut_4': xǁStackSamplerǁ_sample__mutmut_4, 
        'xǁStackSamplerǁ_sample__mutmut_5': xǁStackSamplerǁ_sample__mutmut_5, 
        'xǁStackSamplerǁ_sample__mutmut_6': xǁStackSamplerǁ_sample__mutmut_6, 
        'xǁStackSamplerǁ_sample__mutmut_7': xǁStackSamplerǁ_sample__mutmut_7, 
        'xǁStackSamplerǁ_sample__mutmut_8': xǁStackSamplerǁ_sample__mutmut_8, 
        'xǁStackSamplerǁ_sample__mutmut_9': xǁStackSamplerǁ_sample__mutmut_9, 
        'xǁStackSamplerǁ_sample__mutmut_10': xǁStackSamplerǁ_sample__mutmut_10, 
        'xǁStackSamplerǁ_sample__mutmut_11': xǁStackSamplerǁ_sample__mutmut_11, 
        'xǁStackSamplerǁ_sample__mutmut_12': xǁStackSamplerǁ_sample__mutmut_12, 
        'xǁStackSamplerǁ_sample__mutmut_13': xǁStackSamplerǁ_sample__mutmut_13, 
        'xǁStackSamplerǁ_sample__mutmut_14': xǁStackSamplerǁ_sample__mutmut_14, 
        'xǁStackSamplerǁ_sample__mutmut_15': xǁStackSamplerǁ_sample__mutmut_15, 
        'xǁStackSamplerǁ_sample__mutmut_16': xǁStackSamplerǁ_sample__mutmut_16, 
        'xǁStackSamplerǁ_sample__mutmut_17': xǁStackSamplerǁ_sample__mutmut_17, 
        'xǁStackSamplerǁ_sample__mutmut_18': xǁStackSamplerǁ_sample__mutmut_18, 
        'xǁStackSamplerǁ_sample__mutmut_19': xǁStackSamplerǁ_sample__mutmut_19, 
        'xǁStackSamplerǁ_sample__mutmut_20': xǁStackSamplerǁ_sample__mutmut_20, 
        'xǁStackSamplerǁ_sample__mutmut_21': xǁStackSamplerǁ_sample__mutmut_21, 
        'xǁStackSamplerǁ_sample__mutmut_22': xǁStackSamplerǁ_sample__mutmut_22, 
        'xǁStackSamplerǁ_sample__mutmut_23': xǁStackSamplerǁ_sample__mutmut_23, 
        'xǁStackSamplerǁ_sample__mutmut_24': xǁStackSamplerǁ_sample__mutmut_24, 
        'xǁStackSamplerǁ_sample__mutmut_25': xǁStackSamplerǁ_sample__mutmut_25, 
        'xǁStackSamplerǁ_sample__mutmut_26': xǁStackSamplerǁ_sample__mutmut_26, 
        'xǁStackSamplerǁ_sample__mutmut_27': xǁStackSamplerǁ_sample__mutmut_27, 
        'xǁStackSamplerǁ_sample__mutmut_28': xǁStackSamplerǁ_sample__mutmut_28, 
        'xǁStackSamplerǁ_sample__mutmut_29': xǁStackSamplerǁ_sample__mutmut_29, 
        'xǁStackSamplerǁ_sample__mutmut_30': xǁStackSamplerǁ_sample__mutmut_30, 
        'xǁStackSamplerǁ_sample__mutmut_31': xǁStackSamplerǁ_sample__mutmut_31, 
        'xǁStackSamplerǁ_sample__mutmut_32': xǁStackSamplerǁ_sample__mutmut_32, 
        'xǁStackSamplerǁ_sample__mutmut_33': xǁStackSamplerǁ_sample__mutmut_33, 
        'xǁStackSamplerǁ_sample__mutmut_34': xǁStackSamplerǁ_sample__mutmut_34, 
        'xǁStackSamplerǁ_sample__mutmut_35': xǁStackSamplerǁ_sample__mutmut_35, 
        'xǁStackSamplerǁ_sample__mutmut_36': xǁStackSamplerǁ_sample__mutmut_36, 
        'xǁStackSamplerǁ_sample__mutmut_37': xǁStackSamplerǁ_sample__mutmut_37, 
        'xǁStackSamplerǁ_sample__mutmut_38': xǁStackSamplerǁ_sample__mutmut_38, 
        'xǁStackSamplerǁ_sample__mutmut_39': xǁStackSamplerǁ_sample__mutmut_39, 
        'xǁStackSamplerǁ_sample__mutmut_40': xǁStackSamplerǁ_sample__mutmut_40, 
        'xǁStackSamplerǁ_sample__mutmut_41': xǁStackSamplerǁ_sample__mutmut_41, 
        'xǁStackSamplerǁ_sample__mutmut_42': xǁStackSamplerǁ_sample__mutmut_42, 
        'xǁStackSamplerǁ_sample__mutmut_43': xǁStackSamplerǁ_sample__mutmut_43, 
        'xǁStackSamplerǁ_sample__mutmut_44': xǁStackSamplerǁ_sample__mutmut_44, 
        'xǁStackSamplerǁ_sample__mutmut_45': xǁStackSamplerǁ_sample__mutmut_45, 
        'xǁStackSamplerǁ_sample__mutmut_46': xǁStackSamplerǁ_sample__mutmut_46, 
        'xǁStackSamplerǁ_sample__mutmut_47': xǁStackSamplerǁ_sample__mutmut_47, 
        'xǁStackSamplerǁ_sample__mutmut_48': xǁStackSamplerǁ_sample__mutmut_48, 
        'xǁStackSamplerǁ_sample__mutmut_49': xǁStackSamplerǁ_sample__mutmut_49, 
        'xǁStackSamplerǁ_sample__mutmut_50': xǁStackSamplerǁ_sample__mutmut_50
    }
    
    def _sample(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStackSamplerǁ_sample__mutmut_orig"), object.__getattribute__(self, "xǁStackSamplerǁ_sample__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _sample.__signature__ = _mutmut_signature(xǁStackSamplerǁ_sample__mutmut_orig)
    xǁStackSamplerǁ_sample__mutmut_orig.__name__ = 'xǁStackSamplerǁ_sample'

    def _timer(self):
        if self.timer_func:
            return self.timer_func()
        else:
            return timeit.default_timer()

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_orig(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_1(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = None
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_2(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = None
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_3(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(None)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_4(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is not None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_5(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type != "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_6(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "XXwalltimeXX":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_7(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "WALLTIME":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_8(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead >= 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_9(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 1.0000003:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_10(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = None
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_11(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = False
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_12(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = None
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_13(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    None
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_14(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead / 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_15(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1000000001.0:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_16(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    None
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_17(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads or overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_18(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "XXwalltime_coarseXX" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_19(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "WALLTIME_COARSE" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_20(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" not in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_21(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["XXwalltime_coarseXX"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_22(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["WALLTIME_COARSE"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_23(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] <= 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_24(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 1.0000003:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_25(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = None
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_26(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_27(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        None
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_28(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] / 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_29(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["XXwalltime_coarseXX"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_30(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["WALLTIME_COARSE"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_31(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1000000001.0:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_32(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(None,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_33(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=None)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_34(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_35(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        )} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_36(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=False)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_37(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    None
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_38(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = None

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_39(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    None
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_40(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "XX\n\nXX".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_41(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(None, width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_42(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=None) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_43(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_44(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), ) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_45(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(None), width=80) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_46(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=81) for part in message_parts
                )

                print(message, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_47(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(None, file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_48(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, file=None)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_49(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(file=sys.stderr)

    def xǁStackSamplerǁ_check_timing_overhead__mutmut_50(self, interval: float, timer_type: TimerType):
        if self.has_warned_about_timing_overhead:
            return
        if IGNORE_OVERHEAD_WARNING:
            return

        overheads = timing_overhead()
        overhead = overheads.get(timer_type)
        if overhead is None:
            return

        if timer_type == "walltime":
            if overhead > 300e-9:
                self.has_warned_about_timing_overhead = True
                message_parts: list[str] = []
                message_parts.append(
                    f"""
                    pyinstrument: the timer on your system has an overhead of
                    {overhead * 1e9:.0f} nanoseconds, which is considered
                    high. You might experience longer runtimes than usual, and
                    programs with lots of pure-python code might be distorted.
                    """
                )

                message_parts.append(
                    f"""
                    You might want to try the timing thread option, which can
                    be enabled using --use-timing-thread at the command line,
                    or by setting the use_timing_thread parameter in the
                    Profiler constructor.
                    """
                )

                if "walltime_coarse" in overheads and overheads["walltime_coarse"] < 300e-9:
                    coarse_resolution = walltime_coarse_resolution()
                    assert coarse_resolution is not None
                    message_parts.append(
                        f"""
                        Your system does offer a 'coarse' timer, with a lower
                        overhead ({overheads["walltime_coarse"] * 1e9:.2g}
                        nanoseconds). You can enable it by setting
                        pyinstrument's interval to a value higher than
                        {format_float_with_sig_figs(coarse_resolution,
                        trim_zeroes=True)} seconds. If you're happy with the
                        lower precision, this is the best option.
                        """
                    )

                message_parts.append(
                    f"""
                    If you want to suppress this warning, you can set the
                    environment variable PYINSTRUMENT_IGNORE_OVERHEAD_WARNING
                    to '1'.
                    """
                )

                message = "\n\n".join(
                    textwrap.fill(unwrap(part), width=80) for part in message_parts
                )

                print(message, )
    
    xǁStackSamplerǁ_check_timing_overhead__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStackSamplerǁ_check_timing_overhead__mutmut_1': xǁStackSamplerǁ_check_timing_overhead__mutmut_1, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_2': xǁStackSamplerǁ_check_timing_overhead__mutmut_2, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_3': xǁStackSamplerǁ_check_timing_overhead__mutmut_3, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_4': xǁStackSamplerǁ_check_timing_overhead__mutmut_4, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_5': xǁStackSamplerǁ_check_timing_overhead__mutmut_5, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_6': xǁStackSamplerǁ_check_timing_overhead__mutmut_6, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_7': xǁStackSamplerǁ_check_timing_overhead__mutmut_7, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_8': xǁStackSamplerǁ_check_timing_overhead__mutmut_8, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_9': xǁStackSamplerǁ_check_timing_overhead__mutmut_9, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_10': xǁStackSamplerǁ_check_timing_overhead__mutmut_10, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_11': xǁStackSamplerǁ_check_timing_overhead__mutmut_11, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_12': xǁStackSamplerǁ_check_timing_overhead__mutmut_12, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_13': xǁStackSamplerǁ_check_timing_overhead__mutmut_13, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_14': xǁStackSamplerǁ_check_timing_overhead__mutmut_14, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_15': xǁStackSamplerǁ_check_timing_overhead__mutmut_15, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_16': xǁStackSamplerǁ_check_timing_overhead__mutmut_16, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_17': xǁStackSamplerǁ_check_timing_overhead__mutmut_17, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_18': xǁStackSamplerǁ_check_timing_overhead__mutmut_18, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_19': xǁStackSamplerǁ_check_timing_overhead__mutmut_19, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_20': xǁStackSamplerǁ_check_timing_overhead__mutmut_20, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_21': xǁStackSamplerǁ_check_timing_overhead__mutmut_21, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_22': xǁStackSamplerǁ_check_timing_overhead__mutmut_22, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_23': xǁStackSamplerǁ_check_timing_overhead__mutmut_23, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_24': xǁStackSamplerǁ_check_timing_overhead__mutmut_24, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_25': xǁStackSamplerǁ_check_timing_overhead__mutmut_25, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_26': xǁStackSamplerǁ_check_timing_overhead__mutmut_26, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_27': xǁStackSamplerǁ_check_timing_overhead__mutmut_27, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_28': xǁStackSamplerǁ_check_timing_overhead__mutmut_28, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_29': xǁStackSamplerǁ_check_timing_overhead__mutmut_29, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_30': xǁStackSamplerǁ_check_timing_overhead__mutmut_30, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_31': xǁStackSamplerǁ_check_timing_overhead__mutmut_31, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_32': xǁStackSamplerǁ_check_timing_overhead__mutmut_32, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_33': xǁStackSamplerǁ_check_timing_overhead__mutmut_33, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_34': xǁStackSamplerǁ_check_timing_overhead__mutmut_34, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_35': xǁStackSamplerǁ_check_timing_overhead__mutmut_35, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_36': xǁStackSamplerǁ_check_timing_overhead__mutmut_36, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_37': xǁStackSamplerǁ_check_timing_overhead__mutmut_37, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_38': xǁStackSamplerǁ_check_timing_overhead__mutmut_38, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_39': xǁStackSamplerǁ_check_timing_overhead__mutmut_39, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_40': xǁStackSamplerǁ_check_timing_overhead__mutmut_40, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_41': xǁStackSamplerǁ_check_timing_overhead__mutmut_41, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_42': xǁStackSamplerǁ_check_timing_overhead__mutmut_42, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_43': xǁStackSamplerǁ_check_timing_overhead__mutmut_43, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_44': xǁStackSamplerǁ_check_timing_overhead__mutmut_44, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_45': xǁStackSamplerǁ_check_timing_overhead__mutmut_45, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_46': xǁStackSamplerǁ_check_timing_overhead__mutmut_46, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_47': xǁStackSamplerǁ_check_timing_overhead__mutmut_47, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_48': xǁStackSamplerǁ_check_timing_overhead__mutmut_48, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_49': xǁStackSamplerǁ_check_timing_overhead__mutmut_49, 
        'xǁStackSamplerǁ_check_timing_overhead__mutmut_50': xǁStackSamplerǁ_check_timing_overhead__mutmut_50
    }
    
    def _check_timing_overhead(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStackSamplerǁ_check_timing_overhead__mutmut_orig"), object.__getattribute__(self, "xǁStackSamplerǁ_check_timing_overhead__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _check_timing_overhead.__signature__ = _mutmut_signature(xǁStackSamplerǁ_check_timing_overhead__mutmut_orig)
    xǁStackSamplerǁ_check_timing_overhead__mutmut_orig.__name__ = 'xǁStackSamplerǁ_check_timing_overhead'

    class SubscriberNotFound(Exception):
        pass


def x_get_stack_sampler__mutmut_orig() -> StackSampler:
    """
    Gets the stack sampler for the current thread, creating it if necessary
    """
    try:
        return thread_locals.stack_sampler
    except AttributeError:
        # Attribute 'stack_sampler' doesn't exist in thread_locals, create it
        stack_sampler = StackSampler()
        thread_locals.stack_sampler = stack_sampler
        return stack_sampler


def x_get_stack_sampler__mutmut_1() -> StackSampler:
    """
    Gets the stack sampler for the current thread, creating it if necessary
    """
    try:
        return thread_locals.stack_sampler
    except AttributeError:
        # Attribute 'stack_sampler' doesn't exist in thread_locals, create it
        stack_sampler = None
        thread_locals.stack_sampler = stack_sampler
        return stack_sampler


def x_get_stack_sampler__mutmut_2() -> StackSampler:
    """
    Gets the stack sampler for the current thread, creating it if necessary
    """
    try:
        return thread_locals.stack_sampler
    except AttributeError:
        # Attribute 'stack_sampler' doesn't exist in thread_locals, create it
        stack_sampler = StackSampler()
        thread_locals.stack_sampler = None
        return stack_sampler

x_get_stack_sampler__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_stack_sampler__mutmut_1': x_get_stack_sampler__mutmut_1, 
    'x_get_stack_sampler__mutmut_2': x_get_stack_sampler__mutmut_2
}

def get_stack_sampler(*args, **kwargs):
    result = _mutmut_trampoline(x_get_stack_sampler__mutmut_orig, x_get_stack_sampler__mutmut_mutants, args, kwargs)
    return result 

get_stack_sampler.__signature__ = _mutmut_signature(x_get_stack_sampler__mutmut_orig)
x_get_stack_sampler__mutmut_orig.__name__ = 'x_get_stack_sampler'


def x_build_call_stack__mutmut_orig(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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


def x_build_call_stack__mutmut_1(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = None

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


def x_build_call_stack__mutmut_2(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event != "call":
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


def x_build_call_stack__mutmut_3(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "XXcallXX":
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


def x_build_call_stack__mutmut_4(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "CALL":
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


def x_build_call_stack__mutmut_5(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = None
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


def x_build_call_stack__mutmut_6(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" and event == "c_exception":
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


def x_build_call_stack__mutmut_7(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event != "c_return" or event == "c_exception":
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


def x_build_call_stack__mutmut_8(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "XXc_returnXX" or event == "c_exception":
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


def x_build_call_stack__mutmut_9(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "C_RETURN" or event == "c_exception":
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


def x_build_call_stack__mutmut_10(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event != "c_exception":
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


def x_build_call_stack__mutmut_11(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "XXc_exceptionXX":
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


def x_build_call_stack__mutmut_12(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "C_EXCEPTION":
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


def x_build_call_stack__mutmut_13(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "c_exception":
        # if we're exiting a C function, we should add a frame before
        # any Python frames that attributes the time to that C function
        c_frame_identifier = None
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


def x_build_call_stack__mutmut_14(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "c_exception":
        # if we're exiting a C function, we should add a frame before
        # any Python frames that attributes the time to that C function
        c_frame_identifier = "%s\x00%s\x00%i" / (
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


def x_build_call_stack__mutmut_15(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "c_exception":
        # if we're exiting a C function, we should add a frame before
        # any Python frames that attributes the time to that C function
        c_frame_identifier = "XX%s\x00%s\x00%iXX" % (
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


def x_build_call_stack__mutmut_16(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "c_exception":
        # if we're exiting a C function, we should add a frame before
        # any Python frames that attributes the time to that C function
        c_frame_identifier = "%S\x00%S\x00%I" % (
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


def x_build_call_stack__mutmut_17(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "c_exception":
        # if we're exiting a C function, we should add a frame before
        # any Python frames that attributes the time to that C function
        c_frame_identifier = "%s\x00%s\x00%i" % (
            getattr(None, "__qualname__", arg.__name__),
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


def x_build_call_stack__mutmut_18(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "c_exception":
        # if we're exiting a C function, we should add a frame before
        # any Python frames that attributes the time to that C function
        c_frame_identifier = "%s\x00%s\x00%i" % (
            getattr(arg, None, arg.__name__),
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


def x_build_call_stack__mutmut_19(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "c_exception":
        # if we're exiting a C function, we should add a frame before
        # any Python frames that attributes the time to that C function
        c_frame_identifier = "%s\x00%s\x00%i" % (
            getattr(arg, "__qualname__", None),
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


def x_build_call_stack__mutmut_20(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "c_exception":
        # if we're exiting a C function, we should add a frame before
        # any Python frames that attributes the time to that C function
        c_frame_identifier = "%s\x00%s\x00%i" % (
            getattr("__qualname__", arg.__name__),
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


def x_build_call_stack__mutmut_21(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "c_exception":
        # if we're exiting a C function, we should add a frame before
        # any Python frames that attributes the time to that C function
        c_frame_identifier = "%s\x00%s\x00%i" % (
            getattr(arg, arg.__name__),
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


def x_build_call_stack__mutmut_22(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "c_exception":
        # if we're exiting a C function, we should add a frame before
        # any Python frames that attributes the time to that C function
        c_frame_identifier = "%s\x00%s\x00%i" % (
            getattr(arg, "__qualname__", ),
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


def x_build_call_stack__mutmut_23(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "c_exception":
        # if we're exiting a C function, we should add a frame before
        # any Python frames that attributes the time to that C function
        c_frame_identifier = "%s\x00%s\x00%i" % (
            getattr(arg, "XX__qualname__XX", arg.__name__),
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


def x_build_call_stack__mutmut_24(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
    call_stack: list[str] = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back if frame else None
    elif event == "c_return" or event == "c_exception":
        # if we're exiting a C function, we should add a frame before
        # any Python frames that attributes the time to that C function
        c_frame_identifier = "%s\x00%s\x00%i" % (
            getattr(arg, "__QUALNAME__", arg.__name__),
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


def x_build_call_stack__mutmut_25(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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
            "XX<built-in>XX",
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


def x_build_call_stack__mutmut_26(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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
            "<BUILT-IN>",
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


def x_build_call_stack__mutmut_27(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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
            1,
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


def x_build_call_stack__mutmut_28(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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
        call_stack.append(None)

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


def x_build_call_stack__mutmut_29(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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

    while frame is None:
        call_stack.append(get_frame_info(frame))
        frame = frame.f_back

    thread = threading.current_thread()
    thread_identifier = "%s\x00%s\x00%i" % (thread.name, "<thread>", thread.ident)
    call_stack.append(thread_identifier)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack


def x_build_call_stack__mutmut_30(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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
        call_stack.append(None)
        frame = frame.f_back

    thread = threading.current_thread()
    thread_identifier = "%s\x00%s\x00%i" % (thread.name, "<thread>", thread.ident)
    call_stack.append(thread_identifier)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack


def x_build_call_stack__mutmut_31(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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
        call_stack.append(get_frame_info(None))
        frame = frame.f_back

    thread = threading.current_thread()
    thread_identifier = "%s\x00%s\x00%i" % (thread.name, "<thread>", thread.ident)
    call_stack.append(thread_identifier)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack


def x_build_call_stack__mutmut_32(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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
        frame = None

    thread = threading.current_thread()
    thread_identifier = "%s\x00%s\x00%i" % (thread.name, "<thread>", thread.ident)
    call_stack.append(thread_identifier)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack


def x_build_call_stack__mutmut_33(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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

    thread = None
    thread_identifier = "%s\x00%s\x00%i" % (thread.name, "<thread>", thread.ident)
    call_stack.append(thread_identifier)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack


def x_build_call_stack__mutmut_34(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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
    thread_identifier = None
    call_stack.append(thread_identifier)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack


def x_build_call_stack__mutmut_35(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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
    thread_identifier = "%s\x00%s\x00%i" / (thread.name, "<thread>", thread.ident)
    call_stack.append(thread_identifier)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack


def x_build_call_stack__mutmut_36(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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
    thread_identifier = "XX%s\x00%s\x00%iXX" % (thread.name, "<thread>", thread.ident)
    call_stack.append(thread_identifier)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack


def x_build_call_stack__mutmut_37(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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
    thread_identifier = "%S\x00%S\x00%I" % (thread.name, "<thread>", thread.ident)
    call_stack.append(thread_identifier)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack


def x_build_call_stack__mutmut_38(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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
    thread_identifier = "%s\x00%s\x00%i" % (thread.name, "XX<thread>XX", thread.ident)
    call_stack.append(thread_identifier)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack


def x_build_call_stack__mutmut_39(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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
    thread_identifier = "%s\x00%s\x00%i" % (thread.name, "<THREAD>", thread.ident)
    call_stack.append(thread_identifier)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack


def x_build_call_stack__mutmut_40(frame: types.FrameType | None, event: str, arg: Any) -> list[str]:
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
    call_stack.append(None)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack

x_build_call_stack__mutmut_mutants : ClassVar[MutantDict] = {
'x_build_call_stack__mutmut_1': x_build_call_stack__mutmut_1, 
    'x_build_call_stack__mutmut_2': x_build_call_stack__mutmut_2, 
    'x_build_call_stack__mutmut_3': x_build_call_stack__mutmut_3, 
    'x_build_call_stack__mutmut_4': x_build_call_stack__mutmut_4, 
    'x_build_call_stack__mutmut_5': x_build_call_stack__mutmut_5, 
    'x_build_call_stack__mutmut_6': x_build_call_stack__mutmut_6, 
    'x_build_call_stack__mutmut_7': x_build_call_stack__mutmut_7, 
    'x_build_call_stack__mutmut_8': x_build_call_stack__mutmut_8, 
    'x_build_call_stack__mutmut_9': x_build_call_stack__mutmut_9, 
    'x_build_call_stack__mutmut_10': x_build_call_stack__mutmut_10, 
    'x_build_call_stack__mutmut_11': x_build_call_stack__mutmut_11, 
    'x_build_call_stack__mutmut_12': x_build_call_stack__mutmut_12, 
    'x_build_call_stack__mutmut_13': x_build_call_stack__mutmut_13, 
    'x_build_call_stack__mutmut_14': x_build_call_stack__mutmut_14, 
    'x_build_call_stack__mutmut_15': x_build_call_stack__mutmut_15, 
    'x_build_call_stack__mutmut_16': x_build_call_stack__mutmut_16, 
    'x_build_call_stack__mutmut_17': x_build_call_stack__mutmut_17, 
    'x_build_call_stack__mutmut_18': x_build_call_stack__mutmut_18, 
    'x_build_call_stack__mutmut_19': x_build_call_stack__mutmut_19, 
    'x_build_call_stack__mutmut_20': x_build_call_stack__mutmut_20, 
    'x_build_call_stack__mutmut_21': x_build_call_stack__mutmut_21, 
    'x_build_call_stack__mutmut_22': x_build_call_stack__mutmut_22, 
    'x_build_call_stack__mutmut_23': x_build_call_stack__mutmut_23, 
    'x_build_call_stack__mutmut_24': x_build_call_stack__mutmut_24, 
    'x_build_call_stack__mutmut_25': x_build_call_stack__mutmut_25, 
    'x_build_call_stack__mutmut_26': x_build_call_stack__mutmut_26, 
    'x_build_call_stack__mutmut_27': x_build_call_stack__mutmut_27, 
    'x_build_call_stack__mutmut_28': x_build_call_stack__mutmut_28, 
    'x_build_call_stack__mutmut_29': x_build_call_stack__mutmut_29, 
    'x_build_call_stack__mutmut_30': x_build_call_stack__mutmut_30, 
    'x_build_call_stack__mutmut_31': x_build_call_stack__mutmut_31, 
    'x_build_call_stack__mutmut_32': x_build_call_stack__mutmut_32, 
    'x_build_call_stack__mutmut_33': x_build_call_stack__mutmut_33, 
    'x_build_call_stack__mutmut_34': x_build_call_stack__mutmut_34, 
    'x_build_call_stack__mutmut_35': x_build_call_stack__mutmut_35, 
    'x_build_call_stack__mutmut_36': x_build_call_stack__mutmut_36, 
    'x_build_call_stack__mutmut_37': x_build_call_stack__mutmut_37, 
    'x_build_call_stack__mutmut_38': x_build_call_stack__mutmut_38, 
    'x_build_call_stack__mutmut_39': x_build_call_stack__mutmut_39, 
    'x_build_call_stack__mutmut_40': x_build_call_stack__mutmut_40
}

def build_call_stack(*args, **kwargs):
    result = _mutmut_trampoline(x_build_call_stack__mutmut_orig, x_build_call_stack__mutmut_mutants, args, kwargs)
    return result 

build_call_stack.__signature__ = _mutmut_signature(x_build_call_stack__mutmut_orig)
x_build_call_stack__mutmut_orig.__name__ = 'x_build_call_stack'


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


_timing_overhead: dict[TimerType, float] | None = None


def x_timing_overhead__mutmut_orig() -> dict[TimerType, float]:
    global _timing_overhead
    if _timing_overhead is None:
        _timing_overhead = measure_timing_overhead()
    return _timing_overhead


def x_timing_overhead__mutmut_1() -> dict[TimerType, float]:
    global _timing_overhead
    if _timing_overhead is not None:
        _timing_overhead = measure_timing_overhead()
    return _timing_overhead


def x_timing_overhead__mutmut_2() -> dict[TimerType, float]:
    global _timing_overhead
    if _timing_overhead is None:
        _timing_overhead = None
    return _timing_overhead

x_timing_overhead__mutmut_mutants : ClassVar[MutantDict] = {
'x_timing_overhead__mutmut_1': x_timing_overhead__mutmut_1, 
    'x_timing_overhead__mutmut_2': x_timing_overhead__mutmut_2
}

def timing_overhead(*args, **kwargs):
    result = _mutmut_trampoline(x_timing_overhead__mutmut_orig, x_timing_overhead__mutmut_mutants, args, kwargs)
    return result 

timing_overhead.__signature__ = _mutmut_signature(x_timing_overhead__mutmut_orig)
x_timing_overhead__mutmut_orig.__name__ = 'x_timing_overhead'
