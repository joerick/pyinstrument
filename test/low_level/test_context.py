from __future__ import annotations

import contextvars
import time
from typing import Any

import pytest

from ..util import busy_wait
from .util import parametrize_setstatprofile


@parametrize_setstatprofile
def test_context_type(setstatprofile):
    with pytest.raises(TypeError):
        setstatprofile(lambda f, e, a: 0, 1e6, "not a context var")
        setstatprofile(None)


profiler_context_var: contextvars.ContextVar[object | None] = contextvars.ContextVar(
    "profiler_context_var", default=None
)


@parametrize_setstatprofile
def test_context_tracking(setstatprofile):
    profile_calls = []

    def profile_callback(frame, event, arg):
        nonlocal profile_calls
        profile_calls.append((frame, event, arg))

    profiler_1 = object()
    profiler_2 = object()

    context_1 = contextvars.copy_context()
    context_2 = contextvars.copy_context()

    context_1.run(profiler_context_var.set, profiler_1)
    context_2.run(profiler_context_var.set, profiler_2)

    setstatprofile(
        profile_callback,
        1e10,  # set large interval so we only get context_change events
        profiler_context_var,
    )

    context_1.run(busy_wait, 0.001)
    context_2.run(busy_wait, 0.001)

    setstatprofile(None)

    assert all(c[1] == "context_changed" for c in profile_calls)
    assert len(profile_calls) == 4

    new, old, _ = profile_calls[0][2]
    assert old is None
    assert new is profiler_1

    new, old, _ = profile_calls[1][2]
    assert old is profiler_1
    assert new is None

    new, old, _ = profile_calls[2][2]
    assert old is None
    assert new is profiler_2

    new, old, _ = profile_calls[3][2]
    assert old is profiler_2
    assert new is None
