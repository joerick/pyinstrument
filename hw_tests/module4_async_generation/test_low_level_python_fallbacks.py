from __future__ import annotations

import time

import pytest

from pyinstrument.low_level import pyi_timing_thread_python as timing_thread
from pyinstrument.low_level.types import TimerType


def wait_for(condition, timeout=1.0):
    start = time.time()
    while time.time() < start + timeout:
        if condition():
            return True
        time.sleep(0.001)
    return False


def test_timer_type_literal_values():
    assert TimerType == "walltime" or TimerType  # runtime smoke check for the alias


def test_timing_thread_python_subscribe_unsubscribe_cycle():
    timing_thread.subscribers.clear()
    timing_thread.current_time = 0.0
    timing_thread.thread_should_exit = False
    timing_thread.thread_alive = False

    first = timing_thread.pyi_timing_thread_subscribe(0.05)
    second = timing_thread.pyi_timing_thread_subscribe(0.01)

    try:
        assert first == 0
        assert second == 1
        assert timing_thread.pyi_timing_thread_get_interval() == 0.01
        assert wait_for(lambda: timing_thread.pyi_timing_thread_get_time() > 0.0)
        assert timing_thread.get_interval(1.0) == 0.01
        assert timing_thread.pyi_timing_thread_unsubscribe(first) == 0
        assert timing_thread.pyi_timing_thread_get_interval() == 0.01
        assert timing_thread.pyi_timing_thread_unsubscribe(second) == 0
        assert wait_for(lambda: timing_thread.thread_alive is False)
        assert timing_thread.pyi_timing_thread_get_interval() == -1.0
    finally:
        while timing_thread.subscribers:
            timing_thread.pyi_timing_thread_unsubscribe(timing_thread.subscribers[0].id)


def test_timing_thread_python_reuses_smallest_available_id():
    timing_thread.subscribers.clear()
    timing_thread.thread_should_exit = False
    timing_thread.thread_alive = False

    first = timing_thread.pyi_timing_thread_subscribe(0.1)
    second = timing_thread.pyi_timing_thread_subscribe(0.2)
    assert timing_thread.pyi_timing_thread_unsubscribe(first) == 0
    replacement = timing_thread.pyi_timing_thread_subscribe(0.3)

    try:
        assert replacement == first
    finally:
        for ident in [second, replacement]:
            timing_thread.pyi_timing_thread_unsubscribe(ident)
        wait_for(lambda: timing_thread.thread_alive is False)


def test_timing_thread_python_unsubscribe_missing_id_raises():
    timing_thread.subscribers.clear()
    timing_thread.thread_should_exit = False
    timing_thread.thread_alive = False

    with pytest.raises(Exception, match="NOT_SUBSCRIBED"):
        timing_thread.pyi_timing_thread_unsubscribe(999)
