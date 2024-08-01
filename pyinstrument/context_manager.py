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


class ProfileContextOptions(typing.TypedDict, total=False):
    interval: float
    async_mode: AsyncMode
    use_timing_thread: bool | None
    renderer: Renderer | None
    target_description: str | None


class ProfileContext:
    options: ProfileContextOptions

    def __init__(
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

    @typing.overload
    def __call__(self, func: CallableVar, /) -> CallableVar: ...
    @typing.overload
    def __call__(self, /, **kwargs: Unpack[ProfileContextOptions]) -> "ProfileContext": ...
    def __call__(
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

    def __enter__(self):
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

    def __exit__(self, exc_type, exc_value, traceback):
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


class _Profile:
    @typing.overload
    def __call__(self, func: CallableVar, /) -> CallableVar: ...
    @typing.overload
    def __call__(self, /, **kwargs: Unpack[ProfileContextOptions]) -> "ProfileContext": ...
    def __call__(
        self, func: typing.Callable | None = None, /, **kwargs: Unpack[ProfileContextOptions]
    ):
        if func is not None:
            return ProfileContext(**kwargs)(func)
        else:
            return ProfileContext(**kwargs)


profile = _Profile()
