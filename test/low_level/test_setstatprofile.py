import sys
import time
from typing import Any

import pytest

from pyinstrument.low_level.stat_profile import setstatprofile

from ..util import busy_wait


class CallCounter:
    def __init__(self) -> None:
        self.count = 0

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.count += 1


def test_100ms():
    counter = CallCounter()
    setstatprofile(counter, 0.1)
    busy_wait(1.0)
    setstatprofile(None)
    assert 8 < counter.count < 12


def test_10ms():
    counter = CallCounter()
    setstatprofile(counter, 0.01)
    busy_wait(1.0)
    setstatprofile(None)
    assert 70 <= counter.count <= 130


def test_internal_object_compatibility():
    setstatprofile(CallCounter(), 1e6)

    profile_state = sys.getprofile()

    print(repr(profile_state))
    print(str(profile_state))
    print(profile_state)
    print(type(profile_state))
    print(type(profile_state).__name__)

    setstatprofile(None)
