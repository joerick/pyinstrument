from __future__ import print_function
import time

from pyinstrument import Profiler

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

def test_aggregator_collapses_multiple_calls():
    profiler = Profiler()
    profiler.start()

    long_function_a()
    long_function_b()
    long_function_a()
    long_function_b()

    profiler.stop()

    print(profiler.output_text())

    frame = profiler.first_interesting_frame()
    assert frame.function == 'test_aggregator_collapses_multiple_calls'
    assert len(frame.children) == 2

def test_timeline_retains_multiple_calls():
    profiler = Profiler(recorder='timeline')
    profiler.start()

    long_function_a()
    long_function_b()
    long_function_a()
    long_function_b()

    profiler.stop()

    print(profiler.output_text())

    frame = profiler.first_interesting_frame()
    assert frame.function == 'test_timeline_retains_multiple_calls'
    assert len(frame.children) == 4

def test_two_functions():
    profiler = Profiler()
    profiler.start()

    long_function_a()
    long_function_b()

    profiler.stop()

    print(profiler.output_text())

    frame = profiler.first_interesting_frame()

    assert frame.function == 'test_two_functions'
    assert len(frame.children) == 2

    frame_b, frame_a = frame.children

    assert frame_a.function == 'long_function_a'
    assert frame_b.function == 'long_function_b'
    assert 0.2 < frame_a.time() < 0.3
    assert 0.45 < frame_b.time() < 0.55
