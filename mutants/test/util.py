import asyncio
import os
import sys
import time
from typing import Callable, Generator, Generic, Iterable, Iterator, NoReturn, Optional, TypeVar

from flaky import flaky

from pyinstrument import stack_sampler
from pyinstrument.frame import SYNTHETIC_LEAF_IDENTIFIERS, Frame
from pyinstrument.profiler import Profiler
from pyinstrument.session import Session

if "CI" in os.environ:
    # a decorator that allows some test flakiness in CI environments, presumably
    # due to contention. Useful for tests that rely on real time measurements.
    flaky_in_ci = flaky(max_runs=5, min_passes=1)
else:
    flaky_in_ci = lambda a: a


def assert_never(x: NoReturn) -> NoReturn:
    raise AssertionError(f"Invalid value: {x!r}")


def do_nothing():
    pass


def busy_wait(duration):
    end_time = time.time() + duration

    while time.time() < end_time:
        do_nothing()


def walk_frames(frame: Frame) -> Generator[Frame, None, None]:
    yield frame

    for f in frame.children:
        yield from walk_frames(f)


T = TypeVar("T")


def first(iterator: Iterator[T]) -> Optional[T]:
    try:
        return next(iterator)
    except StopIteration:
        return None


def calculate_frame_tree_times(frame: Frame):
    # assuming that the leaf nodes of a frame tree have correct, time values,
    # calculate the times of all nodes in the frame tree

    child_time_sum = 0.0

    for child in frame.children:
        if child.identifier not in SYNTHETIC_LEAF_IDENTIFIERS:
            calculate_frame_tree_times(child)

        child_time_sum += child.time

    frame.time = child_time_sum + frame.absorbed_time


BUSY_WAIT_SCRIPT = """
import time, sys

def do_nothing():
    pass

def busy_wait(duration):
    end_time = time.time() + duration

    while time.time() < end_time:
        do_nothing()

def main():
    print('sys.argv: ', sys.argv)
    busy_wait(0.1)


if __name__ == '__main__':
    main()
"""


def dummy_session() -> Session:
    return Session(
        frame_records=[],
        start_time=0,
        min_interval=0.1,
        max_interval=0.1,
        duration=0,
        sample_count=0,
        start_call_stack=[],
        target_description="dummy",
        cpu_time=0,
        sys_path=sys.path,
        sys_prefixes=Session.current_sys_prefixes(),
    )


def tidy_up_profiler_state_on_fail(func: Callable) -> Callable[[], None]:
    """
    Useful inside a test that's flaky in CI, where the check_sampler_state
    fixture only gets to run at the end of all flaky attempts.
    """
    # consider adding to the flasky_in_ci decorator if it's useful elsewhere

    def wrapped():
        try:
            func()
        except BaseException:
            sys.setprofile(None)
            stack_sampler.thread_locals.__dict__.clear()
            raise

    return wrapped
