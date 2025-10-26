from __future__ import annotations

import inspect
import os
import sys
import time
import types
from pathlib import Path
from time import process_time
from typing import IO, Any

from pyinstrument import renderers
from pyinstrument.frame import AWAIT_FRAME_IDENTIFIER, OUT_OF_CONTEXT_FRAME_IDENTIFIER
from pyinstrument.renderers.console import FlatTimeMode
from pyinstrument.session import Session
from pyinstrument.stack_sampler import AsyncState, StackSampler, build_call_stack, get_stack_sampler
from pyinstrument.typing import LiteralStr, TypeAlias
from pyinstrument.util import file_supports_color, file_supports_unicode
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

# pyright: strict


class ActiveProfilerSession:
    frame_records: list[tuple[list[str], float]]

    def xǁActiveProfilerSessionǁ__init____mutmut_orig(
        self,
        start_time: float,
        start_process_time: float,
        start_call_stack: list[str],
        target_description: str,
        interval: float,
    ) -> None:
        self.start_time = start_time
        self.start_process_time = start_process_time
        self.start_call_stack = start_call_stack
        self.frame_records = []
        self.target_description = target_description
        self.interval = interval

    def xǁActiveProfilerSessionǁ__init____mutmut_1(
        self,
        start_time: float,
        start_process_time: float,
        start_call_stack: list[str],
        target_description: str,
        interval: float,
    ) -> None:
        self.start_time = None
        self.start_process_time = start_process_time
        self.start_call_stack = start_call_stack
        self.frame_records = []
        self.target_description = target_description
        self.interval = interval

    def xǁActiveProfilerSessionǁ__init____mutmut_2(
        self,
        start_time: float,
        start_process_time: float,
        start_call_stack: list[str],
        target_description: str,
        interval: float,
    ) -> None:
        self.start_time = start_time
        self.start_process_time = None
        self.start_call_stack = start_call_stack
        self.frame_records = []
        self.target_description = target_description
        self.interval = interval

    def xǁActiveProfilerSessionǁ__init____mutmut_3(
        self,
        start_time: float,
        start_process_time: float,
        start_call_stack: list[str],
        target_description: str,
        interval: float,
    ) -> None:
        self.start_time = start_time
        self.start_process_time = start_process_time
        self.start_call_stack = None
        self.frame_records = []
        self.target_description = target_description
        self.interval = interval

    def xǁActiveProfilerSessionǁ__init____mutmut_4(
        self,
        start_time: float,
        start_process_time: float,
        start_call_stack: list[str],
        target_description: str,
        interval: float,
    ) -> None:
        self.start_time = start_time
        self.start_process_time = start_process_time
        self.start_call_stack = start_call_stack
        self.frame_records = None
        self.target_description = target_description
        self.interval = interval

    def xǁActiveProfilerSessionǁ__init____mutmut_5(
        self,
        start_time: float,
        start_process_time: float,
        start_call_stack: list[str],
        target_description: str,
        interval: float,
    ) -> None:
        self.start_time = start_time
        self.start_process_time = start_process_time
        self.start_call_stack = start_call_stack
        self.frame_records = []
        self.target_description = None
        self.interval = interval

    def xǁActiveProfilerSessionǁ__init____mutmut_6(
        self,
        start_time: float,
        start_process_time: float,
        start_call_stack: list[str],
        target_description: str,
        interval: float,
    ) -> None:
        self.start_time = start_time
        self.start_process_time = start_process_time
        self.start_call_stack = start_call_stack
        self.frame_records = []
        self.target_description = target_description
        self.interval = None
    
    xǁActiveProfilerSessionǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁActiveProfilerSessionǁ__init____mutmut_1': xǁActiveProfilerSessionǁ__init____mutmut_1, 
        'xǁActiveProfilerSessionǁ__init____mutmut_2': xǁActiveProfilerSessionǁ__init____mutmut_2, 
        'xǁActiveProfilerSessionǁ__init____mutmut_3': xǁActiveProfilerSessionǁ__init____mutmut_3, 
        'xǁActiveProfilerSessionǁ__init____mutmut_4': xǁActiveProfilerSessionǁ__init____mutmut_4, 
        'xǁActiveProfilerSessionǁ__init____mutmut_5': xǁActiveProfilerSessionǁ__init____mutmut_5, 
        'xǁActiveProfilerSessionǁ__init____mutmut_6': xǁActiveProfilerSessionǁ__init____mutmut_6
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁActiveProfilerSessionǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁActiveProfilerSessionǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁActiveProfilerSessionǁ__init____mutmut_orig)
    xǁActiveProfilerSessionǁ__init____mutmut_orig.__name__ = 'xǁActiveProfilerSessionǁ__init__'


AsyncMode: TypeAlias = LiteralStr["enabled", "disabled", "strict"]


class Profiler:
    """
    The profiler - this is the main way to use pyinstrument.
    """

    _last_session: Session | None
    _active_session: ActiveProfilerSession | None
    _interval: float
    _async_mode: AsyncMode
    use_timing_thread: bool | None

    def xǁProfilerǁ__init____mutmut_orig(
        self,
        interval: float = 0.001,
        async_mode: AsyncMode = "enabled",
        use_timing_thread: bool | None = None,
    ):
        """
        Note the profiling will not start until :func:`start` is called.

        :param interval: See :attr:`interval`.
        :param async_mode: See :attr:`async_mode`.
        :param use_timing_thread: If True, the profiler will use a separate
            thread to keep track of time. This is useful if you're on a system
            where getting the time has significant overhead.
        """
        self._interval = interval
        self._last_session = None
        self._active_session = None
        self._async_mode = async_mode
        self.use_timing_thread = use_timing_thread

    def xǁProfilerǁ__init____mutmut_1(
        self,
        interval: float = 1.001,
        async_mode: AsyncMode = "enabled",
        use_timing_thread: bool | None = None,
    ):
        """
        Note the profiling will not start until :func:`start` is called.

        :param interval: See :attr:`interval`.
        :param async_mode: See :attr:`async_mode`.
        :param use_timing_thread: If True, the profiler will use a separate
            thread to keep track of time. This is useful if you're on a system
            where getting the time has significant overhead.
        """
        self._interval = interval
        self._last_session = None
        self._active_session = None
        self._async_mode = async_mode
        self.use_timing_thread = use_timing_thread

    def xǁProfilerǁ__init____mutmut_2(
        self,
        interval: float = 0.001,
        async_mode: AsyncMode = "XXenabledXX",
        use_timing_thread: bool | None = None,
    ):
        """
        Note the profiling will not start until :func:`start` is called.

        :param interval: See :attr:`interval`.
        :param async_mode: See :attr:`async_mode`.
        :param use_timing_thread: If True, the profiler will use a separate
            thread to keep track of time. This is useful if you're on a system
            where getting the time has significant overhead.
        """
        self._interval = interval
        self._last_session = None
        self._active_session = None
        self._async_mode = async_mode
        self.use_timing_thread = use_timing_thread

    def xǁProfilerǁ__init____mutmut_3(
        self,
        interval: float = 0.001,
        async_mode: AsyncMode = "ENABLED",
        use_timing_thread: bool | None = None,
    ):
        """
        Note the profiling will not start until :func:`start` is called.

        :param interval: See :attr:`interval`.
        :param async_mode: See :attr:`async_mode`.
        :param use_timing_thread: If True, the profiler will use a separate
            thread to keep track of time. This is useful if you're on a system
            where getting the time has significant overhead.
        """
        self._interval = interval
        self._last_session = None
        self._active_session = None
        self._async_mode = async_mode
        self.use_timing_thread = use_timing_thread

    def xǁProfilerǁ__init____mutmut_4(
        self,
        interval: float = 0.001,
        async_mode: AsyncMode = "enabled",
        use_timing_thread: bool | None = None,
    ):
        """
        Note the profiling will not start until :func:`start` is called.

        :param interval: See :attr:`interval`.
        :param async_mode: See :attr:`async_mode`.
        :param use_timing_thread: If True, the profiler will use a separate
            thread to keep track of time. This is useful if you're on a system
            where getting the time has significant overhead.
        """
        self._interval = None
        self._last_session = None
        self._active_session = None
        self._async_mode = async_mode
        self.use_timing_thread = use_timing_thread

    def xǁProfilerǁ__init____mutmut_5(
        self,
        interval: float = 0.001,
        async_mode: AsyncMode = "enabled",
        use_timing_thread: bool | None = None,
    ):
        """
        Note the profiling will not start until :func:`start` is called.

        :param interval: See :attr:`interval`.
        :param async_mode: See :attr:`async_mode`.
        :param use_timing_thread: If True, the profiler will use a separate
            thread to keep track of time. This is useful if you're on a system
            where getting the time has significant overhead.
        """
        self._interval = interval
        self._last_session = ""
        self._active_session = None
        self._async_mode = async_mode
        self.use_timing_thread = use_timing_thread

    def xǁProfilerǁ__init____mutmut_6(
        self,
        interval: float = 0.001,
        async_mode: AsyncMode = "enabled",
        use_timing_thread: bool | None = None,
    ):
        """
        Note the profiling will not start until :func:`start` is called.

        :param interval: See :attr:`interval`.
        :param async_mode: See :attr:`async_mode`.
        :param use_timing_thread: If True, the profiler will use a separate
            thread to keep track of time. This is useful if you're on a system
            where getting the time has significant overhead.
        """
        self._interval = interval
        self._last_session = None
        self._active_session = ""
        self._async_mode = async_mode
        self.use_timing_thread = use_timing_thread

    def xǁProfilerǁ__init____mutmut_7(
        self,
        interval: float = 0.001,
        async_mode: AsyncMode = "enabled",
        use_timing_thread: bool | None = None,
    ):
        """
        Note the profiling will not start until :func:`start` is called.

        :param interval: See :attr:`interval`.
        :param async_mode: See :attr:`async_mode`.
        :param use_timing_thread: If True, the profiler will use a separate
            thread to keep track of time. This is useful if you're on a system
            where getting the time has significant overhead.
        """
        self._interval = interval
        self._last_session = None
        self._active_session = None
        self._async_mode = None
        self.use_timing_thread = use_timing_thread

    def xǁProfilerǁ__init____mutmut_8(
        self,
        interval: float = 0.001,
        async_mode: AsyncMode = "enabled",
        use_timing_thread: bool | None = None,
    ):
        """
        Note the profiling will not start until :func:`start` is called.

        :param interval: See :attr:`interval`.
        :param async_mode: See :attr:`async_mode`.
        :param use_timing_thread: If True, the profiler will use a separate
            thread to keep track of time. This is useful if you're on a system
            where getting the time has significant overhead.
        """
        self._interval = interval
        self._last_session = None
        self._active_session = None
        self._async_mode = async_mode
        self.use_timing_thread = None
    
    xǁProfilerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerǁ__init____mutmut_1': xǁProfilerǁ__init____mutmut_1, 
        'xǁProfilerǁ__init____mutmut_2': xǁProfilerǁ__init____mutmut_2, 
        'xǁProfilerǁ__init____mutmut_3': xǁProfilerǁ__init____mutmut_3, 
        'xǁProfilerǁ__init____mutmut_4': xǁProfilerǁ__init____mutmut_4, 
        'xǁProfilerǁ__init____mutmut_5': xǁProfilerǁ__init____mutmut_5, 
        'xǁProfilerǁ__init____mutmut_6': xǁProfilerǁ__init____mutmut_6, 
        'xǁProfilerǁ__init____mutmut_7': xǁProfilerǁ__init____mutmut_7, 
        'xǁProfilerǁ__init____mutmut_8': xǁProfilerǁ__init____mutmut_8
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁProfilerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁProfilerǁ__init____mutmut_orig)
    xǁProfilerǁ__init____mutmut_orig.__name__ = 'xǁProfilerǁ__init__'

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

    def xǁProfilerǁstart__mutmut_orig(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_1(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if caller_frame is not None:
            caller_frame = inspect.currentframe().f_back  # type: ignore

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_2(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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
            caller_frame = None  # type: ignore

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_3(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is not None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_4(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is not None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_5(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = None
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_6(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "XXProfile at unknown locationXX"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_7(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_8(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "PROFILE AT UNKNOWN LOCATION"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_9(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = None

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_10(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    None, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_11(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, None
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_12(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_13(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_14(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "XXProfile at {}:{}XX".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_15(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_16(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "PROFILE AT {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_17(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = None

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_18(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=None,
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_19(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=None,
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_20(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=None,
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_21(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=None,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_22(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=None,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_23(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_24(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_25(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_26(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_27(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_28(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(None, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_29(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, None, None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_30(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack("initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_31(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_32(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", ),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_33(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "XXinitialXX", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_34(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "INITIAL", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_35(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = None
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_36(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode == "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_37(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "XXdisabledXX"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_38(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "DISABLED"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_39(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                None,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_40(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=None,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_41(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=None,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_42(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=None,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_43(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_44(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_45(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_46(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                )
        except:
            self._active_session = None
            raise

    def xǁProfilerǁstart__mutmut_47(
        self, caller_frame: types.FrameType | None = None, target_description: str | None = None
    ):
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

        if target_description is None:
            if caller_frame is None:
                target_description = "Profile at unknown location"
            else:
                target_description = "Profile at {}:{}".format(
                    caller_frame.f_code.co_filename, caller_frame.f_lineno
                )

        try:
            self._active_session = ActiveProfilerSession(
                start_time=time.time(),
                start_process_time=process_time(),
                start_call_stack=build_call_stack(caller_frame, "initial", None),
                target_description=target_description,
                interval=self.interval,
            )

            use_async_context = self.async_mode != "disabled"
            get_stack_sampler().subscribe(
                self._sampler_saw_call_stack,
                desired_interval=self.interval,
                use_async_context=use_async_context,
                use_timing_thread=self.use_timing_thread,
            )
        except:
            self._active_session = ""
            raise
    
    xǁProfilerǁstart__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerǁstart__mutmut_1': xǁProfilerǁstart__mutmut_1, 
        'xǁProfilerǁstart__mutmut_2': xǁProfilerǁstart__mutmut_2, 
        'xǁProfilerǁstart__mutmut_3': xǁProfilerǁstart__mutmut_3, 
        'xǁProfilerǁstart__mutmut_4': xǁProfilerǁstart__mutmut_4, 
        'xǁProfilerǁstart__mutmut_5': xǁProfilerǁstart__mutmut_5, 
        'xǁProfilerǁstart__mutmut_6': xǁProfilerǁstart__mutmut_6, 
        'xǁProfilerǁstart__mutmut_7': xǁProfilerǁstart__mutmut_7, 
        'xǁProfilerǁstart__mutmut_8': xǁProfilerǁstart__mutmut_8, 
        'xǁProfilerǁstart__mutmut_9': xǁProfilerǁstart__mutmut_9, 
        'xǁProfilerǁstart__mutmut_10': xǁProfilerǁstart__mutmut_10, 
        'xǁProfilerǁstart__mutmut_11': xǁProfilerǁstart__mutmut_11, 
        'xǁProfilerǁstart__mutmut_12': xǁProfilerǁstart__mutmut_12, 
        'xǁProfilerǁstart__mutmut_13': xǁProfilerǁstart__mutmut_13, 
        'xǁProfilerǁstart__mutmut_14': xǁProfilerǁstart__mutmut_14, 
        'xǁProfilerǁstart__mutmut_15': xǁProfilerǁstart__mutmut_15, 
        'xǁProfilerǁstart__mutmut_16': xǁProfilerǁstart__mutmut_16, 
        'xǁProfilerǁstart__mutmut_17': xǁProfilerǁstart__mutmut_17, 
        'xǁProfilerǁstart__mutmut_18': xǁProfilerǁstart__mutmut_18, 
        'xǁProfilerǁstart__mutmut_19': xǁProfilerǁstart__mutmut_19, 
        'xǁProfilerǁstart__mutmut_20': xǁProfilerǁstart__mutmut_20, 
        'xǁProfilerǁstart__mutmut_21': xǁProfilerǁstart__mutmut_21, 
        'xǁProfilerǁstart__mutmut_22': xǁProfilerǁstart__mutmut_22, 
        'xǁProfilerǁstart__mutmut_23': xǁProfilerǁstart__mutmut_23, 
        'xǁProfilerǁstart__mutmut_24': xǁProfilerǁstart__mutmut_24, 
        'xǁProfilerǁstart__mutmut_25': xǁProfilerǁstart__mutmut_25, 
        'xǁProfilerǁstart__mutmut_26': xǁProfilerǁstart__mutmut_26, 
        'xǁProfilerǁstart__mutmut_27': xǁProfilerǁstart__mutmut_27, 
        'xǁProfilerǁstart__mutmut_28': xǁProfilerǁstart__mutmut_28, 
        'xǁProfilerǁstart__mutmut_29': xǁProfilerǁstart__mutmut_29, 
        'xǁProfilerǁstart__mutmut_30': xǁProfilerǁstart__mutmut_30, 
        'xǁProfilerǁstart__mutmut_31': xǁProfilerǁstart__mutmut_31, 
        'xǁProfilerǁstart__mutmut_32': xǁProfilerǁstart__mutmut_32, 
        'xǁProfilerǁstart__mutmut_33': xǁProfilerǁstart__mutmut_33, 
        'xǁProfilerǁstart__mutmut_34': xǁProfilerǁstart__mutmut_34, 
        'xǁProfilerǁstart__mutmut_35': xǁProfilerǁstart__mutmut_35, 
        'xǁProfilerǁstart__mutmut_36': xǁProfilerǁstart__mutmut_36, 
        'xǁProfilerǁstart__mutmut_37': xǁProfilerǁstart__mutmut_37, 
        'xǁProfilerǁstart__mutmut_38': xǁProfilerǁstart__mutmut_38, 
        'xǁProfilerǁstart__mutmut_39': xǁProfilerǁstart__mutmut_39, 
        'xǁProfilerǁstart__mutmut_40': xǁProfilerǁstart__mutmut_40, 
        'xǁProfilerǁstart__mutmut_41': xǁProfilerǁstart__mutmut_41, 
        'xǁProfilerǁstart__mutmut_42': xǁProfilerǁstart__mutmut_42, 
        'xǁProfilerǁstart__mutmut_43': xǁProfilerǁstart__mutmut_43, 
        'xǁProfilerǁstart__mutmut_44': xǁProfilerǁstart__mutmut_44, 
        'xǁProfilerǁstart__mutmut_45': xǁProfilerǁstart__mutmut_45, 
        'xǁProfilerǁstart__mutmut_46': xǁProfilerǁstart__mutmut_46, 
        'xǁProfilerǁstart__mutmut_47': xǁProfilerǁstart__mutmut_47
    }
    
    def start(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerǁstart__mutmut_orig"), object.__getattribute__(self, "xǁProfilerǁstart__mutmut_mutants"), args, kwargs, self)
        return result 
    
    start.__signature__ = _mutmut_signature(xǁProfilerǁstart__mutmut_orig)
    xǁProfilerǁstart__mutmut_orig.__name__ = 'xǁProfilerǁstart'

    def xǁProfilerǁstop__mutmut_orig(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_1(self) -> Session:
        """
        Stops the profiler observing, and sets :attr:`last_session`
        to the captured session.

        :return: The captured session.
        """
        if self._active_session:
            raise RuntimeError("This profiler is not currently running.")

        try:
            get_stack_sampler().unsubscribe(self._sampler_saw_call_stack)
        except StackSampler.SubscriberNotFound:
            raise RuntimeError(
                "Failed to stop profiling. Make sure that you start/stop profiling on the same thread."
            )

        cpu_time = process_time() - self._active_session.start_process_time

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_2(self) -> Session:
        """
        Stops the profiler observing, and sets :attr:`last_session`
        to the captured session.

        :return: The captured session.
        """
        if not self._active_session:
            raise RuntimeError(None)

        try:
            get_stack_sampler().unsubscribe(self._sampler_saw_call_stack)
        except StackSampler.SubscriberNotFound:
            raise RuntimeError(
                "Failed to stop profiling. Make sure that you start/stop profiling on the same thread."
            )

        cpu_time = process_time() - self._active_session.start_process_time

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_3(self) -> Session:
        """
        Stops the profiler observing, and sets :attr:`last_session`
        to the captured session.

        :return: The captured session.
        """
        if not self._active_session:
            raise RuntimeError("XXThis profiler is not currently running.XX")

        try:
            get_stack_sampler().unsubscribe(self._sampler_saw_call_stack)
        except StackSampler.SubscriberNotFound:
            raise RuntimeError(
                "Failed to stop profiling. Make sure that you start/stop profiling on the same thread."
            )

        cpu_time = process_time() - self._active_session.start_process_time

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_4(self) -> Session:
        """
        Stops the profiler observing, and sets :attr:`last_session`
        to the captured session.

        :return: The captured session.
        """
        if not self._active_session:
            raise RuntimeError("this profiler is not currently running.")

        try:
            get_stack_sampler().unsubscribe(self._sampler_saw_call_stack)
        except StackSampler.SubscriberNotFound:
            raise RuntimeError(
                "Failed to stop profiling. Make sure that you start/stop profiling on the same thread."
            )

        cpu_time = process_time() - self._active_session.start_process_time

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_5(self) -> Session:
        """
        Stops the profiler observing, and sets :attr:`last_session`
        to the captured session.

        :return: The captured session.
        """
        if not self._active_session:
            raise RuntimeError("THIS PROFILER IS NOT CURRENTLY RUNNING.")

        try:
            get_stack_sampler().unsubscribe(self._sampler_saw_call_stack)
        except StackSampler.SubscriberNotFound:
            raise RuntimeError(
                "Failed to stop profiling. Make sure that you start/stop profiling on the same thread."
            )

        cpu_time = process_time() - self._active_session.start_process_time

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_6(self) -> Session:
        """
        Stops the profiler observing, and sets :attr:`last_session`
        to the captured session.

        :return: The captured session.
        """
        if not self._active_session:
            raise RuntimeError("This profiler is not currently running.")

        try:
            get_stack_sampler().unsubscribe(None)
        except StackSampler.SubscriberNotFound:
            raise RuntimeError(
                "Failed to stop profiling. Make sure that you start/stop profiling on the same thread."
            )

        cpu_time = process_time() - self._active_session.start_process_time

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_7(self) -> Session:
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
                None
            )

        cpu_time = process_time() - self._active_session.start_process_time

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_8(self) -> Session:
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
                "XXFailed to stop profiling. Make sure that you start/stop profiling on the same thread.XX"
            )

        cpu_time = process_time() - self._active_session.start_process_time

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_9(self) -> Session:
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
                "failed to stop profiling. make sure that you start/stop profiling on the same thread."
            )

        cpu_time = process_time() - self._active_session.start_process_time

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_10(self) -> Session:
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
                "FAILED TO STOP PROFILING. MAKE SURE THAT YOU START/STOP PROFILING ON THE SAME THREAD."
            )

        cpu_time = process_time() - self._active_session.start_process_time

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_11(self) -> Session:
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

        cpu_time = None

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_12(self) -> Session:
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

        cpu_time = process_time() + self._active_session.start_process_time

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_13(self) -> Session:
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

        active_session = None
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_14(self) -> Session:
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

        active_session = self._active_session
        self._active_session = ""

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_15(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = None

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_16(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=None,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_17(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=None,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_18(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=None,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_19(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=None,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_20(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=None,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_21(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=None,
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_22(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=None,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_23(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=None,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_24(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=None,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_25(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=None,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_26(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=None,
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_27(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_28(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_29(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_30(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_31(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_32(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_33(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_34(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_35(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_36(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_37(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_38(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() + active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_39(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_40(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = None

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_41(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(None, session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_42(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, None)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_43(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(session)

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_44(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, )

        self._last_session = session

        return session

    def xǁProfilerǁstop__mutmut_45(self) -> Session:
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

        active_session = self._active_session
        self._active_session = None

        session = Session(
            frame_records=active_session.frame_records,
            start_time=active_session.start_time,
            duration=time.time() - active_session.start_time,
            min_interval=active_session.interval,
            max_interval=active_session.interval,
            sample_count=len(active_session.frame_records),
            target_description=active_session.target_description,
            start_call_stack=active_session.start_call_stack,
            cpu_time=cpu_time,
            sys_path=sys.path,
            sys_prefixes=Session.current_sys_prefixes(),
        )

        if self.last_session is not None:
            # include the previous session's data too
            session = Session.combine(self.last_session, session)

        self._last_session = None

        return session
    
    xǁProfilerǁstop__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerǁstop__mutmut_1': xǁProfilerǁstop__mutmut_1, 
        'xǁProfilerǁstop__mutmut_2': xǁProfilerǁstop__mutmut_2, 
        'xǁProfilerǁstop__mutmut_3': xǁProfilerǁstop__mutmut_3, 
        'xǁProfilerǁstop__mutmut_4': xǁProfilerǁstop__mutmut_4, 
        'xǁProfilerǁstop__mutmut_5': xǁProfilerǁstop__mutmut_5, 
        'xǁProfilerǁstop__mutmut_6': xǁProfilerǁstop__mutmut_6, 
        'xǁProfilerǁstop__mutmut_7': xǁProfilerǁstop__mutmut_7, 
        'xǁProfilerǁstop__mutmut_8': xǁProfilerǁstop__mutmut_8, 
        'xǁProfilerǁstop__mutmut_9': xǁProfilerǁstop__mutmut_9, 
        'xǁProfilerǁstop__mutmut_10': xǁProfilerǁstop__mutmut_10, 
        'xǁProfilerǁstop__mutmut_11': xǁProfilerǁstop__mutmut_11, 
        'xǁProfilerǁstop__mutmut_12': xǁProfilerǁstop__mutmut_12, 
        'xǁProfilerǁstop__mutmut_13': xǁProfilerǁstop__mutmut_13, 
        'xǁProfilerǁstop__mutmut_14': xǁProfilerǁstop__mutmut_14, 
        'xǁProfilerǁstop__mutmut_15': xǁProfilerǁstop__mutmut_15, 
        'xǁProfilerǁstop__mutmut_16': xǁProfilerǁstop__mutmut_16, 
        'xǁProfilerǁstop__mutmut_17': xǁProfilerǁstop__mutmut_17, 
        'xǁProfilerǁstop__mutmut_18': xǁProfilerǁstop__mutmut_18, 
        'xǁProfilerǁstop__mutmut_19': xǁProfilerǁstop__mutmut_19, 
        'xǁProfilerǁstop__mutmut_20': xǁProfilerǁstop__mutmut_20, 
        'xǁProfilerǁstop__mutmut_21': xǁProfilerǁstop__mutmut_21, 
        'xǁProfilerǁstop__mutmut_22': xǁProfilerǁstop__mutmut_22, 
        'xǁProfilerǁstop__mutmut_23': xǁProfilerǁstop__mutmut_23, 
        'xǁProfilerǁstop__mutmut_24': xǁProfilerǁstop__mutmut_24, 
        'xǁProfilerǁstop__mutmut_25': xǁProfilerǁstop__mutmut_25, 
        'xǁProfilerǁstop__mutmut_26': xǁProfilerǁstop__mutmut_26, 
        'xǁProfilerǁstop__mutmut_27': xǁProfilerǁstop__mutmut_27, 
        'xǁProfilerǁstop__mutmut_28': xǁProfilerǁstop__mutmut_28, 
        'xǁProfilerǁstop__mutmut_29': xǁProfilerǁstop__mutmut_29, 
        'xǁProfilerǁstop__mutmut_30': xǁProfilerǁstop__mutmut_30, 
        'xǁProfilerǁstop__mutmut_31': xǁProfilerǁstop__mutmut_31, 
        'xǁProfilerǁstop__mutmut_32': xǁProfilerǁstop__mutmut_32, 
        'xǁProfilerǁstop__mutmut_33': xǁProfilerǁstop__mutmut_33, 
        'xǁProfilerǁstop__mutmut_34': xǁProfilerǁstop__mutmut_34, 
        'xǁProfilerǁstop__mutmut_35': xǁProfilerǁstop__mutmut_35, 
        'xǁProfilerǁstop__mutmut_36': xǁProfilerǁstop__mutmut_36, 
        'xǁProfilerǁstop__mutmut_37': xǁProfilerǁstop__mutmut_37, 
        'xǁProfilerǁstop__mutmut_38': xǁProfilerǁstop__mutmut_38, 
        'xǁProfilerǁstop__mutmut_39': xǁProfilerǁstop__mutmut_39, 
        'xǁProfilerǁstop__mutmut_40': xǁProfilerǁstop__mutmut_40, 
        'xǁProfilerǁstop__mutmut_41': xǁProfilerǁstop__mutmut_41, 
        'xǁProfilerǁstop__mutmut_42': xǁProfilerǁstop__mutmut_42, 
        'xǁProfilerǁstop__mutmut_43': xǁProfilerǁstop__mutmut_43, 
        'xǁProfilerǁstop__mutmut_44': xǁProfilerǁstop__mutmut_44, 
        'xǁProfilerǁstop__mutmut_45': xǁProfilerǁstop__mutmut_45
    }
    
    def stop(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerǁstop__mutmut_orig"), object.__getattribute__(self, "xǁProfilerǁstop__mutmut_mutants"), args, kwargs, self)
        return result 
    
    stop.__signature__ = _mutmut_signature(xǁProfilerǁstop__mutmut_orig)
    xǁProfilerǁstop__mutmut_orig.__name__ = 'xǁProfilerǁstop'

    @property
    def is_running(self):
        """
        Returns `True` if this profiler is running - i.e. observing the program execution.
        """
        return self._active_session is not None

    def xǁProfilerǁreset__mutmut_orig(self):
        """
        Resets the Profiler, clearing the `last_session`.
        """
        if self.is_running:
            self.stop()

        self._last_session = None

    def xǁProfilerǁreset__mutmut_1(self):
        """
        Resets the Profiler, clearing the `last_session`.
        """
        if self.is_running:
            self.stop()

        self._last_session = ""
    
    xǁProfilerǁreset__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerǁreset__mutmut_1': xǁProfilerǁreset__mutmut_1
    }
    
    def reset(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerǁreset__mutmut_orig"), object.__getattribute__(self, "xǁProfilerǁreset__mutmut_mutants"), args, kwargs, self)
        return result 
    
    reset.__signature__ = _mutmut_signature(xǁProfilerǁreset__mutmut_orig)
    xǁProfilerǁreset__mutmut_orig.__name__ = 'xǁProfilerǁreset'

    def xǁProfilerǁ__enter____mutmut_orig(self):
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

    def xǁProfilerǁ__enter____mutmut_1(self):
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
        self.start(caller_frame=None)  # type: ignore
        return self
    
    xǁProfilerǁ__enter____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerǁ__enter____mutmut_1': xǁProfilerǁ__enter____mutmut_1
    }
    
    def __enter__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerǁ__enter____mutmut_orig"), object.__getattribute__(self, "xǁProfilerǁ__enter____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __enter__.__signature__ = _mutmut_signature(xǁProfilerǁ__enter____mutmut_orig)
    xǁProfilerǁ__enter____mutmut_orig.__name__ = 'xǁProfilerǁ__enter__'

    def __exit__(self, *args: Any):
        self.stop()

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_orig(
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_1(
        self,
        call_stack: list[str],
        time_since_last_sample: float,
        async_state: AsyncState | None,
    ):
        if self._active_session:
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_2(
        self,
        call_stack: list[str],
        time_since_last_sample: float,
        async_state: AsyncState | None,
    ):
        if not self._active_session:
            raise RuntimeError(
                None
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_3(
        self,
        call_stack: list[str],
        time_since_last_sample: float,
        async_state: AsyncState | None,
    ):
        if not self._active_session:
            raise RuntimeError(
                "XXReceived a call stack without an active session. Please file an issue on pyinstrument Github describing how you made this happen!XX"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_4(
        self,
        call_stack: list[str],
        time_since_last_sample: float,
        async_state: AsyncState | None,
    ):
        if not self._active_session:
            raise RuntimeError(
                "received a call stack without an active session. please file an issue on pyinstrument github describing how you made this happen!"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_5(
        self,
        call_stack: list[str],
        time_since_last_sample: float,
        async_state: AsyncState | None,
    ):
        if not self._active_session:
            raise RuntimeError(
                "RECEIVED A CALL STACK WITHOUT AN ACTIVE SESSION. PLEASE FILE AN ISSUE ON PYINSTRUMENT GITHUB DESCRIBING HOW YOU MADE THIS HAPPEN!"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_6(
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
            and async_state.state == "out_of_context_awaited" or self._async_mode in ["enabled", "strict"]
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_7(
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
            async_state or async_state.state == "out_of_context_awaited"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_8(
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
            and async_state.state != "out_of_context_awaited"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_9(
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
            and async_state.state == "XXout_of_context_awaitedXX"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_10(
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
            and async_state.state == "OUT_OF_CONTEXT_AWAITED"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_11(
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
            and self._async_mode not in ["enabled", "strict"]
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_12(
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
            and self._async_mode in ["XXenabledXX", "strict"]
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_13(
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
            and self._async_mode in ["ENABLED", "strict"]
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_14(
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
            and self._async_mode in ["enabled", "XXstrictXX"]
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_15(
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
            and self._async_mode in ["enabled", "STRICT"]
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_16(
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
            awaiting_coroutine_stack = None
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_17(
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
                None
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_18(
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
                    awaiting_coroutine_stack - [AWAIT_FRAME_IDENTIFIER],
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_19(
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
            and async_state.state == "out_of_context_unknown" or self._async_mode == "strict"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_20(
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
            async_state or async_state.state == "out_of_context_unknown"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_21(
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
            and async_state.state != "out_of_context_unknown"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_22(
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
            and async_state.state == "XXout_of_context_unknownXX"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_23(
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
            and async_state.state == "OUT_OF_CONTEXT_UNKNOWN"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_24(
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
            and self._async_mode != "strict"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_25(
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
            and self._async_mode == "XXstrictXX"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_26(
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
            and self._async_mode == "STRICT"
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

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_27(
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
            context_exit_frame = None
            self._active_session.frame_records.append(
                (
                    context_exit_frame + [OUT_OF_CONTEXT_FRAME_IDENTIFIER],
                    time_since_last_sample,
                )
            )
        else:
            # regular sync code
            self._active_session.frame_records.append((call_stack, time_since_last_sample))

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_28(
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
                None
            )
        else:
            # regular sync code
            self._active_session.frame_records.append((call_stack, time_since_last_sample))

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_29(
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
                    context_exit_frame - [OUT_OF_CONTEXT_FRAME_IDENTIFIER],
                    time_since_last_sample,
                )
            )
        else:
            # regular sync code
            self._active_session.frame_records.append((call_stack, time_since_last_sample))

    # pylint: disable=W0613
    def xǁProfilerǁ_sampler_saw_call_stack__mutmut_30(
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
            self._active_session.frame_records.append(None)
    
    xǁProfilerǁ_sampler_saw_call_stack__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerǁ_sampler_saw_call_stack__mutmut_1': xǁProfilerǁ_sampler_saw_call_stack__mutmut_1, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_2': xǁProfilerǁ_sampler_saw_call_stack__mutmut_2, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_3': xǁProfilerǁ_sampler_saw_call_stack__mutmut_3, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_4': xǁProfilerǁ_sampler_saw_call_stack__mutmut_4, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_5': xǁProfilerǁ_sampler_saw_call_stack__mutmut_5, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_6': xǁProfilerǁ_sampler_saw_call_stack__mutmut_6, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_7': xǁProfilerǁ_sampler_saw_call_stack__mutmut_7, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_8': xǁProfilerǁ_sampler_saw_call_stack__mutmut_8, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_9': xǁProfilerǁ_sampler_saw_call_stack__mutmut_9, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_10': xǁProfilerǁ_sampler_saw_call_stack__mutmut_10, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_11': xǁProfilerǁ_sampler_saw_call_stack__mutmut_11, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_12': xǁProfilerǁ_sampler_saw_call_stack__mutmut_12, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_13': xǁProfilerǁ_sampler_saw_call_stack__mutmut_13, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_14': xǁProfilerǁ_sampler_saw_call_stack__mutmut_14, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_15': xǁProfilerǁ_sampler_saw_call_stack__mutmut_15, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_16': xǁProfilerǁ_sampler_saw_call_stack__mutmut_16, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_17': xǁProfilerǁ_sampler_saw_call_stack__mutmut_17, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_18': xǁProfilerǁ_sampler_saw_call_stack__mutmut_18, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_19': xǁProfilerǁ_sampler_saw_call_stack__mutmut_19, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_20': xǁProfilerǁ_sampler_saw_call_stack__mutmut_20, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_21': xǁProfilerǁ_sampler_saw_call_stack__mutmut_21, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_22': xǁProfilerǁ_sampler_saw_call_stack__mutmut_22, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_23': xǁProfilerǁ_sampler_saw_call_stack__mutmut_23, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_24': xǁProfilerǁ_sampler_saw_call_stack__mutmut_24, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_25': xǁProfilerǁ_sampler_saw_call_stack__mutmut_25, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_26': xǁProfilerǁ_sampler_saw_call_stack__mutmut_26, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_27': xǁProfilerǁ_sampler_saw_call_stack__mutmut_27, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_28': xǁProfilerǁ_sampler_saw_call_stack__mutmut_28, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_29': xǁProfilerǁ_sampler_saw_call_stack__mutmut_29, 
        'xǁProfilerǁ_sampler_saw_call_stack__mutmut_30': xǁProfilerǁ_sampler_saw_call_stack__mutmut_30
    }
    
    def _sampler_saw_call_stack(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerǁ_sampler_saw_call_stack__mutmut_orig"), object.__getattribute__(self, "xǁProfilerǁ_sampler_saw_call_stack__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _sampler_saw_call_stack.__signature__ = _mutmut_signature(xǁProfilerǁ_sampler_saw_call_stack__mutmut_orig)
    xǁProfilerǁ_sampler_saw_call_stack__mutmut_orig.__name__ = 'xǁProfilerǁ_sampler_saw_call_stack'

    def xǁProfilerǁprint__mutmut_orig(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_1(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = True,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_2(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = True,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_3(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "XXsecondsXX",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_4(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "SECONDS",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_5(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = True,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_6(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "XXselfXX",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_7(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "SELF",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_8(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = True,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_9(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
        """
        if unicode is not None:
            unicode = file_supports_unicode(file)
        if color is None:
            color = file_supports_color(file)

        print(
            self.output_text(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_10(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
        """
        if unicode is None:
            unicode = None
        if color is None:
            color = file_supports_color(file)

        print(
            self.output_text(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_11(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
        """
        if unicode is None:
            unicode = file_supports_unicode(None)
        if color is None:
            color = file_supports_color(file)

        print(
            self.output_text(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_12(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
        """
        if unicode is None:
            unicode = file_supports_unicode(file)
        if color is not None:
            color = file_supports_color(file)

        print(
            self.output_text(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_13(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
        """
        if unicode is None:
            unicode = file_supports_unicode(file)
        if color is None:
            color = None

        print(
            self.output_text(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_14(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
        """
        if unicode is None:
            unicode = file_supports_unicode(file)
        if color is None:
            color = file_supports_color(None)

        print(
            self.output_text(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_15(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
        """
        if unicode is None:
            unicode = file_supports_unicode(file)
        if color is None:
            color = file_supports_color(file)

        print(
            None,
            file=file,
        )

    def xǁProfilerǁprint__mutmut_16(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=None,
        )

    def xǁProfilerǁprint__mutmut_17(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
        """
        if unicode is None:
            unicode = file_supports_unicode(file)
        if color is None:
            color = file_supports_color(file)

        print(
            file=file,
        )

    def xǁProfilerǁprint__mutmut_18(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            )

    def xǁProfilerǁprint__mutmut_19(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
        """
        if unicode is None:
            unicode = file_supports_unicode(file)
        if color is None:
            color = file_supports_color(file)

        print(
            self.output_text(
                unicode=None,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_20(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
        """
        if unicode is None:
            unicode = file_supports_unicode(file)
        if color is None:
            color = file_supports_color(file)

        print(
            self.output_text(
                unicode=unicode,
                color=None,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_21(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
        """
        if unicode is None:
            unicode = file_supports_unicode(file)
        if color is None:
            color = file_supports_color(file)

        print(
            self.output_text(
                unicode=unicode,
                color=color,
                show_all=None,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_22(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                timeline=None,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_23(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=None,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_24(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=None,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_25(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=None,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_26(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=None,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_27(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=None,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_28(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
        """
        if unicode is None:
            unicode = file_supports_unicode(file)
        if color is None:
            color = file_supports_color(file)

        print(
            self.output_text(
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_29(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
        """
        if unicode is None:
            unicode = file_supports_unicode(file)
        if color is None:
            color = file_supports_color(file)

        print(
            self.output_text(
                unicode=unicode,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_30(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
        """
        if unicode is None:
            unicode = file_supports_unicode(file)
        if color is None:
            color = file_supports_color(file)

        print(
            self.output_text(
                unicode=unicode,
                color=color,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_31(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_32(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_33(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_34(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                short_mode=short_mode,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_35(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                processor_options=processor_options,
            ),
            file=file,
        )

    def xǁProfilerǁprint__mutmut_36(
        self,
        file: IO[str] = sys.stdout,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """print(file=sys.stdout, *, unicode=None, color=None, show_all=False, timeline=False, time='seconds', flat=False, flat_time='self', short_mode=False, processor_options=None)

        Print the captured profile to the console, as rendered by :class:`renderers.ConsoleRenderer`

        :param file: the IO stream to write to. Could be a file descriptor or sys.stdout, sys.stderr. Defaults to sys.stdout.

        See :class:`renderers.ConsoleRenderer` for the other parameters.
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
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                ),
            file=file,
        )
    
    xǁProfilerǁprint__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerǁprint__mutmut_1': xǁProfilerǁprint__mutmut_1, 
        'xǁProfilerǁprint__mutmut_2': xǁProfilerǁprint__mutmut_2, 
        'xǁProfilerǁprint__mutmut_3': xǁProfilerǁprint__mutmut_3, 
        'xǁProfilerǁprint__mutmut_4': xǁProfilerǁprint__mutmut_4, 
        'xǁProfilerǁprint__mutmut_5': xǁProfilerǁprint__mutmut_5, 
        'xǁProfilerǁprint__mutmut_6': xǁProfilerǁprint__mutmut_6, 
        'xǁProfilerǁprint__mutmut_7': xǁProfilerǁprint__mutmut_7, 
        'xǁProfilerǁprint__mutmut_8': xǁProfilerǁprint__mutmut_8, 
        'xǁProfilerǁprint__mutmut_9': xǁProfilerǁprint__mutmut_9, 
        'xǁProfilerǁprint__mutmut_10': xǁProfilerǁprint__mutmut_10, 
        'xǁProfilerǁprint__mutmut_11': xǁProfilerǁprint__mutmut_11, 
        'xǁProfilerǁprint__mutmut_12': xǁProfilerǁprint__mutmut_12, 
        'xǁProfilerǁprint__mutmut_13': xǁProfilerǁprint__mutmut_13, 
        'xǁProfilerǁprint__mutmut_14': xǁProfilerǁprint__mutmut_14, 
        'xǁProfilerǁprint__mutmut_15': xǁProfilerǁprint__mutmut_15, 
        'xǁProfilerǁprint__mutmut_16': xǁProfilerǁprint__mutmut_16, 
        'xǁProfilerǁprint__mutmut_17': xǁProfilerǁprint__mutmut_17, 
        'xǁProfilerǁprint__mutmut_18': xǁProfilerǁprint__mutmut_18, 
        'xǁProfilerǁprint__mutmut_19': xǁProfilerǁprint__mutmut_19, 
        'xǁProfilerǁprint__mutmut_20': xǁProfilerǁprint__mutmut_20, 
        'xǁProfilerǁprint__mutmut_21': xǁProfilerǁprint__mutmut_21, 
        'xǁProfilerǁprint__mutmut_22': xǁProfilerǁprint__mutmut_22, 
        'xǁProfilerǁprint__mutmut_23': xǁProfilerǁprint__mutmut_23, 
        'xǁProfilerǁprint__mutmut_24': xǁProfilerǁprint__mutmut_24, 
        'xǁProfilerǁprint__mutmut_25': xǁProfilerǁprint__mutmut_25, 
        'xǁProfilerǁprint__mutmut_26': xǁProfilerǁprint__mutmut_26, 
        'xǁProfilerǁprint__mutmut_27': xǁProfilerǁprint__mutmut_27, 
        'xǁProfilerǁprint__mutmut_28': xǁProfilerǁprint__mutmut_28, 
        'xǁProfilerǁprint__mutmut_29': xǁProfilerǁprint__mutmut_29, 
        'xǁProfilerǁprint__mutmut_30': xǁProfilerǁprint__mutmut_30, 
        'xǁProfilerǁprint__mutmut_31': xǁProfilerǁprint__mutmut_31, 
        'xǁProfilerǁprint__mutmut_32': xǁProfilerǁprint__mutmut_32, 
        'xǁProfilerǁprint__mutmut_33': xǁProfilerǁprint__mutmut_33, 
        'xǁProfilerǁprint__mutmut_34': xǁProfilerǁprint__mutmut_34, 
        'xǁProfilerǁprint__mutmut_35': xǁProfilerǁprint__mutmut_35, 
        'xǁProfilerǁprint__mutmut_36': xǁProfilerǁprint__mutmut_36
    }
    
    def print(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerǁprint__mutmut_orig"), object.__getattribute__(self, "xǁProfilerǁprint__mutmut_mutants"), args, kwargs, self)
        return result 
    
    print.__signature__ = _mutmut_signature(xǁProfilerǁprint__mutmut_orig)
    xǁProfilerǁprint__mutmut_orig.__name__ = 'xǁProfilerǁprint'

    def xǁProfilerǁoutput_text__mutmut_orig(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_1(
        self,
        unicode: bool = True,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_2(
        self,
        unicode: bool = False,
        color: bool = True,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_3(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = True,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_4(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = True,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_5(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "XXsecondsXX",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_6(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "SECONDS",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_7(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = True,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_8(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "XXselfXX",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_9(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "SELF",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_10(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = True,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_11(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=None
        )

    def xǁProfilerǁoutput_text__mutmut_12(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=None,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_13(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=None,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_14(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=None,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_15(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=None,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_16(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=None,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_17(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=None,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_18(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=None,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_19(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=None,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_20(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=None,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_21(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_22(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_23(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_24(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_25(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_26(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat_time=flat_time,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_27(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                short_mode=short_mode,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_28(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                processor_options=processor_options,
            )
        )

    def xǁProfilerǁoutput_text__mutmut_29(
        self,
        unicode: bool = False,
        color: bool = False,
        show_all: bool = False,
        timeline: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat: bool = False,
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
        processor_options: dict[str, Any] | None = None,
    ) -> str:
        """
        Return the profile output as text, as rendered by :class:`ConsoleRenderer`

        See :class:`renderers.ConsoleRenderer` for parameter description.
        """
        return self.output(
            renderer=renderers.ConsoleRenderer(
                unicode=unicode,
                color=color,
                show_all=show_all,
                timeline=timeline,
                time=time,
                flat=flat,
                flat_time=flat_time,
                short_mode=short_mode,
                )
        )
    
    xǁProfilerǁoutput_text__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerǁoutput_text__mutmut_1': xǁProfilerǁoutput_text__mutmut_1, 
        'xǁProfilerǁoutput_text__mutmut_2': xǁProfilerǁoutput_text__mutmut_2, 
        'xǁProfilerǁoutput_text__mutmut_3': xǁProfilerǁoutput_text__mutmut_3, 
        'xǁProfilerǁoutput_text__mutmut_4': xǁProfilerǁoutput_text__mutmut_4, 
        'xǁProfilerǁoutput_text__mutmut_5': xǁProfilerǁoutput_text__mutmut_5, 
        'xǁProfilerǁoutput_text__mutmut_6': xǁProfilerǁoutput_text__mutmut_6, 
        'xǁProfilerǁoutput_text__mutmut_7': xǁProfilerǁoutput_text__mutmut_7, 
        'xǁProfilerǁoutput_text__mutmut_8': xǁProfilerǁoutput_text__mutmut_8, 
        'xǁProfilerǁoutput_text__mutmut_9': xǁProfilerǁoutput_text__mutmut_9, 
        'xǁProfilerǁoutput_text__mutmut_10': xǁProfilerǁoutput_text__mutmut_10, 
        'xǁProfilerǁoutput_text__mutmut_11': xǁProfilerǁoutput_text__mutmut_11, 
        'xǁProfilerǁoutput_text__mutmut_12': xǁProfilerǁoutput_text__mutmut_12, 
        'xǁProfilerǁoutput_text__mutmut_13': xǁProfilerǁoutput_text__mutmut_13, 
        'xǁProfilerǁoutput_text__mutmut_14': xǁProfilerǁoutput_text__mutmut_14, 
        'xǁProfilerǁoutput_text__mutmut_15': xǁProfilerǁoutput_text__mutmut_15, 
        'xǁProfilerǁoutput_text__mutmut_16': xǁProfilerǁoutput_text__mutmut_16, 
        'xǁProfilerǁoutput_text__mutmut_17': xǁProfilerǁoutput_text__mutmut_17, 
        'xǁProfilerǁoutput_text__mutmut_18': xǁProfilerǁoutput_text__mutmut_18, 
        'xǁProfilerǁoutput_text__mutmut_19': xǁProfilerǁoutput_text__mutmut_19, 
        'xǁProfilerǁoutput_text__mutmut_20': xǁProfilerǁoutput_text__mutmut_20, 
        'xǁProfilerǁoutput_text__mutmut_21': xǁProfilerǁoutput_text__mutmut_21, 
        'xǁProfilerǁoutput_text__mutmut_22': xǁProfilerǁoutput_text__mutmut_22, 
        'xǁProfilerǁoutput_text__mutmut_23': xǁProfilerǁoutput_text__mutmut_23, 
        'xǁProfilerǁoutput_text__mutmut_24': xǁProfilerǁoutput_text__mutmut_24, 
        'xǁProfilerǁoutput_text__mutmut_25': xǁProfilerǁoutput_text__mutmut_25, 
        'xǁProfilerǁoutput_text__mutmut_26': xǁProfilerǁoutput_text__mutmut_26, 
        'xǁProfilerǁoutput_text__mutmut_27': xǁProfilerǁoutput_text__mutmut_27, 
        'xǁProfilerǁoutput_text__mutmut_28': xǁProfilerǁoutput_text__mutmut_28, 
        'xǁProfilerǁoutput_text__mutmut_29': xǁProfilerǁoutput_text__mutmut_29
    }
    
    def output_text(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerǁoutput_text__mutmut_orig"), object.__getattribute__(self, "xǁProfilerǁoutput_text__mutmut_mutants"), args, kwargs, self)
        return result 
    
    output_text.__signature__ = _mutmut_signature(xǁProfilerǁoutput_text__mutmut_orig)
    xǁProfilerǁoutput_text__mutmut_orig.__name__ = 'xǁProfilerǁoutput_text'

    def xǁProfilerǁoutput_html__mutmut_orig(
        self,
    ) -> str:
        """
        Return the profile output as HTML, as rendered by :class:`HTMLRenderer`
        """
        return self.output(renderer=renderers.HTMLRenderer())

    def xǁProfilerǁoutput_html__mutmut_1(
        self,
    ) -> str:
        """
        Return the profile output as HTML, as rendered by :class:`HTMLRenderer`
        """
        return self.output(renderer=None)
    
    xǁProfilerǁoutput_html__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerǁoutput_html__mutmut_1': xǁProfilerǁoutput_html__mutmut_1
    }
    
    def output_html(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerǁoutput_html__mutmut_orig"), object.__getattribute__(self, "xǁProfilerǁoutput_html__mutmut_mutants"), args, kwargs, self)
        return result 
    
    output_html.__signature__ = _mutmut_signature(xǁProfilerǁoutput_html__mutmut_orig)
    xǁProfilerǁoutput_html__mutmut_orig.__name__ = 'xǁProfilerǁoutput_html'

    def xǁProfilerǁwrite_html__mutmut_orig(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(path)
        file.write_text(
            self.output(renderer=renderers.HTMLRenderer(timeline=timeline, show_all=show_all)),
            encoding="utf-8",
        )

    def xǁProfilerǁwrite_html__mutmut_1(
        self, path: str | os.PathLike[str], timeline: bool = True, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(path)
        file.write_text(
            self.output(renderer=renderers.HTMLRenderer(timeline=timeline, show_all=show_all)),
            encoding="utf-8",
        )

    def xǁProfilerǁwrite_html__mutmut_2(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = True
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(path)
        file.write_text(
            self.output(renderer=renderers.HTMLRenderer(timeline=timeline, show_all=show_all)),
            encoding="utf-8",
        )

    def xǁProfilerǁwrite_html__mutmut_3(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = None
        file.write_text(
            self.output(renderer=renderers.HTMLRenderer(timeline=timeline, show_all=show_all)),
            encoding="utf-8",
        )

    def xǁProfilerǁwrite_html__mutmut_4(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(None)
        file.write_text(
            self.output(renderer=renderers.HTMLRenderer(timeline=timeline, show_all=show_all)),
            encoding="utf-8",
        )

    def xǁProfilerǁwrite_html__mutmut_5(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(path)
        file.write_text(
            None,
            encoding="utf-8",
        )

    def xǁProfilerǁwrite_html__mutmut_6(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(path)
        file.write_text(
            self.output(renderer=renderers.HTMLRenderer(timeline=timeline, show_all=show_all)),
            encoding=None,
        )

    def xǁProfilerǁwrite_html__mutmut_7(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(path)
        file.write_text(
            encoding="utf-8",
        )

    def xǁProfilerǁwrite_html__mutmut_8(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(path)
        file.write_text(
            self.output(renderer=renderers.HTMLRenderer(timeline=timeline, show_all=show_all)),
            )

    def xǁProfilerǁwrite_html__mutmut_9(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(path)
        file.write_text(
            self.output(renderer=None),
            encoding="utf-8",
        )

    def xǁProfilerǁwrite_html__mutmut_10(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(path)
        file.write_text(
            self.output(renderer=renderers.HTMLRenderer(timeline=None, show_all=show_all)),
            encoding="utf-8",
        )

    def xǁProfilerǁwrite_html__mutmut_11(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(path)
        file.write_text(
            self.output(renderer=renderers.HTMLRenderer(timeline=timeline, show_all=None)),
            encoding="utf-8",
        )

    def xǁProfilerǁwrite_html__mutmut_12(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(path)
        file.write_text(
            self.output(renderer=renderers.HTMLRenderer(show_all=show_all)),
            encoding="utf-8",
        )

    def xǁProfilerǁwrite_html__mutmut_13(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(path)
        file.write_text(
            self.output(renderer=renderers.HTMLRenderer(timeline=timeline, )),
            encoding="utf-8",
        )

    def xǁProfilerǁwrite_html__mutmut_14(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(path)
        file.write_text(
            self.output(renderer=renderers.HTMLRenderer(timeline=timeline, show_all=show_all)),
            encoding="XXutf-8XX",
        )

    def xǁProfilerǁwrite_html__mutmut_15(
        self, path: str | os.PathLike[str], timeline: bool = False, show_all: bool = False
    ):
        """
        Writes the profile output as HTML to a file, as rendered by :class:`HTMLRenderer`
        """
        file = Path(path)
        file.write_text(
            self.output(renderer=renderers.HTMLRenderer(timeline=timeline, show_all=show_all)),
            encoding="UTF-8",
        )
    
    xǁProfilerǁwrite_html__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerǁwrite_html__mutmut_1': xǁProfilerǁwrite_html__mutmut_1, 
        'xǁProfilerǁwrite_html__mutmut_2': xǁProfilerǁwrite_html__mutmut_2, 
        'xǁProfilerǁwrite_html__mutmut_3': xǁProfilerǁwrite_html__mutmut_3, 
        'xǁProfilerǁwrite_html__mutmut_4': xǁProfilerǁwrite_html__mutmut_4, 
        'xǁProfilerǁwrite_html__mutmut_5': xǁProfilerǁwrite_html__mutmut_5, 
        'xǁProfilerǁwrite_html__mutmut_6': xǁProfilerǁwrite_html__mutmut_6, 
        'xǁProfilerǁwrite_html__mutmut_7': xǁProfilerǁwrite_html__mutmut_7, 
        'xǁProfilerǁwrite_html__mutmut_8': xǁProfilerǁwrite_html__mutmut_8, 
        'xǁProfilerǁwrite_html__mutmut_9': xǁProfilerǁwrite_html__mutmut_9, 
        'xǁProfilerǁwrite_html__mutmut_10': xǁProfilerǁwrite_html__mutmut_10, 
        'xǁProfilerǁwrite_html__mutmut_11': xǁProfilerǁwrite_html__mutmut_11, 
        'xǁProfilerǁwrite_html__mutmut_12': xǁProfilerǁwrite_html__mutmut_12, 
        'xǁProfilerǁwrite_html__mutmut_13': xǁProfilerǁwrite_html__mutmut_13, 
        'xǁProfilerǁwrite_html__mutmut_14': xǁProfilerǁwrite_html__mutmut_14, 
        'xǁProfilerǁwrite_html__mutmut_15': xǁProfilerǁwrite_html__mutmut_15
    }
    
    def write_html(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerǁwrite_html__mutmut_orig"), object.__getattribute__(self, "xǁProfilerǁwrite_html__mutmut_mutants"), args, kwargs, self)
        return result 
    
    write_html.__signature__ = _mutmut_signature(xǁProfilerǁwrite_html__mutmut_orig)
    xǁProfilerǁwrite_html__mutmut_orig.__name__ = 'xǁProfilerǁwrite_html'

    def xǁProfilerǁopen_in_browser__mutmut_orig(self, timeline: bool = False):
        """
        Opens the last profile session in your web browser.
        """
        session = self._get_last_session_or_fail()

        return renderers.HTMLRenderer(timeline=timeline).open_in_browser(session)

    def xǁProfilerǁopen_in_browser__mutmut_1(self, timeline: bool = True):
        """
        Opens the last profile session in your web browser.
        """
        session = self._get_last_session_or_fail()

        return renderers.HTMLRenderer(timeline=timeline).open_in_browser(session)

    def xǁProfilerǁopen_in_browser__mutmut_2(self, timeline: bool = False):
        """
        Opens the last profile session in your web browser.
        """
        session = None

        return renderers.HTMLRenderer(timeline=timeline).open_in_browser(session)

    def xǁProfilerǁopen_in_browser__mutmut_3(self, timeline: bool = False):
        """
        Opens the last profile session in your web browser.
        """
        session = self._get_last_session_or_fail()

        return renderers.HTMLRenderer(timeline=timeline).open_in_browser(None)

    def xǁProfilerǁopen_in_browser__mutmut_4(self, timeline: bool = False):
        """
        Opens the last profile session in your web browser.
        """
        session = self._get_last_session_or_fail()

        return renderers.HTMLRenderer(timeline=None).open_in_browser(session)
    
    xǁProfilerǁopen_in_browser__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerǁopen_in_browser__mutmut_1': xǁProfilerǁopen_in_browser__mutmut_1, 
        'xǁProfilerǁopen_in_browser__mutmut_2': xǁProfilerǁopen_in_browser__mutmut_2, 
        'xǁProfilerǁopen_in_browser__mutmut_3': xǁProfilerǁopen_in_browser__mutmut_3, 
        'xǁProfilerǁopen_in_browser__mutmut_4': xǁProfilerǁopen_in_browser__mutmut_4
    }
    
    def open_in_browser(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerǁopen_in_browser__mutmut_orig"), object.__getattribute__(self, "xǁProfilerǁopen_in_browser__mutmut_mutants"), args, kwargs, self)
        return result 
    
    open_in_browser.__signature__ = _mutmut_signature(xǁProfilerǁopen_in_browser__mutmut_orig)
    xǁProfilerǁopen_in_browser__mutmut_orig.__name__ = 'xǁProfilerǁopen_in_browser'

    def xǁProfilerǁoutput__mutmut_orig(self, renderer: renderers.Renderer) -> str:
        """
        Returns the last profile session, as rendered by ``renderer``.

        :param renderer: The renderer to use.
        """
        session = self._get_last_session_or_fail()

        return renderer.render(session)

    def xǁProfilerǁoutput__mutmut_1(self, renderer: renderers.Renderer) -> str:
        """
        Returns the last profile session, as rendered by ``renderer``.

        :param renderer: The renderer to use.
        """
        session = None

        return renderer.render(session)

    def xǁProfilerǁoutput__mutmut_2(self, renderer: renderers.Renderer) -> str:
        """
        Returns the last profile session, as rendered by ``renderer``.

        :param renderer: The renderer to use.
        """
        session = self._get_last_session_or_fail()

        return renderer.render(None)
    
    xǁProfilerǁoutput__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerǁoutput__mutmut_1': xǁProfilerǁoutput__mutmut_1, 
        'xǁProfilerǁoutput__mutmut_2': xǁProfilerǁoutput__mutmut_2
    }
    
    def output(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerǁoutput__mutmut_orig"), object.__getattribute__(self, "xǁProfilerǁoutput__mutmut_mutants"), args, kwargs, self)
        return result 
    
    output.__signature__ = _mutmut_signature(xǁProfilerǁoutput__mutmut_orig)
    xǁProfilerǁoutput__mutmut_orig.__name__ = 'xǁProfilerǁoutput'

    def xǁProfilerǁ_get_last_session_or_fail__mutmut_orig(self) -> Session:
        if self.is_running:
            raise Exception("can't render profile output because this profiler is still running")

        if self.last_session is None:
            raise Exception(
                "can't render profile output because this profiler has not completed a profile session yet"
            )

        return self.last_session

    def xǁProfilerǁ_get_last_session_or_fail__mutmut_1(self) -> Session:
        if self.is_running:
            raise Exception(None)

        if self.last_session is None:
            raise Exception(
                "can't render profile output because this profiler has not completed a profile session yet"
            )

        return self.last_session

    def xǁProfilerǁ_get_last_session_or_fail__mutmut_2(self) -> Session:
        if self.is_running:
            raise Exception("XXcan't render profile output because this profiler is still runningXX")

        if self.last_session is None:
            raise Exception(
                "can't render profile output because this profiler has not completed a profile session yet"
            )

        return self.last_session

    def xǁProfilerǁ_get_last_session_or_fail__mutmut_3(self) -> Session:
        if self.is_running:
            raise Exception("CAN'T RENDER PROFILE OUTPUT BECAUSE THIS PROFILER IS STILL RUNNING")

        if self.last_session is None:
            raise Exception(
                "can't render profile output because this profiler has not completed a profile session yet"
            )

        return self.last_session

    def xǁProfilerǁ_get_last_session_or_fail__mutmut_4(self) -> Session:
        if self.is_running:
            raise Exception("can't render profile output because this profiler is still running")

        if self.last_session is not None:
            raise Exception(
                "can't render profile output because this profiler has not completed a profile session yet"
            )

        return self.last_session

    def xǁProfilerǁ_get_last_session_or_fail__mutmut_5(self) -> Session:
        if self.is_running:
            raise Exception("can't render profile output because this profiler is still running")

        if self.last_session is None:
            raise Exception(
                None
            )

        return self.last_session

    def xǁProfilerǁ_get_last_session_or_fail__mutmut_6(self) -> Session:
        if self.is_running:
            raise Exception("can't render profile output because this profiler is still running")

        if self.last_session is None:
            raise Exception(
                "XXcan't render profile output because this profiler has not completed a profile session yetXX"
            )

        return self.last_session

    def xǁProfilerǁ_get_last_session_or_fail__mutmut_7(self) -> Session:
        if self.is_running:
            raise Exception("can't render profile output because this profiler is still running")

        if self.last_session is None:
            raise Exception(
                "CAN'T RENDER PROFILE OUTPUT BECAUSE THIS PROFILER HAS NOT COMPLETED A PROFILE SESSION YET"
            )

        return self.last_session
    
    xǁProfilerǁ_get_last_session_or_fail__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerǁ_get_last_session_or_fail__mutmut_1': xǁProfilerǁ_get_last_session_or_fail__mutmut_1, 
        'xǁProfilerǁ_get_last_session_or_fail__mutmut_2': xǁProfilerǁ_get_last_session_or_fail__mutmut_2, 
        'xǁProfilerǁ_get_last_session_or_fail__mutmut_3': xǁProfilerǁ_get_last_session_or_fail__mutmut_3, 
        'xǁProfilerǁ_get_last_session_or_fail__mutmut_4': xǁProfilerǁ_get_last_session_or_fail__mutmut_4, 
        'xǁProfilerǁ_get_last_session_or_fail__mutmut_5': xǁProfilerǁ_get_last_session_or_fail__mutmut_5, 
        'xǁProfilerǁ_get_last_session_or_fail__mutmut_6': xǁProfilerǁ_get_last_session_or_fail__mutmut_6, 
        'xǁProfilerǁ_get_last_session_or_fail__mutmut_7': xǁProfilerǁ_get_last_session_or_fail__mutmut_7
    }
    
    def _get_last_session_or_fail(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerǁ_get_last_session_or_fail__mutmut_orig"), object.__getattribute__(self, "xǁProfilerǁ_get_last_session_or_fail__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _get_last_session_or_fail.__signature__ = _mutmut_signature(xǁProfilerǁ_get_last_session_or_fail__mutmut_orig)
    xǁProfilerǁ_get_last_session_or_fail__mutmut_orig.__name__ = 'xǁProfilerǁ_get_last_session_or_fail'
