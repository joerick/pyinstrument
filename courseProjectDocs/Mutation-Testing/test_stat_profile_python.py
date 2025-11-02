import types
import contextvars
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

    previous_frame = MagicMock(spec=types.FrameType)
    frame = MagicMock(spec=types.FrameType)
    frame.f_back = previous_frame
    event = "call"

    old_value = ctx_var.get()
    ctx_var.set('new_value')
    profiler.last_context_var_value = old_value

    profiler.profile(frame, event, None)

    # Check that target was called at least once
    assert target.call_count > 0

    args, kwargs = target.call_args

    # First argument is a frame
    assert isinstance(args[0], type(frame))
    # Second argument is an event
    assert args[1] in ("call", "context_changed")

    # Third argument may be None, check before iterating
    if args[2] is not None:
        new_val, old_val, await_stack = args[2]
        assert new_val == 'new_value'
        assert old_val == old_value
        assert isinstance(await_stack, list)

    # Second mutation event
    event_mutante = "CALL"
    profiler.last_context_var_value = old_value
    ctx_var.set('another_value')

    profiler.profile(frame, event_mutante, None)

    args2, kwargs2 = target.call_args

    if args2[2] is not None:
        new_val2, old_val2, await_stack2 = args2[2]
        assert new_val2 == 'another_value'
        assert old_val2 == old_value
        assert isinstance(await_stack2, list)
