import asyncio
import dataclasses
import json
import time
from functools import partial
from test.fake_time_util import fake_time
from typing import Generator, Optional

import pytest
import trio

from pyinstrument import Profiler, renderers
from pyinstrument.frame import BaseFrame, Frame
from pyinstrument.renderers.speedscope import SpeedscopeEvent, SpeedscopeEventType, SpeedscopeFrame
from pyinstrument.session import Session

from .util import assert_never, busy_wait, flaky_in_ci

# Utilities #


def long_function_a():
    time.sleep(0.25)


def long_function_b():
    time.sleep(0.5)


# Tests #


def test_collapses_multiple_calls_by_default():
    profiler = Profiler()

    with fake_time():
        profiler.start()

        long_function_a()
        long_function_b()
        long_function_a()
        long_function_b()

        profiler.stop()

    text_output = profiler.output_text()
    print(text_output)

    # output should be something like:
    # 1.500 test_collapses_multiple_calls_by_default  test/test_profiler.py:25
    # |- 0.500 long_function_a  test/test_profiler.py:17
    # |- 0.500 long_function_b  test/test_profiler.py:20

    assert text_output.count("1.500 test_collapses_multiple_calls_by_default") == 1
    assert text_output.count("0.500 long_function_a") == 1
    assert text_output.count("1.000 long_function_b") == 1


def test_profiler_retains_multiple_calls():
    profiler = Profiler()

    with fake_time():
        profiler.start()

        long_function_a()
        long_function_b()
        long_function_a()
        long_function_b()

        profiler.stop()

    print(profiler.output_text())

    assert profiler.last_session
    frame = profiler.last_session.root_frame()
    assert frame
    assert frame.function == "test_profiler_retains_multiple_calls"
    assert len(frame.children) == 4


def test_two_functions():
    profiler = Profiler()

    with fake_time():
        profiler.start()

        long_function_a()
        long_function_b()

        profiler.stop()

    print(profiler.output_text())

    assert profiler.last_session

    frame = profiler.last_session.root_frame()

    assert frame
    assert frame.function == "test_two_functions"
    assert len(frame.children) == 2

    frame_b, frame_a = sorted(frame.children, key=lambda f: f.time(), reverse=True)

    assert frame_a.function == "long_function_a"
    assert frame_b.function == "long_function_b"

    # busy CI runners can be slow to wake up from the sleep. So we relax the
    # ranges a bit
    assert frame_a.time() == pytest.approx(0.25, abs=0.1)
    assert frame_b.time() == pytest.approx(0.5, abs=0.2)


def test_context_manager():
    with fake_time():
        with Profiler() as profiler:
            long_function_a()
            long_function_b()

    assert profiler.last_session
    frame = profiler.last_session.root_frame()
    assert frame
    assert frame.function == "test_context_manager"
    assert len(frame.children) == 2


def test_json_output():
    with fake_time():
        with Profiler() as profiler:
            long_function_a()
            long_function_b()

    output_data = profiler.output(renderers.JSONRenderer())

    output = json.loads(output_data)
    assert "root_frame" in output

    root_frame = output["root_frame"]

    assert root_frame["function"] == "test_json_output"
    assert len(root_frame["children"]) == 2


def test_speedscope_output():
    with fake_time():
        with Profiler() as profiler:
            long_function_a()
            long_function_b()

    output_data = profiler.output(renderers.SpeedscopeRenderer())

    output = json.loads(output_data)

    file_level_schema_fields = {
        "$schema",
        "name",
        "exporter",
        "activeProfileIndex",
        "profiles",
        "shared",
    }
    for file_field in file_level_schema_fields:
        assert file_field in output

    assert output["$schema"] == "https://www.speedscope.app/file-format-schema.json"
    assert "pyinstrument" in output["exporter"]
    assert output["activeProfileIndex"] is None
    assert "CPU profile" in output["name"]

    assert "frames" in output["shared"]
    speedscope_frame_list = output["shared"]["frames"]

    # Distinct functions called stores indices in key-value pairs because function
    # index lookup needed for Speedscope event list tests. Were we not testing
    # the event list, the distinct functions called could be stored as a tuple.
    distinct_functions_called = {
        "test_speedscope_output": 0,
        "long_function_a": 1,
        "sleep": 2,
        "long_function_b": 3,
    }
    assert len(speedscope_frame_list) == len(distinct_functions_called)
    speedscope_frame_fields = tuple([field.name for field in dataclasses.fields(SpeedscopeFrame)])
    for (function_name, frame_index) in distinct_functions_called.items():
        for frame_field in speedscope_frame_fields:
            assert frame_field in speedscope_frame_list[frame_index], (
                f"Field named '{frame_field}' not in Speedscope output"
                f"at 'shared.frames[{frame_index}]'"
            )
        frame_index_name = speedscope_frame_list[frame_index]["name"]
        assert frame_index_name == function_name, (
            f"Speedscope output 'shared.frames[{frame_index}].name' has value "
            f"{frame_index_name} != {function_name}"
        )

    speedscope_profile_list = output["profiles"]
    assert len(speedscope_profile_list) == 1
    speedscope_profile = speedscope_profile_list[0]
    speedscope_profile_fields = ("type", "name", "unit", "startValue", "endValue", "events")
    for profile_field in speedscope_profile_fields:
        assert (
            profile_field in speedscope_profile
        ), f"Field named '{profile_field}' not in Speedscope output at 'profiles[0]'"

    start_time_in_seconds = 0.0
    event_time_in_seconds = start_time_in_seconds
    assert speedscope_profile["type"] == "evented"
    assert speedscope_profile["unit"] == "seconds"
    assert speedscope_profile["startValue"] == start_time_in_seconds

    """Two helper functions for constructing a timeline and testing it"""

    def update_event_time_on_sleep_close(time_increment_in_seconds: float):
        """Updates running total of event time in seconds and returns updated value"""
        nonlocal event_time_in_seconds
        event_time_in_seconds += time_increment_in_seconds
        return event_time_in_seconds

    def get_approx_abs_tol(time_in_seconds: float):
        """Computes absolute tolerance for given time value to account for CI time jitter"""
        uncertainty_per_quarter_second = 0.1
        absolute_tolerance = (time_in_seconds / 0.25) * uncertainty_per_quarter_second
        return absolute_tolerance

    speedscope_event_list = speedscope_profile["events"]
    sleep_a_time_in_seconds = 0.25
    sleep_b_time_in_seconds = 0.5

    output_event_tuple = (
        SpeedscopeEvent(
            SpeedscopeEventType.OPEN,
            event_time_in_seconds,
            distinct_functions_called["test_speedscope_output"],
        ),
        SpeedscopeEvent(
            SpeedscopeEventType.OPEN,
            event_time_in_seconds,
            distinct_functions_called["long_function_a"],
        ),
        SpeedscopeEvent(
            SpeedscopeEventType.OPEN,
            event_time_in_seconds,
            distinct_functions_called["sleep"],
        ),
        SpeedscopeEvent(
            SpeedscopeEventType.CLOSE,
            update_event_time_on_sleep_close(sleep_a_time_in_seconds),
            distinct_functions_called["sleep"],
        ),
        SpeedscopeEvent(
            SpeedscopeEventType.CLOSE,
            event_time_in_seconds,
            distinct_functions_called["long_function_a"],
        ),
        SpeedscopeEvent(
            SpeedscopeEventType.OPEN,
            event_time_in_seconds,
            distinct_functions_called["long_function_b"],
        ),
        SpeedscopeEvent(
            SpeedscopeEventType.OPEN,
            event_time_in_seconds,
            distinct_functions_called["sleep"],
        ),
        SpeedscopeEvent(
            SpeedscopeEventType.CLOSE,
            update_event_time_on_sleep_close(sleep_b_time_in_seconds),
            distinct_functions_called["sleep"],
        ),
        SpeedscopeEvent(
            SpeedscopeEventType.CLOSE,
            event_time_in_seconds,
            distinct_functions_called["long_function_b"],
        ),
        SpeedscopeEvent(
            SpeedscopeEventType.CLOSE,
            event_time_in_seconds,
            distinct_functions_called["test_speedscope_output"],
        ),
    )

    assert len(speedscope_event_list) == len(output_event_tuple)
    speedscope_event_fields = tuple([field.name for field in dataclasses.fields(SpeedscopeEvent)])
    for (event_index, speedscope_event) in enumerate(speedscope_event_list):
        for event_field in speedscope_event_fields:
            assert event_field in speedscope_event, (
                f"Speedscope output 'profiles[0].events[{event_index}]' lacks "
                f"a field named '{event_field}'"
            )

        output_event_type = output_event_tuple[event_index].type.value
        speedscope_event_type = speedscope_event["type"]
        assert speedscope_event["type"] == output_event_tuple[event_index].type.value, (
            f"Speedscope output 'profiles[0].events[{event_index}].type has "
            f"value {speedscope_event_type} != {output_event_type}"
        )

        output_event_frame_index = output_event_tuple[event_index].frame
        speedscope_event_frame_index = speedscope_event["frame"]
        assert speedscope_event_frame_index == output_event_frame_index, (
            f"Speedscope output 'profiles[0].events[{event_index}].frame has "
            f"value {speedscope_event_frame_index} != {output_event_frame_index}"
        )

        output_event_time_in_seconds = output_event_tuple[event_index].at
        output_event_time_abs_tol = get_approx_abs_tol(output_event_time_in_seconds)
        speedscope_event_time_in_seconds = speedscope_event["at"]
        assert speedscope_event_time_in_seconds == pytest.approx(
            output_event_time_in_seconds, abs=output_event_time_abs_tol
        ), (
            f"Speedscope output 'profiles[0].events[{event_index}].at has value "
            f"{speedscope_event_time_in_seconds} != {output_event_time_in_seconds} "
            f"+/- {output_event_time_abs_tol}"
        )

    assert speedscope_profile["endValue"] == pytest.approx(
        event_time_in_seconds, abs=get_approx_abs_tol(event_time_in_seconds)
    )


def test_empty_profile():
    with Profiler() as profiler:
        pass
    profiler.output(renderer=renderers.ConsoleRenderer())


@flaky_in_ci
def test_state_management():
    profiler = Profiler()

    assert profiler.last_session is None
    assert profiler.is_running == False

    profiler.start()

    assert profiler.last_session is None
    assert profiler.is_running == True

    busy_wait(0.1)

    profiler.stop()

    assert profiler.is_running == False
    assert profiler.last_session is not None
    assert profiler.last_session.duration == pytest.approx(0.1, rel=0.2)

    # test a second session, does it merge with the first?
    profiler.start()

    assert profiler.is_running == True
    busy_wait(0.1)

    profiler.stop()

    assert profiler.is_running == False

    assert profiler.last_session is not None
    assert profiler.last_session.duration == pytest.approx(0.2, rel=0.2)

    # test a reset
    profiler.reset()
    assert profiler.last_session is None

    # test a reset while running
    profiler.start()
    assert profiler.is_running == True
    profiler.reset()
    assert profiler.is_running == False
    assert profiler.last_session is None
