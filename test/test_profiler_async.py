import asyncio
import time
from functools import partial
from typing import Optional

import greenlet
import pytest
import trio

from pyinstrument import processors
from pyinstrument.frame import AwaitTimeFrame, OutOfContextFrame
from pyinstrument.profiler import Profiler
from pyinstrument.session import Session

from .util import assert_never, async_wait, flaky_in_ci, walk_frames

# Utilities #


# Tests #


@flaky_in_ci
@pytest.mark.asyncio
async def test_sleep():
    profiler = Profiler()
    profiler.start()

    await asyncio.sleep(0.2)

    session = profiler.stop()
    root_frame = session.root_frame()
    assert root_frame

    assert root_frame.time() == pytest.approx(0.2, rel=0.1)
    assert root_frame.await_time() == pytest.approx(0.2, rel=0.1)

    sleep_frame = next(f for f in walk_frames(root_frame) if f.function == "sleep")
    assert sleep_frame.time() == pytest.approx(0.2, rel=0.1)
    assert sleep_frame.time() == pytest.approx(0.2, rel=0.1)


@flaky_in_ci
@pytest.mark.parametrize("engine", ["asyncio", "trio"])
def test_async_engines(engine):
    profiler_session: Optional[Session] = None

    if engine == "asyncio":
        loop = asyncio.new_event_loop()

        profile_task = loop.create_task(async_wait(sync_time=0.1, async_time=0.5, profile=True))
        loop.create_task(async_wait(sync_time=0.1, async_time=0.3))
        loop.create_task(async_wait(sync_time=0.1, async_time=0.3))

        loop.run_until_complete(profile_task)
        loop.close()

        profiler_session = profile_task.result()
    elif engine == "trio":

        async def async_wait_and_capture(**kwargs):
            nonlocal profiler_session
            profiler_session = await async_wait(**kwargs)

        async def multi_task():
            async with trio.open_nursery() as nursery:
                nursery.start_soon(
                    partial(
                        async_wait_and_capture,
                        sync_time=0.1,
                        async_time=0.5,
                        engine="trio",
                        profile=True,
                    )
                )
                nursery.start_soon(
                    partial(async_wait, sync_time=0.1, async_time=0.3, engine="trio")
                )
                nursery.start_soon(
                    partial(async_wait, sync_time=0.1, async_time=0.3, engine="trio")
                )

        trio.run(multi_task)
    else:
        assert_never(engine)

    assert profiler_session
    assert profiler_session.duration == pytest.approx(0.1 + 0.5, rel=0.1)

    root_frame = profiler_session.root_frame()
    assert root_frame is not None
    fake_work_frame = next(f for f in walk_frames(root_frame) if f.function == "async_wait")
    assert fake_work_frame.time() == pytest.approx(0.1 + 0.5, rel=0.1)

    root_frame = processors.aggregate_repeated_calls(root_frame, {})
    assert root_frame

    await_frames = [f for f in walk_frames(root_frame) if isinstance(f, AwaitTimeFrame)]

    assert sum(f.self_time for f in await_frames) == pytest.approx(0.5, rel=0.1)
    assert sum(f.time() for f in await_frames) == pytest.approx(0.5, rel=0.1)


def test_greenlet():
    profiler = Profiler()
    profiler.start()

    def y(duration):
        time.sleep(duration)

    y(0.1)
    greenlet.greenlet(y).switch(0.1)

    session = profiler.stop()
    profiler.print()

    root_frame = session.root_frame()
    assert root_frame

    assert root_frame.time() == pytest.approx(0.2, rel=0.1)

    sleep_frames = [f for f in walk_frames(root_frame) if f.function == "sleep"]
    assert len(sleep_frames) == 2
    assert sleep_frames[0].time() == pytest.approx(0.1, rel=0.1)
    assert sleep_frames[1].time() == pytest.approx(0.1, rel=0.1)


def test_strict_with_greenlet():
    profiler = Profiler(async_mode="strict")
    profiler.start()

    def y(duration):
        time.sleep(duration)

    y(0.1)
    greenlet.greenlet(y).switch(0.1)

    session = profiler.stop()
    profiler.print()

    root_frame = session.root_frame()
    assert root_frame

    assert root_frame.time() == pytest.approx(0.2, rel=0.1)

    sleep_frames = [f for f in walk_frames(root_frame) if f.function == "sleep"]
    assert len(sleep_frames) == 1
    assert sleep_frames[0].time() == pytest.approx(0.1, rel=0.1)

    out_of_context_frames = [f for f in walk_frames(root_frame) if isinstance(f, OutOfContextFrame)]
    assert len(out_of_context_frames) == 1
    assert out_of_context_frames[0].time() == pytest.approx(0.1, rel=0.1)
