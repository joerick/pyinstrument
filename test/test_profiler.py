from __future__ import print_function
import time, json

import pytest
from pyinstrument import Profiler, renderers
from flaky import flaky

# Utilities #

def do_nothing():
    pass

def busy_wait(duration):
    end_time = time.time() + duration

    while time.time() < end_time:
        do_nothing()

def long_function_a():
    time.sleep(0.25)

def long_function_b():
    time.sleep(0.5)

# Tests #

def test_collapses_multiple_calls_by_default():
    profiler = Profiler()
    profiler.start()

    long_function_a()
    long_function_b()
    long_function_a()
    long_function_b()

    profiler.stop()

    text_output = profiler.output_text()

    # output should be something like:
    # 1.513 test_collapses_multiple_calls_by_default  test/test_profiler.py:25
    # |- 0.507 long_function_a  test/test_profiler.py:17
    # |- 0.503 long_function_b  test/test_profiler.py:20

    assert text_output.count('test_collapses_multiple_calls_by_default') == 1
    assert text_output.count('long_function_a') == 1
    assert text_output.count('long_function_b') == 1

# this test can be flaky on CI, because it's not deterministic when the
# setstatprofile timer will fire. Sometimes the profiler.start frame is
# included.
@flaky(max_runs=5, min_passes=2)
def test_profiler_retains_multiple_calls():
    profiler = Profiler()
    profiler.start()

    long_function_a()
    long_function_b()
    long_function_a()
    long_function_b()

    profiler.stop()

    print(profiler.output_text())

    frame = profiler.last_session.root_frame()
    assert frame.function == 'test_profiler_retains_multiple_calls'
    assert len(frame.children) == 4

@flaky(max_runs=5, min_passes=2)
def test_two_functions():
    profiler = Profiler()
    profiler.start()

    long_function_a()
    long_function_b()

    profiler.stop()

    print(profiler.output_text())

    frame = profiler.last_session.root_frame()

    assert frame.function == 'test_two_functions'
    assert len(frame.children) == 2

    frame_b, frame_a = sorted(frame.children, key=lambda f: f.time(), reverse=True)

    assert frame_a.function == 'long_function_a'
    assert frame_b.function == 'long_function_b'

    # busy CI runners can be slow to wake up from the sleep. So we relax the
    # ranges a bit
    assert frame_a.time() == pytest.approx(0.25, abs=0.1)
    assert frame_b.time() == pytest.approx(0.5, abs=0.2)

@flaky(max_runs=5, min_passes=2)
def test_context_manager():
    with Profiler() as profiler:
        long_function_a()
        long_function_b()

    frame = profiler.last_session.root_frame()
    assert frame.function == 'test_context_manager'
    assert len(frame.children) == 2

@flaky(max_runs=5, min_passes=2)
def test_json_output():
    with Profiler() as profiler:
        long_function_a()
        long_function_b()

    output_data = profiler.output(renderers.JSONRenderer())

    output = json.loads(output_data)
    assert 'root_frame' in output

    root_frame = output['root_frame']

    assert root_frame['function'] == 'test_json_output'
    assert len(root_frame['children']) == 2

def test_empty_profile():
    with Profiler() as profiler:
        pass
    profiler.output(renderer=renderers.ConsoleRenderer())
