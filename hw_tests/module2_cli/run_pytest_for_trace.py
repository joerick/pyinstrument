from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.getcwd())

raise SystemExit(pytest.main(["hw_tests/module2_cli/test_cli_module_white_box.py", "-q"]))
