from __future__ import annotations

import json
import marshal
import warnings
from pathlib import Path
from typing import cast
from unittest.mock import patch

import pytest

from pyinstrument import processors, renderers
from pyinstrument.frame import SELF_TIME_FRAME_IDENTIFIER, Frame, FrameGroup
from pyinstrument.frame_ops import FrameRecordType
from pyinstrument.renderers.base import FrameRenderer, Renderer
from pyinstrument.renderers.html import JSONForHTMLRenderer
from pyinstrument.renderers.speedscope import SpeedscopeEncoder, SpeedscopeEventType

from .conftest import calculate_frame_tree_times, dummy_session, self_time_frame


def test_frame_renderer_processor_configuration_coverage():
    """
    白盒-代码覆盖:
    覆盖 FrameRenderer.__init__ 中的两个核心分支:
    - show_all 删除隐藏类处理器
    - timeline 删除 aggregate_repeated_calls
    """
    renderer = renderers.ConsoleRenderer(show_all=True, timeline=True)

    assert processors.aggregate_repeated_calls not in renderer.processors
    assert processors.group_library_frames_processor not in renderer.processors
    assert processors.remove_importlib not in renderer.processors
    assert processors.remove_irrelevant_nodes not in renderer.processors


def test_renderer_base_not_implemented_branches():
    class DummyRenderer(Renderer):
        pass

    class DummyFrameRenderer(FrameRenderer):
        pass

    with pytest.raises(NotImplementedError):
        DummyRenderer().render(dummy_session())

    with pytest.raises(NotImplementedError):
        DummyFrameRenderer().default_processors()

    with pytest.raises(NotImplementedError):
        DummyFrameRenderer().render(dummy_session())


def test_console_renderer_misconfiguration_basic_path():
    """
    白盒-基本路径覆盖:
    flat=True 且 timeline=True 会走到异常路径。
    """
    with pytest.raises(Renderer.MisconfigurationError):
        renderers.ConsoleRenderer(flat=True, timeline=True)


def test_console_renderer_short_mode_and_unicode_group_rendering():
    session = dummy_session()
    session.sys_path = ["D:/workspace", "env/Lib/site-packages"]
    session.sys_prefixes = ["env"]

    exit_frame = Frame(
        identifier_or_frame_info="callback\x00D:/workspace/app.py\x0030",
        children=[self_time_frame(0.12)],
    )
    hidden_leaf_2 = Frame(
        identifier_or_frame_info="leaf2\x00env/Lib/site-packages/pkg/sub2.py\x0020",
        children=[self_time_frame(0.03), exit_frame],
    )
    hidden_leaf_1 = Frame(
        identifier_or_frame_info="leaf1\x00env/Lib/site-packages/pkg/sub1.py\x0015",
        children=[self_time_frame(0.03), hidden_leaf_2],
    )
    group_root = Frame(
        identifier_or_frame_info="lib_root\x00env/Lib/site-packages/pkg/core.py\x0010",
        children=[hidden_leaf_1, self_time_frame(0.01)],
    )
    root = Frame(
        identifier_or_frame_info="<module>\x00D:/workspace/app.py\x001",
        children=[
            group_root,
            Frame("cleanup\x00D:/workspace/app.py\x0040", children=[self_time_frame(0.2)]),
        ],
        context=session,
    )
    calculate_frame_tree_times(root)
    processors.group_library_frames_processor(root, options={})
    session.root_frame = lambda trim_stem=True: root  # type: ignore[method-assign]

    renderer = renderers.ConsoleRenderer(unicode=True, color=False, short_mode=True, show_all=False)
    renderer.root_frame = root
    output = renderer.render_frame(root, precision=3)

    assert "frames hidden" in output
    assert group_root.group is not None
    group_description = renderer.group_description(group_root.group)
    assert "frames hidden" in group_description
    assert any(token in group_description for token in ("env", "pkg"))
    assert "." * 53 in renderer.render(session)


def test_console_renderer_hidden_group_child_and_misc_branches():
    session = dummy_session()
    session.sys_path = ["D:/workspace", "env/Lib/site-packages"]
    session.sys_prefixes = ["env"]

    visible_exit = Frame("visible\x00D:/workspace/app.py\x0030", children=[self_time_frame(0.01)])
    hidden_c = Frame(
        "hidden_c\x00env/Lib/site-packages/pkg/c.py\x0025",
        children=[self_time_frame(0.01), visible_exit],
    )
    hidden_a = Frame(
        identifier_or_frame_info="hidden_a\x00env/Lib/site-packages/pkg/a.py\x0010",
        children=[Frame("hidden_b\x00env/Lib/site-packages/pkg/b.py\x0020", children=[hidden_c])],
    )
    root = Frame(
        "<module>\x00D:/workspace/app.py\x001",
        children=[
            hidden_a,
            Frame("cleanup\x00D:/workspace/app.py\x0040", children=[self_time_frame(1.0)]),
        ],
        context=session,
    )
    calculate_frame_tree_times(root)
    processors.group_library_frames_processor(root, options={})
    group = hidden_a.group
    assert group is not None

    renderer = renderers.ConsoleRenderer(unicode=False, color=True)
    renderer.root_frame = root

    hidden_child = hidden_a.children[0]
    assert renderer.should_render_frame(hidden_child) is False
    assert "hidden_b" not in renderer.render_frame(hidden_child, precision=3)
    assert renderer._ansi_color_for_time(0.7 * root.time) == renderer.colors.red
    assert renderer._ansi_color_for_time(0.3 * root.time) == renderer.colors.yellow
    assert renderer._ansi_color_for_time(0.1 * root.time) == renderer.colors.green
    assert renderer._ansi_color_for_time(0.001 * root.time) == (
        renderer.colors.bright_green + renderer.colors.faint
    )
    assert renderer._ansi_color_for_name(visible_exit) == (
        renderer.colors.bg_dark_blue_255 + renderer.colors.white_255
    )
    assert renderer.frame_description(
        Frame(SELF_TIME_FRAME_IDENTIFIER, time=0.1), precision=3
    ).endswith("  ")
    classed = Frame(
        "method\x00D:/workspace/app.py\x0040\x01cWidget",
        children=[self_time_frame(0.2)],
        context=session,
    )
    calculate_frame_tree_times(classed)
    renderer.root_frame = classed
    assert "Widget.method" in renderer.frame_description(classed, precision=3)


def test_console_renderer_should_ignore_small_group():
    session = dummy_session()
    session.sys_path = ["D:/workspace", "env/Lib/site-packages"]
    session.sys_prefixes = ["env"]
    group_root = Frame(
        "lib\x00env/Lib/site-packages/pkg/a.py\x001",
        children=[
            Frame("leaf\x00env/Lib/site-packages/pkg/b.py\x002", children=[self_time_frame(0.01)])
        ],
    )
    root = Frame("<module>\x00D:/workspace/app.py\x001", children=[group_root], context=session)
    calculate_frame_tree_times(root)
    processors.group_library_frames_processor(root, options={})

    renderer = renderers.ConsoleRenderer()
    renderer.root_frame = root
    assert group_root.group is not None
    assert renderer.should_ignore_group(group_root.group) is True


def test_console_renderer_zero_time_branch(renderer_tree):
    """
    白盒-代码覆盖:
    覆盖 frame_proportion_of_total_time 中 root_frame.time == 0 的分支。
    """
    renderer = renderers.ConsoleRenderer(unicode=False, color=False)
    renderer.root_frame = renderer_tree
    renderer.root_frame.time = 0

    assert renderer.frame_proportion_of_total_time(0.123) == 1


def test_html_renderer_deprecation_warnings():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        renderers.HTMLRenderer(show_all=True, timeline=True)

    messages = [str(w.message) for w in caught]
    assert any("show_all option is deprecated" in m for m in messages)
    assert any("timeline is deprecated" in m for m in messages)


def test_html_renderer_missing_resources_branch(renderer_session):
    """
    白盒-基本路径覆盖:
    覆盖 HTMLRenderer.render 中资源缺失的异常分支。
    """
    original_exists = Path.exists

    def fake_exists(path: Path) -> bool:
        if path.name in {"app.js", "app.css"}:
            return False
        return original_exists(path)

    with patch("pathlib.Path.exists", new=fake_exists):
        with pytest.raises(RuntimeError, match="Could not find app.js / app.css"):
            renderers.HTMLRenderer().render(renderer_session)


def test_html_renderer_resample_interval_zero_skips_resampling(capsys):
    session = dummy_session()
    session.duration = 2.0
    session.sample_count = 100001
    session.start_call_stack = ["leaf\x00pkg/b.py\x002"]
    session.frame_records = cast(
        list[FrameRecordType],
        [(["leaf\x00pkg/b.py\x002"], 1e-6)] * 100001,
    )

    output = renderers.HTMLRenderer(resample_interval=0).render(session)
    captured = capsys.readouterr()

    assert "const sessionData =" in output
    assert "Resampled to" not in captured.err


def test_html_renderer_resample_branch_coverage(capsys):
    """
    白盒-代码覆盖:
    覆盖 HTMLRenderer.render 的自动重采样路径。
    """
    session = dummy_session()
    session.duration = 1.0001
    session.sample_count = 100001
    session.frame_records = cast(
        list[FrameRecordType],
        [(["<module>\x00pkg/a.py\x001"], 1e-9)] * 100000 + [(["leaf\x00pkg/b.py\x002"], 1)],
    )
    session.start_call_stack = ["leaf\x00pkg/b.py\x002"]

    output = renderers.HTMLRenderer().render(session)
    captured = capsys.readouterr()

    assert "const sessionData =" in output
    assert "Resampled to" in captured.err


def test_html_renderer_multiple_resample_iterations(capsys):
    session = dummy_session()
    session.duration = 10.0
    session.sample_count = 200000
    session.start_call_stack = ["leaf\x00pkg/b.py\x002"]
    session.frame_records = cast(
        list[FrameRecordType],
        [(["leaf\x00pkg/b.py\x002"], 1e-6)] * 200000,
    )

    huge = dummy_session()
    huge.start_call_stack = session.start_call_stack
    huge.frame_records = cast(
        list[FrameRecordType],
        [(["leaf\x00pkg/b.py\x002"], 1e-6)] * 150000,
    )
    huge.duration = 10.0
    small = dummy_session()
    small.start_call_stack = session.start_call_stack
    small.frame_records = cast(
        list[FrameRecordType],
        [(["leaf\x00pkg/b.py\x002"], 1e-6)] * 50000,
    )
    small.duration = 10.0

    with patch.object(type(session), "resample", side_effect=[huge, small]) as mock_resample:
        renderers.HTMLRenderer().render(session)

    captured = capsys.readouterr()
    assert mock_resample.call_count == 2
    assert "Resampled to 50000 samples" in captured.err


def test_html_renderer_open_in_browser_both_paths(renderer_session, tmp_path):
    renderer = renderers.HTMLRenderer()
    explicit_output = tmp_path / "report.html"

    with patch("webbrowser.open") as mock_open:
        returned = renderer.open_in_browser(renderer_session, output_filename=str(explicit_output))
    assert returned == str(explicit_output)
    assert explicit_output.read_text(encoding="utf-8").startswith("<!DOCTYPE html>")
    mock_open.assert_called_once()

    with patch("webbrowser.open") as mock_open:
        returned = renderer.open_in_browser(renderer_session)
    assert returned.endswith(".html")
    assert Path(returned).exists()
    mock_open.assert_called_once()
    Path(returned).unlink()


def test_processors_remove_first_pyinstrument_frames_positive_path():
    """
    白盒-基本路径覆盖:
    命中 remove_first_pyinstrument_frames_processor 的完整裁剪路径。
    """
    session = dummy_session()
    root = Frame(
        identifier_or_frame_info="<module>\x00D:/repo/pyinstrument/__main__.py\x001",
        children=[
            Frame(
                identifier_or_frame_info="<module>\x00<string>\x001",
                children=[
                    Frame(
                        identifier_or_frame_info="<module>\x00<frozen runpy>\x001",
                        children=[
                            Frame(
                                identifier_or_frame_info="user_main\x00D:/workspace/user.py\x0010",
                                children=[self_time_frame(0.3)],
                            )
                        ],
                    )
                ],
            )
        ],
        context=session,
    )
    calculate_frame_tree_times(root)

    trimmed = processors.remove_first_pyinstrument_frames_processor(root, options={})

    assert trimmed is not None
    assert trimmed.function == "user_main"
    assert trimmed.parent is None


def test_processors_remove_first_pyinstrument_frames_negative_path():
    """
    白盒-基本路径覆盖:
    未命中 pyinstrument 启动栈时，应直接返回原 frame。
    """
    session = dummy_session()
    root = Frame(
        identifier_or_frame_info="<module>\x00D:/workspace/app.py\x001",
        children=[Frame("main\x00D:/workspace/app.py\x0010", children=[self_time_frame(0.1)])],
        context=session,
    )
    calculate_frame_tree_times(root)

    result = processors.remove_first_pyinstrument_frames_processor(root, options={})

    assert result is root


def test_processors_core_mutation_branches():
    session = dummy_session()
    root = Frame(
        identifier_or_frame_info="<module>\x00D:/workspace/app.py\x001",
        children=[
            Frame(
                identifier_or_frame_info="import_bootstrap\x00../<frozen importlib._bootstrap>\x0010",
                children=[
                    Frame("inner\x00D:/workspace/real.py\x0020", children=[self_time_frame(0.1)])
                ],
            ),
            Frame(
                identifier_or_frame_info="hide_me\x00D:/workspace/hide.py\x0010\x01h1",
                children=[
                    Frame("visible\x00D:/workspace/real.py\x0020", children=[self_time_frame(0.1)])
                ],
            ),
            Frame(
                identifier_or_frame_info="repeat\x00D:/workspace/r.py\x0010",
                children=[self_time_frame(0.1)],
            ),
            Frame(
                identifier_or_frame_info="repeat\x00D:/workspace/r.py\x0010",
                children=[self_time_frame(0.2)],
            ),
            self_time_frame(0.05),
            self_time_frame(0.07),
        ],
        context=session,
    )
    calculate_frame_tree_times(root)

    processors.remove_importlib(root, options={})
    processors.remove_tracebackhide(root, options={})
    processors.aggregate_repeated_calls(root, options={})
    processors.merge_consecutive_self_time(root, options={})

    assert any(child.function == "inner" for child in root.children)
    assert any(child.function == "visible" for child in root.children)
    assert sum(1 for child in root.children if child.function == "repeat") == 1
    assert any(
        child.identifier == SELF_TIME_FRAME_IDENTIFIER and child.time == pytest.approx(0.12)
        for child in root.children
    )


def test_group_library_frames_show_rule_overrides_hide_rule():
    """
    白盒-数据流分析:
    验证 hide_regex 与 show_regex 同时命中时，show 优先。
    """
    session = dummy_session()
    session.sys_path = ["D:/workspace", "env/Lib/site-packages"]
    session.sys_prefixes = ["env"]

    root = Frame(
        identifier_or_frame_info="<module>\x00D:/workspace/app.py\x001",
        children=[
            Frame(
                identifier_or_frame_info="hidden_lib\x00env/Lib/site-packages/pkg/a.py\x0010",
                children=[
                    Frame(
                        identifier_or_frame_info="still_visible\x00env/Lib/site-packages/pkg/show_me.py\x0020",
                        children=[self_time_frame(0.2)],
                    ),
                    Frame(
                        identifier_or_frame_info="hidden_child\x00env/Lib/site-packages/pkg/hide_me.py\x0030",
                        children=[self_time_frame(0.2)],
                    ),
                ],
            )
        ],
        context=session,
    )
    calculate_frame_tree_times(root)

    processed = processors.group_library_frames_processor(
        root,
        options={
            "hide_regex": r".*site-packages.*",
            "show_regex": r".*show_me\.py",
        },
    )

    assert processed is not None
    group_root = processed.children[0]
    assert group_root.group is not None
    shown_child = group_root.children[0]
    hidden_child = group_root.children[1]
    assert shown_child.group is None
    assert hidden_child.group is group_root.group


def test_processors_remove_first_pyinstrument_frames_exec_mismatch():
    session = dummy_session()
    root = Frame(
        identifier_or_frame_info="<module>\x00D:/repo/pyinstrument/__main__.py\x001",
        children=[Frame("not_exec\x00D:/workspace/user.py\x0010", children=[self_time_frame(0.2)])],
        context=session,
    )
    calculate_frame_tree_times(root)

    assert processors.remove_first_pyinstrument_frames_processor(root, options={}) is root


def test_remove_irrelevant_nodes_zero_total_time_branch():
    """
    白盒-代码覆盖:
    覆盖 total_time <= 0 时的保护分支，确保不会除零。
    """
    session = dummy_session()
    root = Frame(
        identifier_or_frame_info="<module>\x00D:/workspace/app.py\x001",
        children=[Frame("tiny\x00D:/workspace/app.py\x0010", children=[self_time_frame(0.0)])],
        context=session,
    )
    calculate_frame_tree_times(root)
    root.time = 0

    processed = processors.remove_irrelevant_nodes(root, options={"filter_threshold": 0.5})

    assert processed is not None
    assert len(processed.children) == 0


def test_json_renderer_group_and_class_name_branches():
    session = dummy_session()
    frame = Frame(
        "method\x00D:/workspace/app.py\x0010\x01cWidget",
        children=[self_time_frame(0.2)],
        context=session,
    )
    calculate_frame_tree_times(frame)
    group = FrameGroup(frame)
    session.root_frame = lambda trim_stem=True: frame  # type: ignore[method-assign]

    payload = json.loads(JSONForHTMLRenderer().render(session))
    rendered = json.loads(renderers.JSONRenderer(show_all=True).render(session))

    assert payload["frame_tree"]["identifier"].startswith("method")
    assert rendered["root_frame"]["group_id"] == group.id
    assert rendered["root_frame"]["class_name"] == "Widget"


def test_pstats_renderer_none_and_existing_entry_branches():
    renderer = renderers.PstatsRenderer(show_all=True)
    stats = {}
    renderer.render_frame(None, stats)
    assert stats == {}

    session = dummy_session()
    root = Frame("<module>\x00D:/workspace/app.py\x001", children=[], context=session)
    child = Frame(
        "main\x00D:/workspace/app.py\x0010", children=[self_time_frame(0.2)], context=session
    )
    root.add_child(child)
    calculate_frame_tree_times(root)

    renderer.render_frame(child, stats)
    renderer.render_frame(child, stats)

    key = renderer.frame_key(child)
    parent_key = renderer.frame_key(root)
    assert stats[key][2] == pytest.approx(0.4)
    assert stats[key][4][parent_key][2] == pytest.approx(0.4)


def test_speedscope_renderer_data_flow_open_close_balance(renderer_session):
    """
    白盒-数据流分析:
    验证 render_frame 生成的事件流中 OPEN/CLOSE 成对出现，且 frame 索引可回溯。
    """
    payload = json.loads(renderers.SpeedscopeRenderer(show_all=True).render(renderer_session))
    events = payload["profiles"][0]["events"]

    stack = []
    for event in events:
        if event["type"] == SpeedscopeEventType.OPEN.value:
            stack.append(event["frame"])
        else:
            assert stack.pop() == event["frame"]

    assert stack == []


def test_speedscope_encoder_and_render_frame_extra_branches():
    renderer = renderers.SpeedscopeRenderer(show_all=True)
    assert renderer.render_frame(None) == []

    session = dummy_session()
    frame = Frame(
        "repeat\x00D:/workspace/app.py\x0010", children=[self_time_frame(0.2)], context=session
    )
    calculate_frame_tree_times(frame)

    first = renderer.render_frame(frame)
    second = renderer.render_frame(frame)
    assert first[0].frame == second[0].frame

    with pytest.raises(TypeError):
        json.dumps(object(), cls=SpeedscopeEncoder)


def test_pstats_renderer_skips_synthetic_children_data_flow():
    """
    白盒-数据流分析:
    render_frame 在遍历 children 时会跳过 synthetic child。
    """
    session = dummy_session()
    root = Frame(
        identifier_or_frame_info="<module>\x00D:/workspace/app.py\x001",
        children=[
            Frame(
                identifier_or_frame_info="main\x00D:/workspace/app.py\x0010",
                children=[
                    self_time_frame(0.2),
                    Frame(
                        identifier_or_frame_info="worker\x00D:/workspace/worker.py\x0020",
                        children=[self_time_frame(0.1)],
                    ),
                ],
            )
        ],
        context=session,
    )
    calculate_frame_tree_times(root)
    session.root_frame = lambda trim_stem=True: root  # type: ignore[method-assign]

    output = renderers.PstatsRenderer(show_all=True).render(session)
    stats = json.loads(
        json.dumps(list(marshal.loads(output.encode("utf-8", errors="surrogateescape")).keys()))
    )

    flat_names = {item[2] for item in stats}
    assert "main" in flat_names
    assert "worker" in flat_names
    assert "[self]" not in flat_names
