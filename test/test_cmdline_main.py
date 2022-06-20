from pathlib import Path

import pytest

from pyinstrument.__main__ import main
from pyinstrument.renderers.base import FrameRenderer

from .util import BUSY_WAIT_SCRIPT

fake_renderer_instance = None


class FakeRenderer(FrameRenderer):
    def __init__(self, time=None, **kwargs):
        self.time = time
        super().__init__(**kwargs)
        global fake_renderer_instance
        fake_renderer_instance = self
        print("instance")

    def default_processors(self):
        """
        Return a list of processors that this renderer uses by default.
        """
        return []

    def render(self, session) -> str:
        return ""


def test_renderer_option(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    (tmp_path / "test_program.py").write_text(BUSY_WAIT_SCRIPT)
    monkeypatch.setattr(
        "sys.argv",
        [
            "pyinstrument",
            "-r",
            "test.test_cmdline_main.FakeRenderer",
            "-p",
            "time=percent_of_total",
            "test_program.py",
        ],
    )
    monkeypatch.chdir(tmp_path)

    global fake_renderer_instance
    fake_renderer_instance = None

    main()

    assert fake_renderer_instance is not None
    assert fake_renderer_instance.time == "percent_of_total"


def test_json_renderer_option(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    (tmp_path / "test_program.py").write_text(BUSY_WAIT_SCRIPT)
    monkeypatch.setattr(
        "sys.argv",
        [
            "pyinstrument",
            "-r",
            "test.test_cmdline_main.FakeRenderer",
            "-p",
            'processor_options={"some_option": 44}',
            "test_program.py",
        ],
    )
    monkeypatch.chdir(tmp_path)

    global fake_renderer_instance
    fake_renderer_instance = None

    main()

    assert fake_renderer_instance is not None
    assert fake_renderer_instance.processor_options["some_option"] == 44


def test_dotted_renderer_option(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    (tmp_path / "test_program.py").write_text(BUSY_WAIT_SCRIPT)
    monkeypatch.setattr(
        "sys.argv",
        [
            "pyinstrument",
            "-r",
            "test.test_cmdline_main.FakeRenderer",
            "-p",
            "processor_options.other_option=13",
            "test_program.py",
        ],
    )
    monkeypatch.chdir(tmp_path)

    global fake_renderer_instance
    fake_renderer_instance = None

    main()

    assert fake_renderer_instance is not None
    assert fake_renderer_instance.processor_options["other_option"] == 13
