# some tests for the renderer classes

from __future__ import annotations

import time

import pytest

from pyinstrument import renderers
from pyinstrument.profiler import Profiler

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
