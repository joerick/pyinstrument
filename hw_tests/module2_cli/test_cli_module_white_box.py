from __future__ import annotations

import json
import os
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest

from pyinstrument import renderers
from pyinstrument.__main__ import (
    OptionsParseError,
    compute_render_options,
    create_renderer,
    get_renderer_class,
    guess_renderer_from_outfile,
    load_report_from_temp_storage,
    main,
    report_dir,
    save_report_to_temp_storage,
)
from pyinstrument.frame import AWAIT_FRAME_IDENTIFIER, OUT_OF_CONTEXT_FRAME_IDENTIFIER
from pyinstrument.profiler import ActiveProfilerSession, Profiler
from pyinstrument.session import Session
from pyinstrument.util import (
    file_is_a_tty,
    file_supports_color,
    file_supports_unicode,
    format_float_with_sig_figs,
    object_with_import_path,
    strtobool,
)
from pyinstrument.vendor import appdirs, keypath


def make_options(**overrides):
    defaults = dict(
        hide_fnmatch=None,
        hide_regex=None,
        show_fnmatch=None,
        show_regex=None,
        show_all=False,
        unicode=None,
        color=None,
        timeline=False,
        render_options=None,
        output_html=False,
        outfile=None,
        renderer=None,
        load=None,
        load_prev=None,
        module=None,
        program=None,
        target_description="Program: {args}",
        interval=0.001,
        use_timing_thread=None,
        from_path=None,
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def dummy_session(start_time: float = 1.0, sys_path: list[str] | None = None) -> Session:
    return Session(
        frame_records=[(["root"], 0.1)],
        start_time=start_time,
        duration=0.1,
        min_interval=0.001,
        max_interval=0.001,
        sample_count=1,
        start_call_stack=["root"],
        target_description="dummy",
        cpu_time=0.05,
        sys_path=sys_path or ["project", "site-packages"],
        sys_prefixes=["prefix"],
    )


def workspace_temp_dir() -> Path:
    path = Path(__file__).parent / ".artifacts" / uuid4().hex
    path.mkdir(parents=True, exist_ok=True)
    return path


class DummyFile:
    def __init__(self, *, encoding="utf-8", isatty=False):
        self.encoding = encoding
        self._isatty = isatty
        self._parts: list[str] = []

    def isatty(self):
        return self._isatty

    def write(self, text: str):
        self._parts.append(text)
        return len(text)

    def getvalue(self) -> str:
        return "".join(self._parts)


def test_compute_render_options_supports_equivalence_classes():
    options = make_options(
        hide_fnmatch="*/site-packages/*",
        show_fnmatch="*/project/*",
        timeline=True,
        render_options=[
            "processor_options.filter_threshold=0.2",
            "unicode",
            'processor_options.extra={"limit": 5}',
        ],
    )

    result = compute_render_options(
        options,
        renderer_class=renderers.ConsoleRenderer,
        unicode_support=False,
        color_support=True,
    )

    assert result["timeline"] is True
    assert result["unicode"] is True
    assert result["color"] is True
    assert result["processor_options"]["hide_regex"]
    assert result["processor_options"]["show_regex"]
    assert result["processor_options"]["filter_threshold"] == 0.2
    assert result["processor_options"]["extra"] == {"limit": 5}


def test_compute_render_options_rejects_invalid_decision_table_combinations():
    with pytest.raises(OptionsParseError):
        compute_render_options(
            make_options(hide_fnmatch="*.py", hide_regex=".*"),
            renderer_class=renderers.ConsoleRenderer,
            unicode_support=False,
            color_support=False,
        )

    with pytest.raises(OptionsParseError):
        compute_render_options(
            make_options(show_fnmatch="*.py", show_regex=".*"),
            renderer_class=renderers.ConsoleRenderer,
            unicode_support=False,
            color_support=False,
        )


def test_get_renderer_class_and_outfile_boundaries():
    assert guess_renderer_from_outfile("report.txt") == "text"
    assert guess_renderer_from_outfile("REPORT.HTML") == "html"
    assert guess_renderer_from_outfile("trace.speedscope.json") == "speedscope"
    assert guess_renderer_from_outfile("session.pyisession") == "session"
    assert guess_renderer_from_outfile("stats.pstats") == "pstats"
    assert guess_renderer_from_outfile("unknown.bin") is None

    assert get_renderer_class(make_options(outfile="report.html")) is renderers.HTMLRenderer
    assert get_renderer_class(make_options(renderer="json")) is renderers.JSONRenderer

    with pytest.raises(OptionsParseError):
        get_renderer_class(make_options(renderer="not_a_valid_renderer"))


def test_create_renderer_reports_bad_option_names():
    with pytest.raises(OptionsParseError):
        create_renderer(
            renderers.ConsoleRenderer,
            make_options(timeline=True, render_options=["flat=true"]),
            output_file=DummyFile(),
        )


def test_report_dir_save_and_load_prev_prunes_old_files(monkeypatch: pytest.MonkeyPatch):
    tmp_path = workspace_temp_dir()
    monkeypatch.setattr("pyinstrument.__main__.appdirs.user_data_dir", lambda *args, **kwargs: str(tmp_path))

    reports_path = Path(report_dir())
    assert reports_path.exists()

    for i in range(12):
        (reports_path / f"2026-04-19T12-00-{i:02d}.pyisession").write_text("{}", encoding="utf-8")

    session = dummy_session(start_time=0)
    path, identifier = save_report_to_temp_storage(session)

    assert Path(path).exists()
    loaded = load_report_from_temp_storage(identifier)
    assert loaded.target_description == "dummy"
    assert len(list(reports_path.glob("*.pyisession"))) == 11


def test_load_report_from_temp_storage_exits_for_missing_identifier(
    monkeypatch: pytest.MonkeyPatch,
):
    tmp_path = workspace_temp_dir()
    monkeypatch.setattr("pyinstrument.__main__.report_dir", lambda: str(tmp_path))

    with pytest.raises(SystemExit, match="Couldn't find a profile"):
        load_report_from_temp_storage("missing-report")


def test_main_load_prev_path_exercises_session_loading(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    tmp_path = workspace_temp_dir()
    session_file = tmp_path / "saved.pyisession"
    session = dummy_session(start_time=1710000000)
    session_file.write_text(json.dumps(session.to_json()), encoding="utf-8")

    monkeypatch.setattr("pyinstrument.__main__.report_dir", lambda: str(tmp_path))
    monkeypatch.setattr("sys.argv", ["pyinstrument", "--load-prev", "saved"])

    main()

    captured = capsys.readouterr()
    assert "dummy" in captured.out


def test_main_rejects_conflicting_entry_modes(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("sys.argv", ["pyinstrument", "--load=a.pyisession", "script.py"])

    with pytest.raises(SystemExit) as excinfo:
        main()

    assert excinfo.value.code == 2


def test_profiler_start_stop_reset_and_error_paths(monkeypatch: pytest.MonkeyPatch):
    events: list[tuple[str, object]] = []

    class SamplerStub:
        def subscribe(self, callback, **kwargs):
            events.append(("subscribe", kwargs))

        def unsubscribe(self, callback):
            events.append(("unsubscribe", callback))

    times = iter([10.0, 12.0])
    monkeypatch.setattr("pyinstrument.profiler.get_stack_sampler", lambda: SamplerStub())
    monkeypatch.setattr("pyinstrument.profiler.time.time", lambda: next(times))
    monkeypatch.setattr("pyinstrument.profiler.process_time", lambda: 5.0)
    monkeypatch.setattr("pyinstrument.profiler.build_call_stack", lambda frame, event, arg: ["root", "leaf"])

    profiler = Profiler(interval=0.002, async_mode="strict", use_timing_thread=True)
    profiler.start(target_description="CLI target")
    profiler._sampler_saw_call_stack(["sync"], 0.2, None)
    session = profiler.stop()

    assert session.target_description == "CLI target"
    assert session.sample_count == 1
    assert session.frame_records == [(["sync"], 0.2)]
    assert profiler.last_session is session
    assert events[0][0] == "subscribe"
    assert events[1][0] == "unsubscribe"

    profiler.reset()
    assert profiler.last_session is None

    with pytest.raises(RuntimeError):
        profiler.stop()


def test_profiler_sampler_async_branches_and_render_guards():
    profiler = Profiler(async_mode="strict")
    profiler._active_session = ActiveProfilerSession(
        start_time=1.0,
        start_process_time=0.0,
        start_call_stack=["root"],
        target_description="async",
        interval=0.001,
    )

    profiler._sampler_saw_call_stack(["sync"], 0.1, SimpleNamespace(state="out_of_context_awaited", info=["awaiting"]))
    profiler._sampler_saw_call_stack(["sync"], 0.2, SimpleNamespace(state="out_of_context_unknown", info=["exit"]))
    profiler._sampler_saw_call_stack(["sync"], 0.3, SimpleNamespace(state="in_context", info=None))

    assert profiler._active_session.frame_records == [
        (["awaiting", AWAIT_FRAME_IDENTIFIER], 0.1),
        (["exit", OUT_OF_CONTEXT_FRAME_IDENTIFIER], 0.2),
        (["sync"], 0.3),
    ]

    running_profiler = Profiler()
    running_profiler._active_session = ActiveProfilerSession(
        start_time=1.0,
        start_process_time=0.0,
        start_call_stack=["root"],
        target_description="running",
        interval=0.001,
    )
    with pytest.raises(Exception, match="still running"):
        running_profiler._get_last_session_or_fail()

    with pytest.raises(Exception, match="has not completed"):
        Profiler()._get_last_session_or_fail()


def test_session_json_combine_resample_and_shorten_path(monkeypatch: pytest.MonkeyPatch):
    json_session = Session.from_json(
        {
            "frame_records": [(["frame"], 0.05)],
            "start_time": 1.0,
            "duration": 0.1,
            "sample_count": 1,
            "start_call_stack": ["root"],
            "target_description": "loaded",
            "cpu_time": None,
        }
    )
    assert json_session.min_interval == 0.001
    assert json_session.max_interval == 0.001
    assert json_session.cpu_time == 0

    combined = Session.combine(
        dummy_session(start_time=3.0, sys_path=["a", "b"]),
        dummy_session(start_time=1.0, sys_path=["b", "c"]),
    )
    assert combined.start_time == 1.0
    assert combined.duration == 0.2
    assert combined.sample_count == 2
    assert combined.sys_path == ["b", "c", "a"]

    session = dummy_session(sys_path=["C:\\repo", "D:\\lib"])
    path = "C:\\repo\\pkg\\module.py"
    assert session.shorten_path(path) == os.path.join("pkg", "module.py")

    monkeypatch.setattr(
        "pyinstrument.session.os.path.relpath",
        lambda target, start: (_ for _ in ()).throw(ValueError()) if start == "C:\\repo" else "fallback\\module.py",
    )
    other_session = dummy_session(sys_path=["C:\\repo", "D:\\lib"])
    assert other_session.shorten_path("E:\\pkg\\module.py") == "fallback\\module.py"

    resampled = Session(
        frame_records=[(["a"], 0.03), (["b"], 0.04), (["c"], 0.05)],
        start_time=0.0,
        duration=0.12,
        min_interval=0.01,
        max_interval=0.05,
        sample_count=3,
        start_call_stack=["root"],
        target_description="resample",
        cpu_time=0.0,
        sys_path=["."],
        sys_prefixes=["prefix"],
    ).resample(0.06)
    assert resampled.frame_records == [(["b"], pytest.approx(0.07)), (["c"], pytest.approx(0.06))]
    assert resampled.sample_count == 2


def test_util_and_vendor_helpers_cover_boundary_behaviour(monkeypatch: pytest.MonkeyPatch):
    assert object_with_import_path("pyinstrument.session.Session") is Session
    with pytest.raises(ValueError):
        object_with_import_path("Session")

    assert format_float_with_sig_figs(0) == "0"
    assert format_float_with_sig_figs(12.3456, sig_figs=2, trim_zeroes=True) == "12"
    assert strtobool("YES") is True
    assert strtobool("off") is False

    utf8_file = DummyFile(encoding="utf-8", isatty=True)
    latin1_file = DummyFile(encoding="latin-1", isatty=False)
    assert file_supports_unicode(utf8_file) is True
    assert file_supports_unicode(latin1_file) is False
    assert file_is_a_tty(utf8_file) is True

    monkeypatch.setattr("pyinstrument.util.sys.platform", "linux")
    assert file_supports_color(utf8_file) is True
    monkeypatch.setattr("pyinstrument.util.sys.platform", "win32")
    monkeypatch.delenv("ANSICON", raising=False)
    assert file_supports_color(utf8_file) is False

    nested = {"processor_options": {"threshold": 1, "items": [0, {"name": "old"}]}}
    keypath.set_value_at_keypath(nested, "processor_options.threshold", 3)
    keypath.set_value_at_keypath(nested, "processor_options.items.1.name", "new")
    assert keypath.value_at_keypath(nested, "processor_options.threshold") == 3
    assert keypath.value_at_keypath(nested, "processor_options.items.1.name") == "new"

    monkeypatch.setattr(appdirs, "system", "linux")
    monkeypatch.setenv("XDG_DATA_HOME", "/tmp/data-home")
    monkeypatch.setenv("XDG_CONFIG_HOME", "/tmp/config-home")
    assert appdirs.user_data_dir("pyinstrument").replace("\\", "/") == "/tmp/data-home/pyinstrument"
    assert appdirs.user_config_dir("pyinstrument").replace("\\", "/") == "/tmp/config-home/pyinstrument"

    monkeypatch.setattr(appdirs, "system", "win32")
    monkeypatch.setattr(appdirs, "_get_win_folder", lambda _: r"C:\Users\tester\AppData\Local")
    assert appdirs.user_cache_dir("pyinstrument", "PyInstrument").lower().endswith(
        r"pyinstrument\pyinstrument\cache"
    )
