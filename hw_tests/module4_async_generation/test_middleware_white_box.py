from __future__ import annotations

import importlib
import io
import os
import sys
import types
from types import SimpleNamespace

import pytest

from pyinstrument.renderers import Renderer


class DummyRequest:
    def __init__(self, query=None, full_path="/hello/world?x=1"):
        self.GET = query or {}
        self._full_path = full_path

    def get_full_path(self):
        return self._full_path


class DummyResponse:
    pass


class DummySession:
    duration = 1.234


class DummyProfiler:
    def __init__(self, interval):
        self.interval = interval
        self.started = False
        self.stopped = False

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True
        return DummySession()


class DummyHTMLRenderer(Renderer):
    output_file_extension = "html"

    def render(self, session):
        return f"html:{session.duration}"


class DummyTextRenderer(Renderer):
    output_file_extension = "txt"

    def __init__(self):
        self.render_calls = []

    def render(self, session):
        self.render_calls.append(session)
        return f"text:{session.duration}:{len(self.render_calls)}"


def import_middleware_module(monkeypatch: pytest.MonkeyPatch, include_deprecation=True):
    settings = SimpleNamespace()

    django_module = types.ModuleType("django")
    conf_module = types.ModuleType("django.conf")
    conf_module.settings = settings
    http_module = types.ModuleType("django.http")

    class HttpResponse:
        def __init__(self, content):
            self.content = content

    http_module.HttpResponse = HttpResponse

    utils_loading_module = types.ModuleType("django.utils.module_loading")
    deprecation_module = types.ModuleType("django.utils.deprecation")

    imports = {}

    def import_string(path):
        if path == "broken.path":
            raise ImportError("broken import")
        return imports[path]

    utils_loading_module.import_string = import_string
    deprecation_module.MiddlewareMixin = object

    monkeypatch.setitem(sys.modules, "django", django_module)
    monkeypatch.setitem(sys.modules, "django.conf", conf_module)
    monkeypatch.setitem(sys.modules, "django.http", http_module)
    monkeypatch.setitem(sys.modules, "django.utils", types.ModuleType("django.utils"))
    monkeypatch.setitem(sys.modules, "django.utils.module_loading", utils_loading_module)
    if include_deprecation:
        monkeypatch.setitem(sys.modules, "django.utils.deprecation", deprecation_module)
    else:
        monkeypatch.delitem(sys.modules, "django.utils.deprecation", raising=False)

    if "pyinstrument.middleware" in sys.modules:
        del sys.modules["pyinstrument.middleware"]
    middleware = importlib.import_module("pyinstrument.middleware")
    return middleware, settings, imports


def test_middleware_import_without_middleware_mixin(monkeypatch: pytest.MonkeyPatch):
    middleware, _, _ = import_middleware_module(monkeypatch, include_deprecation=False)
    assert middleware.MiddlewareMixin is object


def test_get_renderer_paths(monkeypatch: pytest.MonkeyPatch, capsys):
    middleware, _, imports = import_middleware_module(monkeypatch)

    class GoodRenderer(DummyTextRenderer):
        pass

    class NotARenderer:
        pass

    imports["good.Renderer"] = GoodRenderer
    imports["bad.Renderer"] = NotARenderer
    monkeypatch.setattr(middleware, "HTMLRenderer", DummyHTMLRenderer)

    assert isinstance(middleware.get_renderer(None), DummyHTMLRenderer)
    assert isinstance(middleware.get_renderer("good.Renderer"), GoodRenderer)

    with pytest.raises(ValueError, match="should subclass"):
        middleware.get_renderer("bad.Renderer")

    with pytest.raises(ImportError):
        middleware.get_renderer("broken.path")

    assert "Unable to import the class: broken.path" in capsys.readouterr().out


def test_process_request_process_response_and_filename_callback(monkeypatch: pytest.MonkeyPatch, tmp_path):
    middleware, settings, imports = import_middleware_module(monkeypatch)
    imports["renderers.TextRenderer"] = DummyTextRenderer
    monkeypatch.setattr(middleware, "Profiler", DummyProfiler)
    monkeypatch.setattr(middleware, "HTMLRenderer", DummyHTMLRenderer)

    settings.PYINSTRUMENT_SHOW_CALLBACK = lambda request: True
    settings.PYINSTRUMENT_URL_ARGUMENT = "profile"
    settings.PYINSTRUMENT_PROFILE_DIR = str(tmp_path)
    settings.PYINSTRUMENT_PROFILE_DIR_RENDERER = "renderers.TextRenderer"
    settings.PYINSTRUMENT_INTERVAL = 0.123
    settings.PYINSTRUMENT_FILENAME_CALLBACK = lambda request, session, renderer: "saved.txt"

    request = DummyRequest(query={"profile": "1"})
    response = DummyResponse()
    mw = middleware.ProfilerMiddleware()

    mw.process_request(request)
    assert isinstance(request.profiler, DummyProfiler)
    assert request.profiler.started is True
    assert request.profiler.interval == 0.123

    result = mw.process_response(request, response)

    assert isinstance(result, middleware.HttpResponse)
    assert result.content == "html:1.234"
    assert (tmp_path / "saved.txt").read_text(encoding="utf-8") == "text:1.234:1"


def test_process_response_without_profile_arg_uses_original_response(monkeypatch: pytest.MonkeyPatch, tmp_path):
    middleware, settings, imports = import_middleware_module(monkeypatch)
    imports["show.callback"] = lambda request: False
    monkeypatch.setattr(middleware, "Profiler", DummyProfiler)
    monkeypatch.setattr(middleware, "HTMLRenderer", DummyHTMLRenderer)

    settings.PYINSTRUMENT_SHOW_CALLBACK = "show.callback"
    settings.PYINSTRUMENT_PROFILE_DIR = str(tmp_path)
    settings.PYINSTRUMENT_FILENAME = "{path}.{ext}"

    request = DummyRequest(query={}, full_path="/hello/world?x=1")
    response = DummyResponse()
    mw = middleware.ProfilerMiddleware()
    mw.process_request(request)

    assert hasattr(request, "profiler")
    returned = mw.process_response(request, response)

    assert returned is response
    saved_file = tmp_path / "_hello_world?x=1.html"
    assert saved_file.read_text(encoding="utf-8") == "html:1.234"


def test_process_response_validates_filename_callback_and_windows_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path
):
    middleware, settings, _ = import_middleware_module(monkeypatch)
    monkeypatch.setattr(middleware, "Profiler", DummyProfiler)
    monkeypatch.setattr(middleware, "HTMLRenderer", DummyHTMLRenderer)
    monkeypatch.setattr(middleware.sys, "platform", "win32")

    settings.PYINSTRUMENT_PROFILE_DIR = str(tmp_path)
    settings.PYINSTRUMENT_FILENAME_CALLBACK = lambda request, session, renderer: 123

    request = DummyRequest(query={}, full_path="/route?x=1")
    request.profiler = DummyProfiler(interval=0.1)
    response = DummyResponse()
    mw = middleware.ProfilerMiddleware()

    with pytest.raises(ValueError, match="should be a string"):
        mw.process_response(request, response)

    settings.PYINSTRUMENT_FILENAME_CALLBACK = None
    settings.PYINSTRUMENT_FILENAME = "{path}.{ext}"
    request.profiler = DummyProfiler(interval=0.1)
    returned = mw.process_response(request, response)

    assert returned is response
    assert (tmp_path / "_route_qs_x=1.html").exists()


def test_process_response_without_profiler_returns_original_response(monkeypatch: pytest.MonkeyPatch):
    middleware, _, _ = import_middleware_module(monkeypatch)
    response = DummyResponse()
    assert middleware.ProfilerMiddleware().process_response(DummyRequest(), response) is response


def test_default_show_callback_profile_arg_html_renderer_and_mkdir(
    monkeypatch: pytest.MonkeyPatch, tmp_path
):
    middleware, settings, _ = import_middleware_module(monkeypatch)
    monkeypatch.setattr(middleware, "Profiler", DummyProfiler)
    monkeypatch.setattr(middleware, "HTMLRenderer", DummyHTMLRenderer)

    profile_dir = tmp_path / "profiles"
    settings.PYINSTRUMENT_PROFILE_DIR = str(profile_dir)
    settings.PYINSTRUMENT_URL_ARGUMENT = "profile"
    settings.PYINSTRUMENT_FILENAME = "saved.{ext}"

    request = DummyRequest(query={"profile": "1"})
    response = DummyResponse()
    mw = middleware.ProfilerMiddleware()
    mw.process_request(request)
    returned = mw.process_response(request, response)

    assert profile_dir.is_dir()
    assert (profile_dir / "saved.html").read_text(encoding="utf-8") == "html:1.234"
    assert isinstance(returned, middleware.HttpResponse)
    assert returned.content == "html:1.234"
