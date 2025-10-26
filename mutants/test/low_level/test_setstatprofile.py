import sys
import time
from typing import Any

import pytest

from ..util import busy_wait, flaky_in_ci
from .util import parametrize_setstatprofile


class CallCounter:
    def __init__(self) -> None:
        self.count = 0

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.count += 1


@flaky_in_ci
@parametrize_setstatprofile
def test_100ms(setstatprofile):
    counter = CallCounter()
    setstatprofile(counter, 0.1)
    busy_wait(1.0)
    setstatprofile(None)
    assert 8 < counter.count < 12


@flaky_in_ci
@parametrize_setstatprofile
def test_10ms(setstatprofile):
    counter = CallCounter()
    setstatprofile(counter, 0.01)
    busy_wait(1.0)
    setstatprofile(None)
    assert 70 <= counter.count <= 130


@parametrize_setstatprofile
def test_internal_object_compatibility(setstatprofile):
    setstatprofile(CallCounter(), 1e6)

    profile_state = sys.getprofile()

    print(repr(profile_state))
    print(str(profile_state))
    print(profile_state)
    print(type(profile_state))
    print(type(profile_state).__name__)  # type: ignore

    setstatprofile(None)
