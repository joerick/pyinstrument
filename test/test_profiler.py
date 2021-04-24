from __future__ import print_function
import asyncio
from pyinstrument.frame import Frame
from pyinstrument.session import ProfilerSession
import time, json, trio
from typing import Generator, Optional
from functools import partial

import pytest
from pyinstrument import Profiler, renderers
from .util import assert_never, flaky_in_ci, busy_wait

# Utilities #


def long_function_a():
    time.sleep(0.25)


def long_function_b():
    time.sleep(0.5)


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


def walk_frames(frame: Frame) -> Generator[Frame, None, None]:
    yield frame

    for f in frame.children:
        yield from walk_frames(f)


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

    assert text_output.count("test_collapses_multiple_calls_by_default") == 1
    assert text_output.count("long_function_a") == 1
    assert text_output.count("long_function_b") == 1


# this test can be flaky on CI, because it's not deterministic when the
# setstatprofile timer will fire. Sometimes the profiler.start frame is
# included.
@flaky_in_ci
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
    assert frame.function == "test_profiler_retains_multiple_calls"
    assert len(frame.children) == 4


@flaky_in_ci
def test_two_functions():
    profiler = Profiler()
    profiler.start()

    long_function_a()
    long_function_b()

    profiler.stop()

    print(profiler.output_text())

    frame = profiler.last_session.root_frame()

    assert frame.function == "test_two_functions"
    assert len(frame.children) == 2

    frame_b, frame_a = sorted(frame.children, key=lambda f: f.time(), reverse=True)

    assert frame_a.function == "long_function_a"
    assert frame_b.function == "long_function_b"

    # busy CI runners can be slow to wake up from the sleep. So we relax the
    # ranges a bit
    assert frame_a.time() == pytest.approx(0.25, abs=0.1)
    assert frame_b.time() == pytest.approx(0.5, abs=0.2)


@flaky_in_ci
def test_context_manager():
    with Profiler() as profiler:
        long_function_a()
        long_function_b()

    frame = profiler.last_session.root_frame()
    assert frame.function == "test_context_manager"
    assert len(frame.children) == 2


@flaky_in_ci
def test_json_output():
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
    assert profiler.last_session.duration == pytest.approx(0.1, rel=0.1)

    # test a second session, does it merge with the first?
    profiler.start()

    assert profiler.is_running == True
    busy_wait(0.1)

    profiler.stop()

    assert profiler.is_running == False

    assert profiler.last_session is not None
    assert profiler.last_session.duration == pytest.approx(0.2, rel=0.1)

    # test a reset
    profiler.reset()
    assert profiler.last_session is None

    # test a reset while running
    profiler.start()
    assert profiler.is_running == True
    profiler.reset()
    assert profiler.is_running == False
    assert profiler.last_session is None


@flaky_in_ci
@pytest.mark.parametrize("engine", ["asyncio", "trio"])
def test_async(engine):
    profiler_session: Optional[ProfilerSession] = None

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
    fake_work_frame = next(f for f in walk_frames(root_frame) if f.function == "async_wait")
    assert fake_work_frame.time() == pytest.approx(0.1 + 0.5, rel=0.1)
