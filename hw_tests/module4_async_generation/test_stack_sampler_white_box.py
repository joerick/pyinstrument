from __future__ import annotations

import contextvars
import inspect
import threading
from types import SimpleNamespace

import pytest

from pyinstrument import stack_sampler
from pyinstrument.low_level import stat_profile_python


class RecordingSubscriber:
    def __init__(self) -> None:
        self.calls = []

    def __call__(self, stack, duration, async_state):
        self.calls.append((stack, duration, async_state))


def _sample_frame():
    return inspect.currentframe()


def test_get_stack_sampler_is_thread_local():
    main_sampler = stack_sampler.get_stack_sampler()
    results = []

    def worker():
        worker_sampler = stack_sampler.get_stack_sampler()
        results.append(worker_sampler is stack_sampler.get_stack_sampler())
        results.append(worker_sampler is not main_sampler)

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()

    assert main_sampler is stack_sampler.get_stack_sampler()
    assert results == [True, True]


def test_subscribe_unsubscribe_and_duplicate_errors(monkeypatch: pytest.MonkeyPatch):
    sampler = stack_sampler.StackSampler()
    updates = []
    monkeypatch.setattr(sampler, "_update", lambda: updates.append("updated"))

    subscriber = RecordingSubscriber()
    sampler.subscribe(subscriber, desired_interval=0.01, use_async_context=True)

    assert stack_sampler.active_profiler_context_var.get() is subscriber
    assert updates == ["updated"]

    with pytest.raises(ValueError, match="already subscribed"):
        sampler.subscribe(subscriber, desired_interval=0.02, use_async_context=False)

    sampler.unsubscribe(subscriber)
    assert stack_sampler.active_profiler_context_var.get() is None
    assert updates == ["updated", "updated"]

    with pytest.raises(stack_sampler.StackSampler.SubscriberNotFound):
        sampler.unsubscribe(subscriber)


def test_subscribe_rejects_existing_async_context():
    sampler = stack_sampler.StackSampler()
    stack_sampler.active_profiler_context_var.set(object())

    with pytest.raises(RuntimeError, match="already a profiler running"):
        sampler.subscribe(lambda *_: None, desired_interval=0.01, use_async_context=True)


def test_update_empty_and_single_subscriber_paths(monkeypatch: pytest.MonkeyPatch):
    sampler = stack_sampler.StackSampler()
    calls = []

    monkeypatch.setattr(sampler, "_stop_sampling", lambda: calls.append(("stop",)))
    sampler._update()
    assert calls == [("stop",)]

    def fake_start_sampling(interval, use_timing_thread):
        calls.append((interval, use_timing_thread))
        sampler.current_sampling_interval = interval

    monkeypatch.setattr(sampler, "_start_sampling", fake_start_sampling)
    sampler.subscribers = [
        stack_sampler.StackSamplerSubscriber(
            target=lambda *_: None,
            desired_interval=0.03,
            bound_to_async_context=False,
            async_state=None,
            use_timing_thread=None,
        )
    ]
    sampler._update()
    sampler._update()

    assert calls == [("stop",), (0.03, False)]


def test_update_rejects_conflicting_timing_thread_preferences():
    sampler = stack_sampler.StackSampler()
    sampler.subscribers = [
        stack_sampler.StackSamplerSubscriber(
            target=lambda *_: None,
            desired_interval=0.01,
            bound_to_async_context=False,
            async_state=None,
            use_timing_thread=True,
        ),
        stack_sampler.StackSamplerSubscriber(
            target=lambda *_: None,
            desired_interval=0.02,
            bound_to_async_context=False,
            async_state=None,
            use_timing_thread=False,
        ),
    ]

    with pytest.raises(ValueError, match="different timing thread preferences"):
        sampler._update()


def test_start_sampling_chooses_expected_timer_type(monkeypatch: pytest.MonkeyPatch):
    sampler = stack_sampler.StackSampler()
    calls = []

    monkeypatch.setattr(stack_sampler, "setstatprofile", lambda **kwargs: calls.append(kwargs))
    monkeypatch.setattr(stack_sampler, "timing_overhead", lambda: {})
    monkeypatch.setattr(stack_sampler, "walltime_coarse_resolution", lambda: 0.01)
    monkeypatch.setattr(sampler, "_timer", lambda: 123.0)

    sampler._start_sampling(interval=0.02, use_timing_thread=False)
    assert calls[-1]["timer_type"] == "walltime_coarse"
    assert sampler.current_sampling_interval == 0.02
    assert sampler.last_profile_time == 123.0

    sampler.timer_func = lambda: 77.0
    sampler.last_profile_time = 0.0
    sampler._start_sampling(interval=0.02, use_timing_thread=False)
    assert calls[-1]["timer_type"] == "timer_func"

    sampler.timer_func = None
    monkeypatch.setattr(stack_sampler, "walltime_coarse_resolution", lambda: None)
    sampler._start_sampling(interval=0.02, use_timing_thread=False)
    assert calls[-1]["timer_type"] == "walltime"

    sampler._start_sampling(interval=0.02, use_timing_thread=True)
    assert calls[-1]["timer_type"] == "walltime_thread"

    sampler.timer_func = lambda: 1.0
    with pytest.raises(ValueError, match="custom timer function"):
        sampler._start_sampling(interval=0.02, use_timing_thread=True)


def test_stop_sampling_and_timing_overhead_cache(monkeypatch: pytest.MonkeyPatch, capsys):
    sampler = stack_sampler.StackSampler()
    recorded = []

    monkeypatch.setattr(stack_sampler, "setstatprofile", lambda target=None, **_: recorded.append(target))
    with monkeypatch.context() as context:
        context.setattr(
            stack_sampler,
            "timing_overhead",
            lambda: {"walltime": 500e-9, "walltime_coarse": 100e-9},
        )
        context.setattr(stack_sampler, "walltime_coarse_resolution", lambda: 0.05)

        sampler._check_timing_overhead(interval=0.1, timer_type="walltime")
        sampler._check_timing_overhead(interval=0.1, timer_type="walltime")
        stderr = capsys.readouterr().err

        assert "timing thread option" in stderr
        assert "coarse" in stderr
        assert sampler.has_warned_about_timing_overhead is True

    sampler.current_sampling_interval = 0.01
    sampler.last_profile_time = 3.0
    sampler._stop_sampling()

    assert recorded == [None]
    assert sampler.current_sampling_interval is None
    assert sampler.last_profile_time == 0.0

    calls = {"count": 0}

    def fake_measure():
        calls["count"] += 1
        return {"walltime": 1.0}

    monkeypatch.setattr(stack_sampler, "measure_timing_overhead", fake_measure)
    stack_sampler._timing_overhead = None
    assert stack_sampler.timing_overhead() == {"walltime": 1.0}
    assert stack_sampler.timing_overhead() == {"walltime": 1.0}
    assert calls["count"] == 1


def test_check_timing_overhead_noop_paths(monkeypatch: pytest.MonkeyPatch):
    sampler = stack_sampler.StackSampler()
    sampler.has_warned_about_timing_overhead = True
    monkeypatch.setattr(stack_sampler, "timing_overhead", lambda: pytest.fail("should not measure"))
    sampler._check_timing_overhead(interval=0.1, timer_type="walltime")

    sampler.has_warned_about_timing_overhead = False
    monkeypatch.setattr(stack_sampler, "IGNORE_OVERHEAD_WARNING", True)
    sampler._check_timing_overhead(interval=0.1, timer_type="walltime")

    monkeypatch.setattr(stack_sampler, "IGNORE_OVERHEAD_WARNING", False)
    monkeypatch.setattr(stack_sampler, "timing_overhead", lambda: {})
    sampler._check_timing_overhead(interval=0.1, timer_type="walltime")


def test_sample_updates_async_state_and_dispatches(monkeypatch: pytest.MonkeyPatch):
    sampler = stack_sampler.StackSampler()
    old_subscriber = RecordingSubscriber()
    new_subscriber = RecordingSubscriber()
    frame = _sample_frame()
    assert frame is not None

    sampler.subscribers = [
        stack_sampler.StackSamplerSubscriber(
            target=old_subscriber,
            desired_interval=0.01,
            bound_to_async_context=True,
            async_state=stack_sampler.AsyncState("in_context"),
        ),
        stack_sampler.StackSamplerSubscriber(
            target=new_subscriber,
            desired_interval=0.01,
            bound_to_async_context=True,
            async_state=stack_sampler.AsyncState("out_of_context_unknown"),
        ),
    ]

    coroutine_stack = ["await-leaf"]
    sampler._sample(frame, "context_changed", (new_subscriber, old_subscriber, coroutine_stack))

    assert sampler.subscribers[0].async_state is not None
    assert sampler.subscribers[0].async_state.state == "out_of_context_awaited"
    assert sampler.subscribers[0].async_state.info[-1] == "await-leaf"
    assert sampler.subscribers[1].async_state == stack_sampler.AsyncState("in_context")

    sampler.subscribers[0].async_state = stack_sampler.AsyncState("out_of_context_unknown")
    monkeypatch.setattr(sampler, "_timer", lambda: 5.5)
    sampler.last_profile_time = 2.0

    sampler._sample(frame, "return", None)

    assert len(old_subscriber.calls) == 1
    stack, duration, async_state = old_subscriber.calls[0]
    assert duration == pytest.approx(3.5)
    assert async_state == stack_sampler.AsyncState("out_of_context_unknown")
    assert stack[0].endswith("\x00<thread>\x00%i" % threading.current_thread().ident)


def test_sample_context_change_without_coroutine_stack():
    sampler = stack_sampler.StackSampler()
    old_subscriber = RecordingSubscriber()
    frame = _sample_frame()
    assert frame is not None

    sampler.subscribers = [
        stack_sampler.StackSamplerSubscriber(
            target=old_subscriber,
            desired_interval=0.01,
            bound_to_async_context=True,
            async_state=stack_sampler.AsyncState("in_context"),
        )
    ]

    sampler._sample(frame, "context_changed", (None, old_subscriber, []))

    assert sampler.subscribers[0].async_state is not None
    assert sampler.subscribers[0].async_state.state == "out_of_context_unknown"


def test_timer_uses_custom_and_default_paths(monkeypatch: pytest.MonkeyPatch):
    sampler = stack_sampler.StackSampler()
    sampler.timer_func = lambda: 12.5
    assert sampler._timer() == 12.5

    sampler.timer_func = None
    monkeypatch.setattr(stack_sampler.timeit, "default_timer", lambda: 99.0)
    assert sampler._timer() == 99.0


def test_build_call_stack_for_call_and_c_return_events():
    frame = _sample_frame()
    assert frame is not None

    def builtin():
        return None

    call_stack = stack_sampler.build_call_stack(frame, "call", None)
    c_return_stack = stack_sampler.build_call_stack(frame, "c_return", builtin)

    assert call_stack[0].endswith("\x00<thread>\x00%i" % threading.current_thread().ident)
    assert any(entry.startswith("test_build_call_stack_for_call_and_c_return_events") for entry in call_stack)
    assert c_return_stack[0].endswith("\x00<thread>\x00%i" % threading.current_thread().ident)
    assert c_return_stack[-1].startswith("test_build_call_stack_for_call_and_c_return_events.<locals>.builtin")


def test_python_stat_profiler_timer_and_context_paths(monkeypatch: pytest.MonkeyPatch):
    context_var: contextvars.ContextVar[object | None] = contextvars.ContextVar("prof", default=None)
    events = []
    times = iter([0.0, 0.0, 0.5, 1.5])

    monkeypatch.setattr(stat_profile_python.timeit, "default_timer", lambda: next(times))

    profiler = stat_profile_python.PythonStatProfiler(
        target=lambda frame, event, arg: events.append((frame, event, arg)),
        interval=1.0,
        context_var=context_var,
        timer_type="walltime",
        timer_func=None,
    )

    fake_back = SimpleNamespace(
        f_code=SimpleNamespace(co_flags=0, co_name="caller", co_filename="caller.py", co_firstlineno=2),
        f_locals={},
        f_lineno=20,
        f_back=None,
    )
    fake_frame = SimpleNamespace(
        f_code=SimpleNamespace(co_flags=0x80, co_name="demo", co_filename="demo.py", co_firstlineno=1),
        f_locals={},
        f_lineno=10,
        f_back=fake_back,
    )

    context_var.set("new-context")
    profiler.profile(fake_frame, "return", None)
    assert profiler.await_stack

    context_var.set(None)
    profiler.profile(fake_frame, "call", None)

    assert events[0][1] == "context_changed"
    assert events[0][2][0] == "new-context"
    assert events[0][2][2] == []
    assert events[1][1] == "context_changed"
    assert events[1][2][2] is profiler.await_stack
    assert profiler.await_stack == []

    with pytest.raises(TypeError, match="not a context var"):
        stat_profile_python.PythonStatProfiler(
            target=lambda *_: None,
            interval=1.0,
            context_var="bad",  # type: ignore[arg-type]
            timer_type="walltime",
            timer_func=None,
        )

    with pytest.raises(TypeError, match="timer_func must be provided"):
        stat_profile_python.PythonStatProfiler(
            target=lambda *_: None,
            interval=1.0,
            context_var=None,
            timer_type="timer_func",
            timer_func=None,
        )

    with pytest.raises(ValueError, match="invalid timer_type"):
        stat_profile_python.PythonStatProfiler(
            target=lambda *_: None,
            interval=1.0,
            context_var=None,
            timer_type="walltime_coarse",  # type: ignore[arg-type]
            timer_func=None,
        )

    custom_timer = stat_profile_python.PythonStatProfiler(
        target=lambda *_: None,
        interval=1.0,
        context_var=None,
        timer_type="timer_func",
        timer_func=lambda: 3.0,
    )
    assert custom_timer.get_time() == 3.0

    no_context_events = []
    advancing_times = iter([0.0, 2.0])
    no_context_profiler = stat_profile_python.PythonStatProfiler(
        target=lambda frame, event, arg: no_context_events.append((frame, event, arg)),
        interval=1.0,
        context_var=None,
        timer_type="timer_func",
        timer_func=lambda: next(advancing_times),
    )
    no_context_profiler.profile(fake_frame, "return", "payload")

    assert no_context_events == [(fake_frame, "return", "payload")]


def test_python_stat_profiler_timing_thread_and_setstatprofile(monkeypatch: pytest.MonkeyPatch):
    state = {"subscribed": [], "unsubscribed": [], "profile_func": None}

    monkeypatch.setattr(
        stat_profile_python, "pyi_timing_thread_subscribe", lambda interval: state["subscribed"].append(interval) or 11
    )
    monkeypatch.setattr(
        stat_profile_python, "pyi_timing_thread_unsubscribe", lambda ident: state["unsubscribed"].append(ident)
    )
    monkeypatch.setattr(stat_profile_python, "pyi_timing_thread_get_time", lambda: 7.0)
    monkeypatch.setattr(stat_profile_python.sys, "setprofile", lambda func: state.__setitem__("profile_func", func))

    profiler = stat_profile_python.PythonStatProfiler(
        target=lambda *_: None,
        interval=0.1,
        context_var=None,
        timer_type="walltime_thread",
        timer_func=None,
    )
    profiler.__del__()

    assert state["subscribed"] == [0.1]
    assert state["unsubscribed"] == [11]

    stat_profile_python.setstatprofile(lambda *_: None, interval=0.2)
    assert state["profile_func"] is not None

    stat_profile_python.setstatprofile(None)
    assert state["profile_func"] is None


def test_get_frame_info_handles_self_cls_and_tracebackhide():
    class Demo:
        def instance_method(self):
            __tracebackhide__ = True
            return stat_profile_python.get_frame_info(inspect.currentframe())

        @classmethod
        def class_method(cls):
            return stat_profile_python.get_frame_info(inspect.currentframe())

    instance_info = Demo().instance_method()
    class_info = Demo.class_method()

    assert "\x01c" in instance_info
    assert "Demo" in instance_info
    assert "\x01h1" in instance_info
    assert "\x01l" in instance_info
    assert "\x01c" in class_info
    assert "Demo" in class_info
