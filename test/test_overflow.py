from __future__ import print_function
import time, sys, inspect
import pytest
from pyinstrument import Profiler
from pyinstrument.renderers import JSONRenderer, ConsoleRenderer, HTMLRenderer

# Utilities

def recurse(depth):
    if depth == 0:
        time.sleep(0.1)
        return

    recurse(depth - 1)

def current_stack_depth():
    depth = 0
    frame = inspect.currentframe()
    while frame:
        frame = frame.f_back
        depth += 1
    return depth

# Fixtures

@pytest.fixture(scope="module")
def deep_profiler_session():
    profiler = Profiler()
    profiler.start()

    # give 120 frames for pyinstrument to do its work.
    recursion_depth = sys.getrecursionlimit() - current_stack_depth() - 120
    recurse(recursion_depth)

    profiler.stop()
    return profiler.last_session

# Tests

def test_console(deep_profiler_session):
    ConsoleRenderer().render(deep_profiler_session)

# html now uses the json renderer, so it's xfail too.
def test_html(deep_profiler_session):
    HTMLRenderer().render(deep_profiler_session)

def test_json(deep_profiler_session):
    JSONRenderer().render(deep_profiler_session)
