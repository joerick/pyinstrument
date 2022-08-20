import asyncio
import sys
import time
from functools import partial
from test.fake_time_util import fake_time, fake_time_asyncio, fake_time_trio
from typing import Optional

import greenlet
import pytest
import trio
import trio._core._run
import trio.lowlevel

from pyinstrument import processors, stack_sampler
from pyinstrument.frame import AWAIT_FRAME_IDENTIFIER, OUT_OF_CONTEXT_FRAME_IDENTIFIER, Frame
from pyinstrument.profiler import Profiler
from pyinstrument.session import Session

from .util import assert_never, flaky_in_ci, walk_frames

# Utilities #


@pytest.fixture(autouse=True)
def tidy_up_stack_sampler():
    assert sys.getprofile() is None
    assert len(stack_sampler.get_stack_sampler().subscribers) == 0

    yield

    assert sys.getprofile() is None
    assert len(stack_sampler.get_stack_sampler().subscribers) == 0
    stack_sampler.thread_locals.__dict__.clear()


# Tests #


@pytest.mark.asyncio
async def test_sleep():
    profiler = Profiler()

    with fake_time_asyncio():
        profiler.start()

        await asyncio.sleep(0.2)

        session = profiler.stop()

    assert len(session.frame_records) > 0

    root_frame = session.root_frame()
    assert root_frame

    assert root_frame.time == pytest.approx(0.2, rel=0.1)
    assert root_frame.await_time() == pytest.approx(0.2, rel=0.1)

    sleep_frame = next(f for f in walk_frames(root_frame) if f.function == "sleep")
    assert sleep_frame.time == pytest.approx(0.2, rel=0.1)
    assert sleep_frame.time == pytest.approx(0.2, rel=0.1)


def test_sleep_trio():
    async def run():
        profiler = Profiler()
        profiler.start()

        await trio.sleep(0.2)

        session = profiler.stop()
        assert len(session.frame_records) > 0

        root_frame = session.root_frame()
        assert root_frame

        assert root_frame.time == pytest.approx(0.2)
        assert root_frame.await_time() == pytest.approx(0.2)

        sleep_frame = next(f for f in walk_frames(root_frame) if f.function == "sleep")
        assert sleep_frame.time == pytest.approx(0.2)
        assert sleep_frame.time == pytest.approx(0.2)

    with fake_time_trio() as fake_clock:
        trio.run(run, clock=fake_clock.trio_clock)


@flaky_in_ci
@pytest.mark.parametrize("engine", ["asyncio", "trio"])
def test_profiler_task_isolation(engine):
    profiler_session: Optional[Session] = None

    async def async_wait(sync_time, async_time, profile=False, engine="asyncio"):
        # an async function that has both sync work and async work
        profiler = None

        if profile:
            profiler = Profiler()
            profiler.start()

        time.sleep(sync_time / 2)

        if engine == "asyncio":
            await asyncio.sleep(async_time)
        else:
            await trio.sleep(async_time)

        time.sleep(sync_time / 2)

        if profiler:
            profiler.stop()
            profiler.print(show_all=True)
            return profiler.last_session

    if engine == "asyncio":
        loop = asyncio.new_event_loop()

        with fake_time_asyncio(loop):
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

        with fake_time_trio() as fake_clock:
            trio.run(multi_task, clock=fake_clock.trio_clock)
    else:
        assert_never(engine)

    assert profiler_session

    root_frame = profiler_session.root_frame()
    assert root_frame is not None
    fake_work_frame = next(f for f in walk_frames(root_frame) if f.function == "async_wait")
    assert fake_work_frame.time == pytest.approx(0.1 + 0.5, rel=0.1)

    root_frame = processors.aggregate_repeated_calls(root_frame, {})
    assert root_frame

    await_frames = [f for f in walk_frames(root_frame) if f.identifier == AWAIT_FRAME_IDENTIFIER]

    assert sum(f.await_time() for f in await_frames) == pytest.approx(0.5, rel=0.1)
    assert sum(f.time for f in await_frames) == pytest.approx(0.5, rel=0.1)


def test_greenlet():
    profiler = Profiler()

    with fake_time():
        profiler.start()

        def y(duration):
            time.sleep(duration)

        y(0.1)
        greenlet.greenlet(y).switch(0.1)

        session = profiler.stop()

    profiler.print()

    root_frame = session.root_frame()
    assert root_frame

    assert root_frame.time == pytest.approx(0.2, rel=0.1)

    sleep_frames = [f for f in walk_frames(root_frame) if f.function == "sleep"]
    assert len(sleep_frames) == 2
    assert sleep_frames[0].time == pytest.approx(0.1, rel=0.1)
    assert sleep_frames[1].time == pytest.approx(0.1, rel=0.1)


def test_strict_with_greenlet():
    profiler = Profiler(async_mode="strict")

    with fake_time():
        profiler.start()

        def y(duration):
            time.sleep(duration)

        y(0.1)
        greenlet.greenlet(y).switch(0.1)

        session = profiler.stop()

    profiler.print()

    root_frame = session.root_frame()
    assert root_frame

    assert root_frame.time == pytest.approx(0.2, rel=0.1)

    sleep_frames = [f for f in walk_frames(root_frame) if f.function == "sleep"]
    assert len(sleep_frames) == 1
    assert sleep_frames[0].time == pytest.approx(0.1, rel=0.1)

    greenlet_frames = [
        f for f in walk_frames(root_frame) if f.identifier == OUT_OF_CONTEXT_FRAME_IDENTIFIER
    ]

    assert len(greenlet_frames) == 1
    assert greenlet_frames[0].time == pytest.approx(0.1, rel=0.1)
