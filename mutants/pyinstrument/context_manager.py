from __future__ import annotations

import functools
import inspect
import sys
import typing

from pyinstrument.profiler import AsyncMode, Profiler
from pyinstrument.renderers.base import Renderer
from pyinstrument.renderers.console import ConsoleRenderer
from pyinstrument.typing import Unpack
from pyinstrument.util import file_supports_color, file_supports_unicode

CallableVar = typing.TypeVar("CallableVar", bound=typing.Callable)
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


class ProfileContextOptions(typing.TypedDict, total=False):
    interval: float
    async_mode: AsyncMode
    use_timing_thread: bool | None
    renderer: Renderer | None
    target_description: str | None


class ProfileContext:
    options: ProfileContextOptions

    def xǁProfileContextǁ__init____mutmut_orig(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_1(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = None
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_2(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "XXintervalXX": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_3(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "INTERVAL": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_4(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get(None, 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_5(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", None),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_6(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get(0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_7(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", ),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_8(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("XXintervalXX", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_9(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("INTERVAL", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_10(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 1.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_11(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "XXasync_modeXX": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_12(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "ASYNC_MODE": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_13(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get(None, "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_14(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", None),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_15(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_16(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", ),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_17(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("XXasync_modeXX", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_18(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("ASYNC_MODE", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_19(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "XXdisabledXX"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_20(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "DISABLED"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_21(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "XXuse_timing_threadXX": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_22(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "USE_TIMING_THREAD": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_23(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get(None, None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_24(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get(None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_25(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", ),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_26(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("XXuse_timing_threadXX", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_27(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("USE_TIMING_THREAD", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_28(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = None
        self.options = kwargs

    def xǁProfileContextǁ__init____mutmut_29(
        self,
        **kwargs: Unpack[ProfileContextOptions],
    ):
        profiler_options = {
            "interval": kwargs.get("interval", 0.001),
            # note- different async mode from the default, because it's easy
            # to run multiple profilers at once using the decorator/context
            # manager
            "async_mode": kwargs.get("async_mode", "disabled"),
            "use_timing_thread": kwargs.get("use_timing_thread", None),
        }
        self.profiler = Profiler(**profiler_options)
        self.options = None
    
    xǁProfileContextǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfileContextǁ__init____mutmut_1': xǁProfileContextǁ__init____mutmut_1, 
        'xǁProfileContextǁ__init____mutmut_2': xǁProfileContextǁ__init____mutmut_2, 
        'xǁProfileContextǁ__init____mutmut_3': xǁProfileContextǁ__init____mutmut_3, 
        'xǁProfileContextǁ__init____mutmut_4': xǁProfileContextǁ__init____mutmut_4, 
        'xǁProfileContextǁ__init____mutmut_5': xǁProfileContextǁ__init____mutmut_5, 
        'xǁProfileContextǁ__init____mutmut_6': xǁProfileContextǁ__init____mutmut_6, 
        'xǁProfileContextǁ__init____mutmut_7': xǁProfileContextǁ__init____mutmut_7, 
        'xǁProfileContextǁ__init____mutmut_8': xǁProfileContextǁ__init____mutmut_8, 
        'xǁProfileContextǁ__init____mutmut_9': xǁProfileContextǁ__init____mutmut_9, 
        'xǁProfileContextǁ__init____mutmut_10': xǁProfileContextǁ__init____mutmut_10, 
        'xǁProfileContextǁ__init____mutmut_11': xǁProfileContextǁ__init____mutmut_11, 
        'xǁProfileContextǁ__init____mutmut_12': xǁProfileContextǁ__init____mutmut_12, 
        'xǁProfileContextǁ__init____mutmut_13': xǁProfileContextǁ__init____mutmut_13, 
        'xǁProfileContextǁ__init____mutmut_14': xǁProfileContextǁ__init____mutmut_14, 
        'xǁProfileContextǁ__init____mutmut_15': xǁProfileContextǁ__init____mutmut_15, 
        'xǁProfileContextǁ__init____mutmut_16': xǁProfileContextǁ__init____mutmut_16, 
        'xǁProfileContextǁ__init____mutmut_17': xǁProfileContextǁ__init____mutmut_17, 
        'xǁProfileContextǁ__init____mutmut_18': xǁProfileContextǁ__init____mutmut_18, 
        'xǁProfileContextǁ__init____mutmut_19': xǁProfileContextǁ__init____mutmut_19, 
        'xǁProfileContextǁ__init____mutmut_20': xǁProfileContextǁ__init____mutmut_20, 
        'xǁProfileContextǁ__init____mutmut_21': xǁProfileContextǁ__init____mutmut_21, 
        'xǁProfileContextǁ__init____mutmut_22': xǁProfileContextǁ__init____mutmut_22, 
        'xǁProfileContextǁ__init____mutmut_23': xǁProfileContextǁ__init____mutmut_23, 
        'xǁProfileContextǁ__init____mutmut_24': xǁProfileContextǁ__init____mutmut_24, 
        'xǁProfileContextǁ__init____mutmut_25': xǁProfileContextǁ__init____mutmut_25, 
        'xǁProfileContextǁ__init____mutmut_26': xǁProfileContextǁ__init____mutmut_26, 
        'xǁProfileContextǁ__init____mutmut_27': xǁProfileContextǁ__init____mutmut_27, 
        'xǁProfileContextǁ__init____mutmut_28': xǁProfileContextǁ__init____mutmut_28, 
        'xǁProfileContextǁ__init____mutmut_29': xǁProfileContextǁ__init____mutmut_29
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfileContextǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁProfileContextǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁProfileContextǁ__init____mutmut_orig)
    xǁProfileContextǁ__init____mutmut_orig.__name__ = 'xǁProfileContextǁ__init__'

    @typing.overload
    def __call__(self, func: CallableVar, /) -> CallableVar: ...
    @typing.overload
    def __call__(self, /, **kwargs: Unpack[ProfileContextOptions]) -> "ProfileContext": ...
    def xǁProfileContextǁ__call____mutmut_orig(
        self, func: typing.Callable | None = None, /, **kwargs: Unpack[ProfileContextOptions]
    ):
        if func is not None:

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                target_description = self.options.get("target_description")
                if target_description is None:
                    target_description = f"Function {func.__qualname__} at {func.__code__.co_filename}:{func.__code__.co_firstlineno}"

                with self(target_description=target_description):
                    return func(*args, **kwargs)

            return typing.cast(typing.Callable, wrapper)
        else:
            return ProfileContext(**{**self.options, **kwargs})
    def xǁProfileContextǁ__call____mutmut_1(
        self, func: typing.Callable | None = None, /, **kwargs: Unpack[ProfileContextOptions]
    ):
        if func is None:

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                target_description = self.options.get("target_description")
                if target_description is None:
                    target_description = f"Function {func.__qualname__} at {func.__code__.co_filename}:{func.__code__.co_firstlineno}"

                with self(target_description=target_description):
                    return func(*args, **kwargs)

            return typing.cast(typing.Callable, wrapper)
        else:
            return ProfileContext(**{**self.options, **kwargs})
    def xǁProfileContextǁ__call____mutmut_2(
        self, func: typing.Callable | None = None, /, **kwargs: Unpack[ProfileContextOptions]
    ):
        if func is not None:

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                target_description = self.options.get("target_description")
                if target_description is None:
                    target_description = f"Function {func.__qualname__} at {func.__code__.co_filename}:{func.__code__.co_firstlineno}"

                with self(target_description=target_description):
                    return func(*args, **kwargs)

            return typing.cast(None, wrapper)
        else:
            return ProfileContext(**{**self.options, **kwargs})
    def xǁProfileContextǁ__call____mutmut_3(
        self, func: typing.Callable | None = None, /, **kwargs: Unpack[ProfileContextOptions]
    ):
        if func is not None:

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                target_description = self.options.get("target_description")
                if target_description is None:
                    target_description = f"Function {func.__qualname__} at {func.__code__.co_filename}:{func.__code__.co_firstlineno}"

                with self(target_description=target_description):
                    return func(*args, **kwargs)

            return typing.cast(typing.Callable, None)
        else:
            return ProfileContext(**{**self.options, **kwargs})
    def xǁProfileContextǁ__call____mutmut_4(
        self, func: typing.Callable | None = None, /, **kwargs: Unpack[ProfileContextOptions]
    ):
        if func is not None:

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                target_description = self.options.get("target_description")
                if target_description is None:
                    target_description = f"Function {func.__qualname__} at {func.__code__.co_filename}:{func.__code__.co_firstlineno}"

                with self(target_description=target_description):
                    return func(*args, **kwargs)

            return typing.cast(wrapper)
        else:
            return ProfileContext(**{**self.options, **kwargs})
    def xǁProfileContextǁ__call____mutmut_5(
        self, func: typing.Callable | None = None, /, **kwargs: Unpack[ProfileContextOptions]
    ):
        if func is not None:

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                target_description = self.options.get("target_description")
                if target_description is None:
                    target_description = f"Function {func.__qualname__} at {func.__code__.co_filename}:{func.__code__.co_firstlineno}"

                with self(target_description=target_description):
                    return func(*args, **kwargs)

            return typing.cast(typing.Callable, )
        else:
            return ProfileContext(**{**self.options, **kwargs})
    
    xǁProfileContextǁ__call____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfileContextǁ__call____mutmut_1': xǁProfileContextǁ__call____mutmut_1, 
        'xǁProfileContextǁ__call____mutmut_2': xǁProfileContextǁ__call____mutmut_2, 
        'xǁProfileContextǁ__call____mutmut_3': xǁProfileContextǁ__call____mutmut_3, 
        'xǁProfileContextǁ__call____mutmut_4': xǁProfileContextǁ__call____mutmut_4, 
        'xǁProfileContextǁ__call____mutmut_5': xǁProfileContextǁ__call____mutmut_5
    }
    
    def __call__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfileContextǁ__call____mutmut_orig"), object.__getattribute__(self, "xǁProfileContextǁ__call____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __call__.__signature__ = _mutmut_signature(xǁProfileContextǁ__call____mutmut_orig)
    xǁProfileContextǁ__call____mutmut_orig.__name__ = 'xǁProfileContextǁ__call__'

    def xǁProfileContextǁ__enter____mutmut_orig(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_1(self):
        if self.profiler.is_running:
            raise RuntimeError(
                None
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_2(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "XXThis profiler is already running - did you forget the brackets on pyinstrument.profile() ?XX"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_3(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "this profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_4(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "THIS PROFILER IS ALREADY RUNNING - DID YOU FORGET THE BRACKETS ON PYINSTRUMENT.PROFILE() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_5(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = None  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_6(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_7(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = None
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_8(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get(None)
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_9(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("XXtarget_descriptionXX")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_10(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("TARGET_DESCRIPTION")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_11(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is not None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_12(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = None

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_13(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                None, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_14(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, None
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_15(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_16(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_17(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "XXBlock at {}:{}XX".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_18(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_19(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "BLOCK AT {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_20(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=None,
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_21(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            target_description=None,
        )

    def xǁProfileContextǁ__enter____mutmut_22(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            target_description=target_description,
        )

    def xǁProfileContextǁ__enter____mutmut_23(self):
        if self.profiler.is_running:
            raise RuntimeError(
                "This profiler is already running - did you forget the brackets on pyinstrument.profile() ?"
            )

        caller_frame = inspect.currentframe().f_back  # type: ignore
        assert caller_frame is not None
        target_description = self.options.get("target_description")
        if target_description is None:
            target_description = "Block at {}:{}".format(
                caller_frame.f_code.co_filename, caller_frame.f_lineno
            )

        self.profiler.start(
            caller_frame=caller_frame,
            )
    
    xǁProfileContextǁ__enter____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfileContextǁ__enter____mutmut_1': xǁProfileContextǁ__enter____mutmut_1, 
        'xǁProfileContextǁ__enter____mutmut_2': xǁProfileContextǁ__enter____mutmut_2, 
        'xǁProfileContextǁ__enter____mutmut_3': xǁProfileContextǁ__enter____mutmut_3, 
        'xǁProfileContextǁ__enter____mutmut_4': xǁProfileContextǁ__enter____mutmut_4, 
        'xǁProfileContextǁ__enter____mutmut_5': xǁProfileContextǁ__enter____mutmut_5, 
        'xǁProfileContextǁ__enter____mutmut_6': xǁProfileContextǁ__enter____mutmut_6, 
        'xǁProfileContextǁ__enter____mutmut_7': xǁProfileContextǁ__enter____mutmut_7, 
        'xǁProfileContextǁ__enter____mutmut_8': xǁProfileContextǁ__enter____mutmut_8, 
        'xǁProfileContextǁ__enter____mutmut_9': xǁProfileContextǁ__enter____mutmut_9, 
        'xǁProfileContextǁ__enter____mutmut_10': xǁProfileContextǁ__enter____mutmut_10, 
        'xǁProfileContextǁ__enter____mutmut_11': xǁProfileContextǁ__enter____mutmut_11, 
        'xǁProfileContextǁ__enter____mutmut_12': xǁProfileContextǁ__enter____mutmut_12, 
        'xǁProfileContextǁ__enter____mutmut_13': xǁProfileContextǁ__enter____mutmut_13, 
        'xǁProfileContextǁ__enter____mutmut_14': xǁProfileContextǁ__enter____mutmut_14, 
        'xǁProfileContextǁ__enter____mutmut_15': xǁProfileContextǁ__enter____mutmut_15, 
        'xǁProfileContextǁ__enter____mutmut_16': xǁProfileContextǁ__enter____mutmut_16, 
        'xǁProfileContextǁ__enter____mutmut_17': xǁProfileContextǁ__enter____mutmut_17, 
        'xǁProfileContextǁ__enter____mutmut_18': xǁProfileContextǁ__enter____mutmut_18, 
        'xǁProfileContextǁ__enter____mutmut_19': xǁProfileContextǁ__enter____mutmut_19, 
        'xǁProfileContextǁ__enter____mutmut_20': xǁProfileContextǁ__enter____mutmut_20, 
        'xǁProfileContextǁ__enter____mutmut_21': xǁProfileContextǁ__enter____mutmut_21, 
        'xǁProfileContextǁ__enter____mutmut_22': xǁProfileContextǁ__enter____mutmut_22, 
        'xǁProfileContextǁ__enter____mutmut_23': xǁProfileContextǁ__enter____mutmut_23
    }
    
    def __enter__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfileContextǁ__enter____mutmut_orig"), object.__getattribute__(self, "xǁProfileContextǁ__enter____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __enter__.__signature__ = _mutmut_signature(xǁProfileContextǁ__enter____mutmut_orig)
    xǁProfileContextǁ__enter____mutmut_orig.__name__ = 'xǁProfileContextǁ__enter__'

    def xǁProfileContextǁ__exit____mutmut_orig(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=file_supports_unicode(f),
                short_mode=True,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_1(self, exc_type, exc_value, traceback):
        session = None

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=file_supports_unicode(f),
                short_mode=True,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_2(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = None
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=file_supports_unicode(f),
                short_mode=True,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_3(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get(None)
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=file_supports_unicode(f),
                short_mode=True,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_4(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("XXrendererXX")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=file_supports_unicode(f),
                short_mode=True,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_5(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("RENDERER")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=file_supports_unicode(f),
                short_mode=True,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_6(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = None

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=file_supports_unicode(f),
                short_mode=True,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_7(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is not None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=file_supports_unicode(f),
                short_mode=True,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_8(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is None:
            renderer = None

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_9(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=None,
                unicode=file_supports_unicode(f),
                short_mode=True,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_10(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=None,
                short_mode=True,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_11(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=file_supports_unicode(f),
                short_mode=None,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_12(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                unicode=file_supports_unicode(f),
                short_mode=True,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_13(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                short_mode=True,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_14(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=file_supports_unicode(f),
                )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_15(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(None),
                unicode=file_supports_unicode(f),
                short_mode=True,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_16(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=file_supports_unicode(None),
                short_mode=True,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_17(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=file_supports_unicode(f),
                short_mode=False,
            )

        f.write(renderer.render(session))

    def xǁProfileContextǁ__exit____mutmut_18(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=file_supports_unicode(f),
                short_mode=True,
            )

        f.write(None)

    def xǁProfileContextǁ__exit____mutmut_19(self, exc_type, exc_value, traceback):
        session = self.profiler.stop()

        renderer = self.options.get("renderer")
        f = sys.stderr

        if renderer is None:
            renderer = ConsoleRenderer(
                color=file_supports_color(f),
                unicode=file_supports_unicode(f),
                short_mode=True,
            )

        f.write(renderer.render(None))
    
    xǁProfileContextǁ__exit____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfileContextǁ__exit____mutmut_1': xǁProfileContextǁ__exit____mutmut_1, 
        'xǁProfileContextǁ__exit____mutmut_2': xǁProfileContextǁ__exit____mutmut_2, 
        'xǁProfileContextǁ__exit____mutmut_3': xǁProfileContextǁ__exit____mutmut_3, 
        'xǁProfileContextǁ__exit____mutmut_4': xǁProfileContextǁ__exit____mutmut_4, 
        'xǁProfileContextǁ__exit____mutmut_5': xǁProfileContextǁ__exit____mutmut_5, 
        'xǁProfileContextǁ__exit____mutmut_6': xǁProfileContextǁ__exit____mutmut_6, 
        'xǁProfileContextǁ__exit____mutmut_7': xǁProfileContextǁ__exit____mutmut_7, 
        'xǁProfileContextǁ__exit____mutmut_8': xǁProfileContextǁ__exit____mutmut_8, 
        'xǁProfileContextǁ__exit____mutmut_9': xǁProfileContextǁ__exit____mutmut_9, 
        'xǁProfileContextǁ__exit____mutmut_10': xǁProfileContextǁ__exit____mutmut_10, 
        'xǁProfileContextǁ__exit____mutmut_11': xǁProfileContextǁ__exit____mutmut_11, 
        'xǁProfileContextǁ__exit____mutmut_12': xǁProfileContextǁ__exit____mutmut_12, 
        'xǁProfileContextǁ__exit____mutmut_13': xǁProfileContextǁ__exit____mutmut_13, 
        'xǁProfileContextǁ__exit____mutmut_14': xǁProfileContextǁ__exit____mutmut_14, 
        'xǁProfileContextǁ__exit____mutmut_15': xǁProfileContextǁ__exit____mutmut_15, 
        'xǁProfileContextǁ__exit____mutmut_16': xǁProfileContextǁ__exit____mutmut_16, 
        'xǁProfileContextǁ__exit____mutmut_17': xǁProfileContextǁ__exit____mutmut_17, 
        'xǁProfileContextǁ__exit____mutmut_18': xǁProfileContextǁ__exit____mutmut_18, 
        'xǁProfileContextǁ__exit____mutmut_19': xǁProfileContextǁ__exit____mutmut_19
    }
    
    def __exit__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfileContextǁ__exit____mutmut_orig"), object.__getattribute__(self, "xǁProfileContextǁ__exit____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __exit__.__signature__ = _mutmut_signature(xǁProfileContextǁ__exit____mutmut_orig)
    xǁProfileContextǁ__exit____mutmut_orig.__name__ = 'xǁProfileContextǁ__exit__'


class _Profile:
    @typing.overload
    def __call__(self, func: CallableVar, /) -> CallableVar: ...
    @typing.overload
    def __call__(self, /, **kwargs: Unpack[ProfileContextOptions]) -> "ProfileContext": ...
    def xǁ_Profileǁ__call____mutmut_orig(
        self, func: typing.Callable | None = None, /, **kwargs: Unpack[ProfileContextOptions]
    ):
        if func is not None:
            return ProfileContext(**kwargs)(func)
        else:
            return ProfileContext(**kwargs)
    def xǁ_Profileǁ__call____mutmut_1(
        self, func: typing.Callable | None = None, /, **kwargs: Unpack[ProfileContextOptions]
    ):
        if func is None:
            return ProfileContext(**kwargs)(func)
        else:
            return ProfileContext(**kwargs)
    def xǁ_Profileǁ__call____mutmut_2(
        self, func: typing.Callable | None = None, /, **kwargs: Unpack[ProfileContextOptions]
    ):
        if func is not None:
            return ProfileContext(**kwargs)(None)
        else:
            return ProfileContext(**kwargs)
    
    xǁ_Profileǁ__call____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁ_Profileǁ__call____mutmut_1': xǁ_Profileǁ__call____mutmut_1, 
        'xǁ_Profileǁ__call____mutmut_2': xǁ_Profileǁ__call____mutmut_2
    }
    
    def __call__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁ_Profileǁ__call____mutmut_orig"), object.__getattribute__(self, "xǁ_Profileǁ__call____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __call__.__signature__ = _mutmut_signature(xǁ_Profileǁ__call____mutmut_orig)
    xǁ_Profileǁ__call____mutmut_orig.__name__ = 'xǁ_Profileǁ__call__'


profile = _Profile()
