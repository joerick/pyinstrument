import asyncio
import contextlib
import functools
import random
from unittest import mock

from trio.testing import MockClock

from pyinstrument import stack_sampler


class FakeClock:
    def __init__(self) -> None:
        self.time = random.random() * 1e6

    def get_time(self):
        return self.time

    def sleep(self, duration):
        self.time += duration


@contextlib.contextmanager
def fake_time(fake_clock=None):
    fake_clock = fake_clock or FakeClock()
    stack_sampler.get_stack_sampler().timer_func = fake_clock.get_time

    try:
        with mock.patch("time.sleep", new=fake_clock.sleep):
            yield fake_clock
    finally:
        stack_sampler.get_stack_sampler().timer_func = None


class FakeClockAsyncio:
    # this implementation mostly lifted from
    # https://aiotools.readthedocs.io/en/latest/_modules/aiotools/timer.html#VirtualClock
    # License: https://github.com/achimnol/aiotools/blob/800f7f1bce086b0c83658bad8377e6cb1908e22f/LICENSE
    # Copyright (c) 2017 Joongi Kim
    def __init__(self) -> None:
        self.time = random.random() * 1e6

    def get_time(self):
        return self.time

    def sleep(self, duration):
        self.time += duration

    def _virtual_select(self, orig_select, timeout):
        self.time += timeout
        return orig_select(0)  # override the timeout to zero


@contextlib.contextmanager
def fake_time_asyncio(loop=None):
    loop = loop or asyncio.get_running_loop()
    fake_clock = FakeClockAsyncio()

    # fmt: off
    with mock.patch.object(
        loop._selector,  # type: ignore
        "select",
        new=functools.partial(fake_clock._virtual_select, loop._selector.select),  # type: ignore
    ), mock.patch.object(
        loop,
        "time",
        new=fake_clock.get_time
    ), fake_time(fake_clock):
        yield fake_clock
    # fmt: on


class FakeClockTrio:
    def __init__(self, clock: MockClock) -> None:
        self.trio_clock = clock

    def get_time(self):
        return self.trio_clock.current_time()

    def sleep(self, duration):
        self.trio_clock.jump(duration)


@contextlib.contextmanager
def fake_time_trio():
    trio_clock = MockClock(autojump_threshold=0)
    fake_clock = FakeClockTrio(trio_clock)

    with fake_time(fake_clock):
        yield fake_clock
