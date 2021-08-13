import contextvars
import sys
import time

import pytest

from pyinstrument import stack_sampler

from .util import do_nothing


class SampleCounter:
    count = 0

    def sample(self, stack, time, async_state):
        self.count += 1


def test_create():
    sampler = stack_sampler.get_stack_sampler()
    assert sampler is not None

    assert sampler is stack_sampler.get_stack_sampler()


def test_get_samples():
    sampler = stack_sampler.get_stack_sampler()
    counter = SampleCounter()

    assert sys.getprofile() is None
    sampler.subscribe(counter.sample, desired_interval=0.001, use_async_context=True)
    assert sys.getprofile() is not None
    assert len(sampler.subscribers) == 1

    start = time.time()
    while time.time() < start + 1 and counter.count == 0:
        do_nothing()

    assert counter.count > 0

    assert sys.getprofile() is not None
    sampler.unsubscribe(counter.sample)
    assert sys.getprofile() is None

    assert len(sampler.subscribers) == 0


def test_multiple_samplers():
    sampler = stack_sampler.get_stack_sampler()
    counter_1 = SampleCounter()
    counter_2 = SampleCounter()

    sampler.subscribe(counter_1.sample, desired_interval=0.001, use_async_context=False)
    sampler.subscribe(counter_2.sample, desired_interval=0.001, use_async_context=False)

    assert len(sampler.subscribers) == 2

    start = time.time()
    while time.time() < start + 1 and counter_1.count == 0 and counter_2.count == 0:
        do_nothing()

    assert counter_1.count > 0
    assert counter_2.count > 0

    assert sys.getprofile() is not None

    sampler.unsubscribe(counter_1.sample)
    sampler.unsubscribe(counter_2.sample)

    assert sys.getprofile() is None

    assert len(sampler.subscribers) == 0


def test_multiple_samplers_async_error():
    sampler = stack_sampler.get_stack_sampler()

    counter_1 = SampleCounter()
    counter_2 = SampleCounter()

    sampler.subscribe(counter_1.sample, desired_interval=0.001, use_async_context=True)

    with pytest.raises(RuntimeError):
        sampler.subscribe(counter_2.sample, desired_interval=0.001, use_async_context=True)

    sampler.unsubscribe(counter_1.sample)


def test_multiple_contexts():
    sampler = stack_sampler.get_stack_sampler()

    counter_1 = SampleCounter()
    counter_2 = SampleCounter()

    context_1 = contextvars.copy_context()
    context_2 = contextvars.copy_context()

    assert sys.getprofile() is None
    assert len(sampler.subscribers) == 0
    context_1.run(sampler.subscribe, counter_1.sample, 0.001, True)
    context_2.run(sampler.subscribe, counter_2.sample, 0.001, True)

    assert sys.getprofile() is not None
    assert len(sampler.subscribers) == 2

    start = time.time()
    while time.time() < start + 1 and counter_1.count == 0 and counter_2.count == 0:
        do_nothing()

    assert counter_1.count > 0
    assert counter_2.count > 0

    assert sys.getprofile() is not None

    context_1.run(sampler.unsubscribe, counter_1.sample)
    context_2.run(sampler.unsubscribe, counter_2.sample)

    assert sys.getprofile() is None

    assert len(sampler.subscribers) == 0
