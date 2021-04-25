import contextvars
import sys
import time

import pytest

from pyinstrument import stack_sampler

from .util import do_nothing


@pytest.fixture(autouse=True)
def check_sampler_state():
    yield

    assert sys.getprofile() is None
    assert len(stack_sampler.get_stack_sampler().subscribers) == 0
    stack_sampler.thread_locals.__dict__.clear()


def test_create():
    sampler = stack_sampler.get_stack_sampler()
    assert sampler is not None

    assert sampler is stack_sampler.get_stack_sampler()


def test_get_samples():
    sampler = stack_sampler.get_stack_sampler()

    sample_count = 0

    def sample_observer(stack, time, await_stack):
        nonlocal sample_count
        sample_count += 1

    assert sys.getprofile() is None
    sampler.subscribe(sample_observer, 0.001)
    assert sys.getprofile() is not None
    assert len(sampler.subscribers) == 1

    start = time.time()
    while time.time() < start + 1 and sample_count == 0:
        do_nothing()

    assert sample_count > 0

    assert sys.getprofile() is not None
    sampler.unsubscribe(sample_observer)
    assert sys.getprofile() is None

    assert len(sampler.subscribers) == 0


def test_multiple_samplers():
    sampler = stack_sampler.get_stack_sampler()

    class SampleCounter:
        count = 0

        def sample(self, stack, time, await_stack):
            self.count += 1

    counter_1 = SampleCounter()
    counter_2 = SampleCounter()

    context_1 = contextvars.copy_context()
    context_2 = contextvars.copy_context()

    assert sys.getprofile() is None
    assert len(sampler.subscribers) == 0
    context_1.run(sampler.subscribe, counter_1.sample, 0.001)
    context_2.run(sampler.subscribe, counter_2.sample, 0.001)

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
