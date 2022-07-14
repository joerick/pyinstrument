import contextvars
import types
from typing import Any, Callable

ProfileFunc = Callable[[types.FrameType, str, Any], Any]

def setstatprofile(
    target: ProfileFunc | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_func: Callable[[], float] | None = None,
) -> None: ...
def get_frame_info(frame: types.FrameType) -> str: ...
