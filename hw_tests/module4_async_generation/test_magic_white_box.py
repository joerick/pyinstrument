from __future__ import annotations

import ast
import asyncio
from types import SimpleNamespace

import pytest

import pyinstrument.magic as magic_pkg
from pyinstrument.frame import Frame
from pyinstrument.magic._utils import PrePostAstTransformer
from pyinstrument.magic.magic import (
    InterruptSilently,
    PyinstrumentMagic,
    _get_active_profiler,
    strip_ipython_frames_processor,
)


class DummyShell:
    ast_transformers = []


def test_magic_package_exports_pyinstrument_magic():
    assert magic_pkg.PyinstrumentMagic is PyinstrumentMagic


def test_pre_post_ast_transformer_wraps_last_expression_and_active_flag():
    transformer = PrePostAstTransformer("before = 1", "after = 2")
    module = ast.parse("value = 3\nvalue")

    transformed = transformer.visit_Module(module)
    namespace = {}
    exec(compile(transformed, "<ast>", "exec"), namespace, namespace)

    assert namespace["before"] == 1
    assert namespace["after"] == 2
    assert namespace["value"] == 3
    assert namespace["ast-tmp"] == 3

    transformer.active = False
    untouched = ast.parse("x = 1")
    assert transformer.visit_Module(untouched) is untouched


def test_recreate_transformer_supports_old_and_new_ipython(monkeypatch: pytest.MonkeyPatch):
    shell = DummyShell()
    magic = PyinstrumentMagic(shell)

    monkeypatch.setattr("pyinstrument.magic.magic.IPython.version_info", (8, 14, 0))
    magic.recreate_transformer("legacy")
    assert isinstance(magic._transformer, PrePostAstTransformer)

    class FakeReplaceCodeTransformer:
        @classmethod
        def from_string(cls, source):
            return ("transformer", source)

    import pyinstrument.magic.magic as magic_module

    monkeypatch.setattr(magic_module.IPython, "version_info", (9, 0, 0))
    monkeypatch.setattr(
        "IPython.core.magics.ast_mod.ReplaceCodeTransformer",
        FakeReplaceCodeTransformer,
        raising=False,
    )
    magic.recreate_transformer("modern")

    assert magic._transformer[0] == "transformer"
    assert "modern" in magic._transformer[1]


def test_strip_ipython_frames_processor_prunes_internal_nodes():
    root = Frame("root\x00/work/app.py\x001")
    internal = Frame("internal\x00/usr/lib/IPython/core/interactiveshell.py\x002")
    user = Frame("user\x00/work/user.py\x003")
    internal_child = Frame("leaf\x00/work/leaf.py\x004", time=1.5)

    internal.add_child(internal_child)
    root.add_child(internal)
    root.add_child(user)

    stripped = strip_ipython_frames_processor(root, options={})

    assert stripped is root
    assert [child.function for child in root.children] == ["leaf", "user"]
    assert strip_ipython_frames_processor(None, options={}) is None


def test_get_active_profiler_and_run_cell_async_restores_event_loop():
    old_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(old_loop)

    magic = PyinstrumentMagic(DummyShell())
    profiler = object()

    import pyinstrument.magic.magic as magic_module

    magic_module._active_profiler = profiler
    assert _get_active_profiler() is profiler

    class FakeIPython:
        async def run_cell_async(self, code):
            await asyncio.sleep(0)
            return {"code": code, "status": "ok"}

    try:
        result = magic.run_cell_async(FakeIPython(), "print('hi')")
        assert result == {"code": "print('hi')", "status": "ok"}
        assert asyncio.get_event_loop() is old_loop
    finally:
        magic_module._active_profiler = None
        old_loop.close()


def test_pyinstrument_early_return_warning_and_keyboard_interrupt_paths(
    monkeypatch: pytest.MonkeyPatch,
):
    import pyinstrument.magic.magic as magic_module

    display_calls = []

    class FakeProfiler:
        def __init__(self, *_, **__):
            self.is_running = False

        def stop(self):
            self.is_running = False

    class FakeIP:
        def __init__(self, result):
            self.execution_count = 7
            self.ast_transformers = []
            self.user_ns = {"bad-key": 1}
            self.CustomTB = object()
            self.custom_exceptions = ()
            self._result = result
            self.custom_exc_args = None

        def run_cell(self, code):
            self.ran_code = code
            return self._result

        def set_custom_exc(self, types, handler):
            self.custom_exc_args = (types, handler)

    warning_ip = FakeIP(
        SimpleNamespace(error_in_exec=RuntimeError("This event loop is already running"))
    )
    monkeypatch.setattr(magic_module, "parse_argstring", lambda *args: SimpleNamespace(
        interval=0.001,
        async_mode="disabled",
        show_all=False,
        timeline=False,
        height=400,
    ))
    monkeypatch.setattr(magic_module, "get_ipython", lambda: warning_ip)
    monkeypatch.setattr(magic_module, "Profiler", FakeProfiler)
    monkeypatch.setattr(magic_module, "display", lambda payload, raw=False: display_calls.append((payload, raw)))

    magic = PyinstrumentMagic(DummyShell())
    assert magic.pyinstrument("", cell="print('hello')") is None
    assert "text/html" in display_calls[0][0]
    assert "text/plain" in display_calls[0][0]
    assert "bad-key" not in warning_ip.user_ns

    interrupt_ip = FakeIP(SimpleNamespace(error_in_exec=KeyboardInterrupt()))
    monkeypatch.setattr(magic_module, "get_ipython", lambda: interrupt_ip)

    with pytest.raises(InterruptSilently):
        magic.pyinstrument("", cell="print('boom')")

    assert interrupt_ip.custom_exc_args is not None
    assert interrupt_ip.custom_exc_args[0] == (InterruptSilently,)
    _, handler = interrupt_ip.custom_exc_args
    handler(None, None, None, None)
    assert interrupt_ip.CustomTB is not None


def test_pyinstrument_no_shell_empty_code_line_and_running_profiler_paths(
    monkeypatch: pytest.MonkeyPatch,
):
    import pyinstrument.magic.magic as magic_module

    parsed_args = SimpleNamespace(
        interval=0.001,
        async_mode="disabled",
        show_all=False,
        timeline=False,
        height=400,
    )
    monkeypatch.setattr(magic_module, "parse_argstring", lambda *args: parsed_args)
    monkeypatch.setattr(magic_module, "get_ipython", lambda: None)

    magic = PyinstrumentMagic(DummyShell())
    with pytest.raises(RuntimeError, match="couldn't get ipython"):
        magic.pyinstrument("print('x')")

    class FakeActiveProfiler:
        is_running = True

        def __init__(self):
            self.stopped = False

        def stop(self):
            self.stopped = True
            self.is_running = False

    class FakeProfiler:
        def __init__(self, *_, **__):
            self.is_running = False

        def output(self, renderer):
            return ""

    class FakeIP:
        execution_count = 3

        def __init__(self):
            self.ast_transformers = ["old-transformer"]
            self.user_ns = {}

        def run_cell(self, code):
            return SimpleNamespace(error_in_exec=RuntimeError("This event loop is already running"))

    active_profiler = FakeActiveProfiler()
    fake_ip = FakeIP()
    magic._transformer = "old-transformer"
    magic_module._active_profiler = active_profiler
    monkeypatch.setattr(magic_module, "get_ipython", lambda: fake_ip)
    monkeypatch.setattr(magic_module, "Profiler", FakeProfiler)

    assert magic.pyinstrument("", cell="") is None
    assert magic.pyinstrument("print('line magic')") is None
    assert active_profiler.stopped is True
    assert "old-transformer" not in fake_ip.ast_transformers


def test_pyinstrument_async_mode_uses_threaded_runner(monkeypatch: pytest.MonkeyPatch):
    import pyinstrument.magic.magic as magic_module

    display_calls = []

    class FakeRenderer:
        def __init__(self, **kwargs):
            self.processors = []
            self.preprocessors = []

    class FakeProfiler:
        def __init__(self, *_, **__):
            self.is_running = False

        def output(self, renderer):
            return "async output"

    class FakeIFrame:
        def __init__(self, **kwargs):
            pass

        def _repr_html_(self):
            return "<iframe>async</iframe>"

    class FakeIP:
        execution_count = 4

        def __init__(self):
            self.ast_transformers = []
            self.user_ns = {}

    ip = FakeIP()
    magic = PyinstrumentMagic(DummyShell())
    monkeypatch.setattr(magic_module, "parse_argstring", lambda *args: SimpleNamespace(
        interval=0.001,
        async_mode="enabled",
        show_all=False,
        timeline=False,
        height=400,
    ))
    monkeypatch.setattr(magic_module, "get_ipython", lambda: ip)
    monkeypatch.setattr(magic_module, "Profiler", FakeProfiler)
    monkeypatch.setattr(magic_module, "compute_render_options", lambda *args, **kwargs: {})
    monkeypatch.setattr(magic_module.renderers, "HTMLRenderer", FakeRenderer)
    monkeypatch.setattr(magic_module.renderers, "ConsoleRenderer", FakeRenderer)
    monkeypatch.setattr(magic_module, "IFrame", FakeIFrame)
    monkeypatch.setattr(magic_module, "display", lambda payload, raw=False: display_calls.append((payload, raw)))
    monkeypatch.setattr(
        magic,
        "run_cell_async",
        lambda ip_arg, code: SimpleNamespace(error_in_exec=None, ip=ip_arg, code=code),
    )

    magic.pyinstrument("", cell="await something()")

    assert display_calls == [({"text/html": "<iframe>async</iframe>", "text/plain": "async output"}, True)]


def test_pyinstrument_success_path_displays_output_and_cleans_up(monkeypatch: pytest.MonkeyPatch):
    import pyinstrument.magic.magic as magic_module

    display_calls = []

    class FakeRenderer:
        def __init__(self, kind, **kwargs):
            self.kind = kind
            self.kwargs = kwargs
            self.processors = []
            self.preprocessors = []

    class FakeProfiler:
        def __init__(self, *_, **__):
            self.is_running = False
            self.started = []

        def stop(self):
            self.is_running = False

        def output(self, renderer):
            if renderer.kind == "html":
                return "<html>function_a</html>"
            return "function_a text"

    class FakeIFrame:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def _repr_html_(self):
            return "<iframe>ok</iframe>"

    class FakeIP:
        def __init__(self):
            self.execution_count = 9
            self.ast_transformers = []
            self.user_ns = {"bad-key": 1}
            self.CustomTB = object()
            self.custom_exceptions = ()

        def run_cell(self, code):
            self.ran_code = code
            return SimpleNamespace(error_in_exec=None)

    ip = FakeIP()
    monkeypatch.setattr(magic_module, "parse_argstring", lambda *args: SimpleNamespace(
        interval=0.002,
        async_mode="disabled",
        show_all=True,
        timeline=True,
        height=321,
    ))
    monkeypatch.setattr(magic_module, "get_ipython", lambda: ip)
    monkeypatch.setattr(magic_module, "Profiler", FakeProfiler)
    monkeypatch.setattr(magic_module, "compute_render_options", lambda *args, **kwargs: {"unicode": True})
    monkeypatch.setattr(
        magic_module.renderers, "HTMLRenderer", lambda **kwargs: FakeRenderer("html", **kwargs)
    )
    monkeypatch.setattr(
        magic_module.renderers, "ConsoleRenderer", lambda **kwargs: FakeRenderer("text", **kwargs)
    )
    monkeypatch.setattr(magic_module, "IFrame", FakeIFrame)
    monkeypatch.setattr(magic_module, "display", lambda payload, raw=False: display_calls.append((payload, raw)))

    magic = PyinstrumentMagic(DummyShell())
    magic.pyinstrument("", cell="print('ok')")

    assert ip.ast_transformers == []
    assert "bad-key" not in ip.user_ns
    assert display_calls == [({"text/html": "<iframe>ok</iframe>", "text/plain": "function_a text"}, True)]
    assert magic_module._active_profiler is None
