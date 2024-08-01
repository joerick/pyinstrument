import ctypes
import time

import pytest

import pyinstrument.low_level.stat_profile as native_module

lib = ctypes.CDLL(native_module.__file__)

pyi_floatclock = lib.pyi_floatclock
pyi_floatclock.argtypes = [ctypes.c_int]
pyi_floatclock.restype = ctypes.c_double


def test_floatclock():
    time_a = pyi_floatclock(0)
    time.sleep(0.001)
    time_b = pyi_floatclock(0)
    assert time_b > time_a


def test_is_in_seconds():
    floatclock_time_a = pyi_floatclock(0)
    time_a = time.time()

    time.sleep(0.1)

    floatclock_time_b = pyi_floatclock(0)
    time_b = time.time()

    floatclock_duration = floatclock_time_b - floatclock_time_a
    duration = time_b - time_a

    assert floatclock_duration == pytest.approx(duration, rel=0.1)
