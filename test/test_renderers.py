# some tests for the renderer classes

from __future__ import annotations

import sys
import time
from unittest.mock import patch

import pytest

from pyinstrument import renderers
from pyinstrument.profiler import Profiler
from pyinstrument.session import Session

from .fake_time_util import fake_time

# utils

frame_renderer_classes: list[type[renderers.FrameRenderer]] = [
    renderers.ConsoleRenderer,
    renderers.JSONRenderer,
    renderers.PstatsRenderer,
    renderers.SpeedscopeRenderer,
]

parametrize_frame_renderer_class = pytest.mark.parametrize(
    "frame_renderer_class", frame_renderer_classes, ids=lambda c: c.__name__
)

# fixtures


def a():
    b()
    c()


def b():
    d()


def c():
    d()


def d():
    e()


def e():
    time.sleep(1)


@pytest.fixture(scope="module")
def profiler_session():
    with fake_time():
        profiler = Profiler()
        profiler.start()

        a()

        profiler.stop()
        return profiler.last_session


# tests


@parametrize_frame_renderer_class
def test_empty_profile(frame_renderer_class: type[renderers.FrameRenderer]):
    with Profiler() as profiler:
        pass
    profiler.output(renderer=frame_renderer_class())


@parametrize_frame_renderer_class
def test_timeline_doesnt_crash(
    profiler_session, frame_renderer_class: type[renderers.FrameRenderer]
):
    renderer = frame_renderer_class(timeline=True)
    renderer.render(profiler_session)


@parametrize_frame_renderer_class
def test_show_all_doesnt_crash(
    profiler_session, frame_renderer_class: type[renderers.FrameRenderer]
):
    renderer = frame_renderer_class(show_all=True)
    renderer.render(profiler_session)


@pytest.mark.parametrize("flat_time", ["self", "total"])
def test_console_renderer_flat_doesnt_crash(profiler_session, flat_time):
    renderer = renderers.ConsoleRenderer(flat=True, flat_time=flat_time)
    renderer.render(profiler_session)


def test_html_renderer_resampling(capsys):
    # create a session with more than 100,000 samples
    frame_records = []
    # first 100,000 frames have almost no time in them
    frame_records += [("<module>\x00somemodule/__init__.py\x0012", 1e-9)] * 100_000
    # last frame has some time in it
    frame_records += [("a\x00b\x001", 1)]

    session = Session(
        duration=1.0001,
        start_time=0,
        frame_records=frame_records,
        sample_count=len(frame_records),
        min_interval=1e-9,
        max_interval=1e-9,
        start_call_stack=["<module>\x00somemodule/__init__.py\x0012"],
        target_description="test",
        cpu_time=1.0001,
        sys_path=sys.path,
        sys_prefixes=[],
    )

    renderer = renderers.HTMLRenderer()
    with patch("pyinstrument.session.Session._resample_frame_records") as mock_resample:
        renderer.render(session)

    captured = capsys.readouterr()
    assert "Resampled to" in captured.err
    assert mock_resample.called
