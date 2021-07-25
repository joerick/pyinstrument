import asyncio
import json
import time
from functools import partial
from test.fake_time_util import fake_time
from typing import Generator, Optional

import pytest
import trio

from pyinstrument import Profiler, renderers
from pyinstrument.frame import BaseFrame, Frame
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
