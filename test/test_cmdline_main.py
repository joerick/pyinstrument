import textwrap
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from pyinstrument.__main__ import main
from pyinstrument.renderers.console import ConsoleRenderer

from .util import BUSY_WAIT_SCRIPT


def test_renderer_option(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    (tmp_path / "test_program.py").write_text(BUSY_WAIT_SCRIPT)
    monkeypatch.setattr(
        "sys.argv", ["pyinstrument", "-p", "time=percent_of_total", "test_program.py"]
    )
    monkeypatch.chdir(tmp_path)

    with patch(
        "pyinstrument.__main__.renderers.ConsoleRenderer",
        wraps=ConsoleRenderer,
    ) as mock_renderer_class:
        main()

    mock_renderer_class.assert_called_once()
    assert mock_renderer_class.call_args.kwargs["time"] == "percent_of_total"


def test_processor_renderer_option(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    (tmp_path / "test_program.py").write_text(BUSY_WAIT_SCRIPT)
    monkeypatch.setattr(
        "sys.argv",
        ["pyinstrument", "-p", 'processor_options={"some_option": 44}', "test_program.py"],
    )
    monkeypatch.chdir(tmp_path)

    with patch(
        "pyinstrument.__main__.renderers.ConsoleRenderer",
        wraps=ConsoleRenderer,
    ) as mock_renderer_class:
        main()

    mock_renderer_class.assert_called_once()
    assert mock_renderer_class.call_args.kwargs["processor_options"]["some_option"] == 44
