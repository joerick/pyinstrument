import contextvars
import types
from typing import Any, Callable

from pyinstrument.typing import LiteralStr

def setstatprofile(
    target: Callable[[types.FrameType, str, Any], Any] | None,
    interval: float = 0.001,
    context_var: contextvars.ContextVar[object | None] | None = None,
    timer_type: LiteralStr["walltime", "walltime-thread", "timer_func"] | None = None,
    timer_func: Callable[[], float] | None = None,
) -> None: ...
def get_frame_info(frame: types.FrameType) -> str: ...
