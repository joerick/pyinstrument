import textwrap
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from pyinstrument.__main__ import main
from pyinstrument.renderers.console import ConsoleRenderer

from .util import BUSY_WAIT_SCRIPT


def test_renderer_option(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    (tmp_path / "test_program.py").write_text(BUSY_WAIT_SCRIPT)
    monkeypatch.setattr("sys.argv", ["pyinstrument", "-p", "show_percentages", "test_program.py"])
    monkeypatch.chdir(tmp_path)

    with patch(
        "pyinstrument.renderers.console.ConsoleRenderer", autospec=True
    ) as mock_renderer_class:
        main()

    mock_renderer_class.assert_called_once_with(show_percentages=True)
