from __future__ import annotations

from pathlib import Path
import sys

import pytest

from pyinstrument.frame import SELF_TIME_FRAME_IDENTIFIER, SYNTHETIC_LEAF_IDENTIFIERS, Frame
from pyinstrument.session import Session


def self_time_frame(time: float) -> Frame:
    return Frame(SELF_TIME_FRAME_IDENTIFIER, time=time)


def calculate_frame_tree_times(frame: Frame):
    child_time_sum = 0.0

    for child in frame.children:
        if child.identifier not in SYNTHETIC_LEAF_IDENTIFIERS:
            calculate_frame_tree_times(child)

        child_time_sum += child.time

    frame.time = child_time_sum + frame.absorbed_time


def dummy_session() -> Session:
    return Session(
        frame_records=[],
        start_time=0,
        min_interval=0.1,
        max_interval=0.1,
        duration=0,
        sample_count=0,
        start_call_stack=[],
        target_description="dummy",
        cpu_time=0,
        sys_path=sys.path,
        sys_prefixes=Session.current_sys_prefixes(),
    )


def make_renderer_session():
    """
    Shared fixture data for output/rendering tests.

    The tree contains:
    - application frames
    - library frames
    - repeated calls
    - a tiny frame used for filtering/boundary tests
    """
    session = dummy_session()
    session.start_time = 1710000000.0
    session.duration = 1.0
    session.sample_count = 8
    session.cpu_time = 0.8
    session.min_interval = 0.001
    session.max_interval = 0.001
    session.target_description = "Renderer fixture"
    session.sys_path = ["D:/workspace", "env/Lib/site-packages"]
    session.sys_prefixes = ["env"]

    root = Frame(
        identifier_or_frame_info="<module>\x00D:/workspace/app.py\x001",
        children=[
            Frame(
                identifier_or_frame_info="main\x00D:/workspace/app.py\x0010",
                children=[
                    self_time_frame(0.1),
                    Frame(
                        identifier_or_frame_info="render_report\x00D:/workspace/report.py\x0020",
                        children=[self_time_frame(0.3)],
                    ),
                    Frame(
                        identifier_or_frame_info="lib_entry\x00env/Lib/site-packages/pkg/core.py\x0030",
                        children=[
                            Frame(
                                identifier_or_frame_info="lib_leaf\x00env/Lib/site-packages/pkg/helpers.py\x0040",
                                children=[self_time_frame(0.2)],
                            )
                        ],
                    ),
                    Frame(
                        identifier_or_frame_info="tiny_step\x00D:/workspace/tiny.py\x0050",
                        children=[self_time_frame(0.001)],
                    ),
                ],
            ),
            Frame(
                identifier_or_frame_info="cleanup\x00D:/workspace/app.py\x0060",
                children=[self_time_frame(0.399)],
            ),
        ],
        context=session,
    )

    calculate_frame_tree_times(root)
    root.self_check()

    session.root_frame = lambda trim_stem=True: root  # type: ignore[method-assign]
    return session, root


@pytest.fixture
def renderer_session():
    return make_renderer_session()[0]


@pytest.fixture
def renderer_tree():
    return make_renderer_session()[1]


@pytest.fixture
def html_resources_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "pyinstrument" / "renderers" / "html_resources"
