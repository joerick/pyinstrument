import types
import contextvars
import pytest
from unittest.mock import MagicMock
from pyinstrument.low_level.stat_profile_python import PythonStatProfiler

def test_context_change_frame_handling():
    target = MagicMock()

    ctx_var = contextvars.ContextVar('test')
    ctx_var.set('initial_value')
    profiler = PythonStatProfiler(
        target=target,
        interval=0.001,
        context_var=ctx_var,
        timer_type="walltime",
        timer_func=None
    )

    frame = MagicMock(spec=types.FrameType)
    frame.f_back = 'previous_frame'
    event = "call"

    old_value = ctx_var.get()
    ctx_var.set('new_value')
    profiler.last_context_var_value = old_value

    profiler.profile(frame, event, None)

    target.assert_called_with('previous_frame', "context_changed", (
        'new_value', old_value, profiler.await_stack))

    event_mutante = "CALL"
    profiler.last_context_var_value = old_value
    ctx_var.set('another_value')

    profiler.profile(frame, event_mutante, None)

    target.assert_called_with(frame, "context_changed", (
        'another_value', old_value, profiler.await_stack))
