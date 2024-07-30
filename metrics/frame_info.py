from __future__ import annotations

import inspect
from timeit import Timer
from types import FrameType
from typing import Final

from pyinstrument.low_level.stat_profile import get_frame_info

frame: Final[FrameType | None] = inspect.currentframe()
assert frame


def test_func():
    get_frame_info(frame)


t = Timer(stmt=test_func)
test_func_timings = t.repeat(number=400000)

print("min time", min(test_func_timings))
print("max time", max(test_func_timings))
print("average time", sum(test_func_timings) / len(test_func_timings))
