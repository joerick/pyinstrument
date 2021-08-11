import sys

import pytest

from pyinstrument import stack_sampler


@pytest.fixture(autouse=True)
def check_sampler_state():
    assert sys.getprofile() is None
    assert len(stack_sampler.get_stack_sampler().subscribers) == 0

    try:
        yield
        assert sys.getprofile() is None
        assert len(stack_sampler.get_stack_sampler().subscribers) == 0
    finally:
        sys.setprofile(None)
        stack_sampler.thread_locals.__dict__.clear()
