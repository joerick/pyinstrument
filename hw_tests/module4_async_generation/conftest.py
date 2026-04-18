from __future__ import annotations

import sys

import pytest

from pyinstrument import stack_sampler


@pytest.fixture(autouse=True)
def reset_stack_sampler_state():
    sampler = stack_sampler.get_stack_sampler()
    sampler.subscribers.clear()
    sampler.current_sampling_interval = None
    sampler.last_profile_time = 0.0
    sampler.timer_func = None
    sampler.has_warned_about_timing_overhead = False
    stack_sampler.thread_locals.__dict__.clear()
    stack_sampler.active_profiler_context_var.set(None)
    stack_sampler._timing_overhead = None
    sys.setprofile(None)

    yield

    sys.setprofile(None)
    sampler = stack_sampler.get_stack_sampler()
    sampler.subscribers.clear()
    sampler.current_sampling_interval = None
    sampler.last_profile_time = 0.0
    sampler.timer_func = None
    sampler.has_warned_about_timing_overhead = False
    stack_sampler.thread_locals.__dict__.clear()
    stack_sampler.active_profiler_context_var.set(None)
    stack_sampler._timing_overhead = None
