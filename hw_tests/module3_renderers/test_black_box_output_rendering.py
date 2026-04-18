from __future__ import annotations

import json
import marshal

import pytest

from pyinstrument import renderers
from pyinstrument.renderers.session import SessionRenderer

from .conftest import dummy_session


def test_console_renderer_equivalence_classes_text_output(renderer_session):
    """
    黑盒-等价类:
    选择 text renderer 的两个主要等价类:
    - 普通树形输出
    - flat 输出
    验证用户可见文本都能稳定包含关键函数名与目标描述。
    """
    normal_output = renderers.ConsoleRenderer(unicode=False, color=False).render(renderer_session)
    flat_output = renderers.ConsoleRenderer(unicode=False, color=False, flat=True).render(
        renderer_session
    )

    assert "Renderer fixture" in normal_output
    assert "main" in normal_output
    assert "cleanup" in normal_output
    assert "render_report" in flat_output
    assert "cleanup" in flat_output


@pytest.mark.parametrize(
    ("time_mode", "expected_fragment"),
    [
        ("seconds", "0.399"),
        ("percent_of_total", "39.9%"),
    ],
)
def test_console_renderer_boundary_and_representation(
    renderer_session, time_mode, expected_fragment
):
    """
    黑盒-边界值:
    针对时间展示模式的边界输出进行验证。
    seconds 与 percent_of_total 是互斥等价类，也覆盖了数值格式边界。
    """
    output = renderers.ConsoleRenderer(
        unicode=False, color=False, time=time_mode, show_all=True
    ).render(renderer_session)

    assert expected_fragment in output


def test_json_renderer_schema_and_content(renderer_session):
    """
    黑盒-等价类:
    JSON 输出属于结构化文本类，验证顶层字段与根节点内容。
    """
    output = renderers.JSONRenderer(show_all=True).render(renderer_session)
    payload = json.loads(output)

    assert payload["target_description"] == "Renderer fixture"
    assert payload["sample_count"] == 8
    assert payload["root_frame"]["function"] == "<module>"
    assert any(child["function"] == "main" for child in payload["root_frame"]["children"])


def test_html_renderer_embeds_assets_and_session_data(renderer_session, html_resources_dir):
    """
    黑盒-决策表:
    决策条件:
    - 资源文件存在
    - session 有 root_frame
    期望结果:
    - 输出 HTML
    - 嵌入 JS/CSS
    - 含 sessionData 初始化脚本
    """
    output = renderers.HTMLRenderer().render(renderer_session)

    assert "<!DOCTYPE html>" in output
    assert "pyinstrumentHTMLRenderer.render" in output
    assert "const sessionData =" in output
    assert "Renderer fixture" in output
    assert (html_resources_dir / "app.js").exists()
    assert (html_resources_dir / "app.css").exists()


def test_speedscope_renderer_outputs_valid_profile(renderer_session):
    """
    黑盒-等价类:
    speedscope 输出是时间线 JSON，验证用户可消费的 schema 关键字段。
    """
    output = renderers.SpeedscopeRenderer(show_all=True).render(renderer_session)
    payload = json.loads(output)

    assert payload["$schema"] == "https://www.speedscope.app/file-format-schema.json"
    assert payload["profiles"][0]["type"] == "evented"
    assert payload["profiles"][0]["endValue"] == pytest.approx(renderer_session.duration)
    assert len(payload["shared"]["frames"]) >= 3


def test_pstats_renderer_round_trip_binary_output(renderer_session):
    """
    黑盒-等价类:
    pstats 输出属于二进制兼容格式，验证可以回解为 stats 字典。
    """
    output = renderers.PstatsRenderer(show_all=True).render(renderer_session)
    stats = marshal.loads(output.encode("utf-8", errors="surrogateescape"))

    assert stats
    assert any(frame_key[2] == "main" for frame_key in stats.keys())


def test_session_renderer_round_trip(renderer_session):
    """
    黑盒-边界值:
    session renderer 直接导出 session 元数据，验证无损 JSON 化。
    """
    payload = json.loads(SessionRenderer().render(renderer_session))

    assert payload["target_description"] == "Renderer fixture"
    assert payload["duration"] == pytest.approx(1.0)
    assert payload["sample_count"] == 8


def test_empty_profile_boundary_for_multiple_renderers():
    """
    黑盒-边界值:
    空 profile 是输出模块的关键边界场景。
    """
    session = dummy_session()

    console_output = renderers.ConsoleRenderer(unicode=False, color=False).render(session)
    json_output = json.loads(renderers.JSONRenderer().render(session))
    html_output = renderers.HTMLRenderer().render(session)

    assert "No samples were recorded." in console_output
    assert json_output["root_frame"] is None
    assert "const sessionData =" in html_output


def test_renderers_package_exports_public_api():
    """
    黑盒-决策表:
    当用户从 renderers 包导入公开 API 时，关键类应可见。
    """
    assert renderers.ConsoleRenderer is not None
    assert renderers.HTMLRenderer is not None
    assert renderers.JSONRenderer is not None
    assert renderers.PstatsRenderer is not None
    assert renderers.SessionRenderer is not None
    assert renderers.SpeedscopeRenderer is not None


def test_html_static_assets_are_non_empty(html_resources_dir):
    """
    黑盒-边界值:
    app.js/app.css 至少应存在且非空，否则 HTML renderer 无法完整工作。
    """
    app_js = (html_resources_dir / "app.js").read_text(encoding="utf-8")
    app_css = (html_resources_dir / "app.css").read_text(encoding="utf-8")

    assert "pyinstrumentHTMLRenderer" in app_js
    assert "background-color" in app_css
    assert len(app_js) > 1000
    assert len(app_css) > 1000
