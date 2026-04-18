from __future__ import annotations

import contextvars
import ctypes
import inspect
import sys
import time
from typing import Any

import pytest

import pyinstrument.low_level.stat_profile as native_stat_profile


def spin_until(condition, timeout=1.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if condition():
            return True
        for _ in range(1000):
            pass
    return False


def native_timing_thread_functions():
    lib = ctypes.CDLL(native_stat_profile.__file__)

    subscribe = lib.pyi_timing_thread_subscribe
    subscribe.argtypes = [ctypes.c_double]
    subscribe.restype = ctypes.c_int

    unsubscribe = lib.pyi_timing_thread_unsubscribe
    unsubscribe.argtypes = [ctypes.c_int]
    unsubscribe.restype = ctypes.c_int

    get_time = lib.pyi_timing_thread_get_time
    get_time.argtypes = []
    get_time.restype = ctypes.c_double

    get_interval = lib.pyi_timing_thread_get_interval
    get_interval.argtypes = []
    get_interval.restype = ctypes.c_double

    return subscribe, unsubscribe, get_time, get_interval


def test_native_extension_public_timer_helpers():
    overheads = native_stat_profile.measure_timing_overhead()
    coarse_resolution = native_stat_profile.walltime_coarse_resolution()

    assert set(overheads) >= {"walltime"}
    assert isinstance(overheads["walltime"], float)
    assert overheads["walltime"] >= 0.0
    assert coarse_resolution is None or coarse_resolution > 0.0


def test_native_get_frame_info_success_and_error_paths():
    class Demo:
        def instance_method(self):
            __tracebackhide__ = True
            return native_stat_profile.get_frame_info(inspect.currentframe())

        @classmethod
        def class_method(cls):
            return native_stat_profile.get_frame_info(inspect.currentframe())

    instance_info = Demo().instance_method()
    class_info = Demo.class_method()

    assert "instance_method" in instance_info
    assert "\x01c" in instance_info
    assert "\x01l" in instance_info
    assert "\x01h1" in instance_info
    assert "class_method" in class_info
    assert "\x01c" in class_info

    with pytest.raises(TypeError, match="exactly 1 argument"):
        native_stat_profile.get_frame_info()

    with pytest.raises(TypeError, match="Frame object"):
        native_stat_profile.get_frame_info(object())


def test_native_setstatprofile_argument_validation_and_custom_timer_errors():
    try:
        with pytest.raises(TypeError, match="target must be callable"):
            native_stat_profile.setstatprofile(object())

        with pytest.raises(TypeError):
            native_stat_profile.setstatprofile(lambda *_: None, 0.1, "not a context var")

        with pytest.raises(TypeError, match="argument 4 must be str"):
            native_stat_profile.setstatprofile(lambda *_: None, timer_type=object())

        with pytest.raises(TypeError, match="timer_type must be"):
            native_stat_profile.setstatprofile(lambda *_: None, timer_type="bad")

        with pytest.raises(TypeError, match="timer_func must be set"):
            native_stat_profile.setstatprofile(lambda *_: None, timer_type="timer_func")

        with pytest.raises(TypeError, match="timer_type must be 'timer_func'"):
            native_stat_profile.setstatprofile(lambda *_: None, timer_func=lambda: 0.0)

        native_stat_profile.setstatprofile(
            lambda *_: None,
            timer_type="timer_func",
            timer_func=lambda: 0.0,
        )
    finally:
        native_stat_profile.setstatprofile(None)


def test_native_setstatprofile_samples_context_changes_and_timer_func():
    context_var: contextvars.ContextVar[object | None] = contextvars.ContextVar(
        "native_context", default=None
    )
    events: list[tuple[str, Any]] = []
    current_time = 0.0

    def timer():
        return current_time

    def callback(frame, event, arg):
        events.append((event, arg))

    try:
        native_stat_profile.setstatprofile(
            callback,
            interval=0.5,
            context_var=context_var,
            timer_type="timer_func",
            timer_func=timer,
        )

        token = object()
        context_var.set(token)
        current_time = 0.1
        len([])
        current_time = 1.0
        len([])
    finally:
        native_stat_profile.setstatprofile(None)

    context_events = [arg for event, arg in events if event == "context_changed"]
    sampled_events = [event for event, _ in events if event != "context_changed"]

    assert context_events
    assert context_events[0][0] is token
    assert sampled_events


@pytest.mark.skipif(sys.platform == "win32", reason="timing thread scheduling is flaky on Windows")
def test_native_timing_thread_exported_functions():
    subscribe, unsubscribe, get_time, get_interval = native_timing_thread_functions()

    assert get_interval() == -1.0

    first = subscribe(0.05)
    second = subscribe(0.01)
    try:
        assert first >= 0
        assert second >= 0
        assert get_interval() == pytest.approx(0.01)

        before = get_time()
        assert spin_until(lambda: get_time() > before)

        assert unsubscribe(first) == 0
        assert get_interval() == pytest.approx(0.01)
        assert unsubscribe(second) == 0
        assert spin_until(lambda: get_interval() == -1.0)
        assert unsubscribe(999999) < 0
    finally:
        unsubscribe(first)
        unsubscribe(second)


@pytest.mark.skipif(sys.platform == "win32", reason="timing thread scheduling is flaky on Windows")
def test_native_timing_thread_max_subscribers_and_reused_ids():
    subscribe, unsubscribe, _, get_interval = native_timing_thread_functions()
    subscription_ids = []

    try:
        for _ in range(1000):
            subscription_id = subscribe(0.02)
            assert subscription_id >= 0
            subscription_ids.append(subscription_id)

        removed_id = subscription_ids.pop(123)
        assert unsubscribe(removed_id) == 0
        replacement_id = subscribe(0.03)
        assert replacement_id == removed_id
        subscription_ids.append(replacement_id)

        assert subscribe(0.02) == -2
        assert get_interval() == pytest.approx(0.02)
    finally:
        while subscription_ids:
            unsubscribe(subscription_ids.pop())


def test_native_setstatprofile_walltime_thread_mode_smoke():
    calls = []

    try:
        native_stat_profile.setstatprofile(
            lambda frame, event, arg: calls.append(event),
            interval=0.001,
            timer_type="walltime_thread",
        )
        assert spin_until(lambda: bool(calls))
    finally:
        native_stat_profile.setstatprofile(None)


def test_native_setstatprofile_walltime_coarse_mode_when_available():
    if native_stat_profile.walltime_coarse_resolution() is None:
        pytest.skip("coarse timer is not available on this platform")

    calls = []

    try:
        native_stat_profile.setstatprofile(
            lambda frame, event, arg: calls.append(event),
            interval=0.001,
            timer_type="walltime_coarse",
        )
        assert spin_until(lambda: bool(calls))
    finally:
        native_stat_profile.setstatprofile(None)
