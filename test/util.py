import asyncio
import os
import time
from typing import Generator, NoReturn

import trio
from flaky import flaky

from pyinstrument.frame import BaseFrame
from pyinstrument.profiler import Profiler

if "CI" in os.environ:
    # a decorator that allows some test flakyness in CI environments, presumably
    # due to contention. Useful for tests that rely on real time measurments.
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


async def async_wait(sync_time, async_time, profile=False, engine="asyncio"):
    # an async function that has both sync work and async work
    profiler = None

    if profile:
        profiler = Profiler()
        profiler.start()

    busy_wait(sync_time / 2)

    if engine == "asyncio":
        await asyncio.sleep(async_time)
    else:
        await trio.sleep(async_time)

    busy_wait(sync_time / 2)

    if profiler:
        profiler.stop()
        profiler.print(show_all=True)
        return profiler.last_session


def walk_frames(frame: BaseFrame) -> Generator[BaseFrame, None, None]:
    yield frame

    for f in frame.children:
        yield from walk_frames(f)
