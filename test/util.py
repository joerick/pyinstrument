import asyncio
import os
import time
from typing import Generator, Generic, Iterable, Iterator, NoReturn, Optional, TypeVar

import trio
from flaky import flaky

from pyinstrument.frame import SYNTHETIC_LEAF_IDENTIFIERS, Frame
from pyinstrument.profiler import Profiler

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
    busy_wait(0.25)


if __name__ == '__main__':
    main()
"""
