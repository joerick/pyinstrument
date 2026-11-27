import ctypes
import os
import sys
import time

import pytest

import pyinstrument.low_level.stat_profile as native_module
from pyinstrument.low_level import pyi_timing_thread_python

from ..util import busy_wait, flaky_in_ci

lib = ctypes.CDLL(native_module.__file__)

pyi_timing_thread_subscribe = lib.pyi_timing_thread_subscribe
pyi_timing_thread_subscribe.argtypes = [ctypes.c_double]
pyi_timing_thread_subscribe.restype = ctypes.c_int

pyi_timing_thread_get_time = lib.pyi_timing_thread_get_time
pyi_timing_thread_get_time.argtypes = []
pyi_timing_thread_get_time.restype = ctypes.c_double

pyi_timing_thread_get_interval = lib.pyi_timing_thread_get_interval
pyi_timing_thread_get_interval.argtypes = []
pyi_timing_thread_get_interval.restype = ctypes.c_double

pyi_timing_thread_unsubscribe = lib.pyi_timing_thread_unsubscribe
pyi_timing_thread_unsubscribe.argtypes = [ctypes.c_int]
pyi_timing_thread_unsubscribe.restype = ctypes.c_int

PYI_TIMING_THREAD_UNKNOWN_ERROR = -1
PYI_TIMING_THREAD_TOO_MANY_SUBSCRIBERS = -2
PYI_TIMING_THREAD_NOT_SUBSCRIBED = -3


if sys.platform == "win32":
    # on windows, the thread scheduling 'quanta', the time that a thread can run
    # before potentially being preempted, is 20-30ms. This means that the
    # worst-case, we have to wait 30ms before the timing thread gets a chance to
    # run. This isn't really a huge problem in practice, because thread-based
    # timing isn't much use on windows, since the synchronous timing functions are
    # so fast.
    WAIT_TIME = 0.03
elif os.environ.get("QEMU_EMULATED"):
    # the scheduler seems slower under emulation
    WAIT_TIME = 0.2
else:
    WAIT_TIME = 0.015


@flaky_in_ci
def test():
    # check the thread isn't running to begin with
    assert pyi_timing_thread_get_interval() == -1

    time_before = pyi_timing_thread_get_time()
    time.sleep(WAIT_TIME)
    assert pyi_timing_thread_get_time() == time_before

    # subscribe
    subscription_id = pyi_timing_thread_subscribe(0.001)
    try:
        assert subscription_id >= 0

        assert pyi_timing_thread_get_interval() == 0.001

        # check it's updating
        busy_wait(WAIT_TIME)
        time_a = pyi_timing_thread_get_time()
        assert time_a > time_before
        busy_wait(WAIT_TIME)
        time_b = pyi_timing_thread_get_time()
        assert time_b > time_a

        # unsubscribe
        assert pyi_timing_thread_unsubscribe(subscription_id) == 0

        assert pyi_timing_thread_get_interval() == -1

        # check it's stopped updating
        time.sleep(WAIT_TIME)
        time_c = pyi_timing_thread_get_time()
        time.sleep(WAIT_TIME)
        time_d = pyi_timing_thread_get_time()
        assert time_c == time_d
    finally:
        # ensure the subscriber is removed even if the test fails
        pyi_timing_thread_unsubscribe(subscription_id)


def test_max_subscribers():
    subscription_ids = []

    try:
        for i in range(1000):
            subscription_id = pyi_timing_thread_subscribe(0.001)
            assert subscription_id >= 0
            subscription_ids.append(subscription_id)

        # the next one should fail
        assert pyi_timing_thread_subscribe(0.001) == PYI_TIMING_THREAD_TOO_MANY_SUBSCRIBERS

        # unsubscribe them in FIFO order
        for subscription_id in subscription_ids:
            assert pyi_timing_thread_get_interval() == 0.001
            assert pyi_timing_thread_unsubscribe(subscription_id) == 0

        # check there are no subscribers left
        assert pyi_timing_thread_get_interval() == -1
    finally:
        # ensure all subscription ids are removed even if the test fails
        while subscription_ids:
            subscription_id = subscription_ids.pop()
            pyi_timing_thread_unsubscribe(subscription_id)


@flaky_in_ci
@pytest.mark.parametrize("impl", [lib, pyi_timing_thread_python], ids=["c", "python"])
def test_first_subscription_interval(impl):
    # the first subscription starts the thread, which should use the
    # subscription's interval from the start, rather than the 1s default.
    subscription_id = impl.pyi_timing_thread_subscribe(0.001)
    try:
        time_a = impl.pyi_timing_thread_get_time()
        time.sleep(WAIT_TIME)
        time_b = impl.pyi_timing_thread_get_time()
        assert time_b > time_a
        time.sleep(WAIT_TIME)
        assert impl.pyi_timing_thread_get_time() > time_b
    finally:
        impl.pyi_timing_thread_unsubscribe(subscription_id)


def test_duplicate_unsubscribe():
    subscription_id = pyi_timing_thread_subscribe(0.001)
    assert pyi_timing_thread_unsubscribe(subscription_id) == 0
    time.sleep(WAIT_TIME)
    assert pyi_timing_thread_unsubscribe(subscription_id) == PYI_TIMING_THREAD_NOT_SUBSCRIBED
    assert pyi_timing_thread_get_interval() == -1
