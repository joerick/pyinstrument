import os
import subprocess
import sys
from pathlib import Path

import pytest

# this script just does a busywait for 0.25 seconds.
BUSY_WAIT_SCRIPT = """
import time, sys

def do_nothing():
    pass

def busy_wait(duration):
    end_time = time.time() + duration

    while time.time() < end_time:
        do_nothing()

def main():
    print('sys.argv: ', sys.argv)
    busy_wait(0.25)


if __name__ == '__main__':
    main()
"""

EXECUTION_DETAILS_SCRIPT = f"""
#!{sys.executable}
import sys, os
print('__name__', __name__, file=sys.stderr)
print('sys.argv', sys.argv, file=sys.stderr)
print('sys.path', sys.path, file=sys.stderr)
print('sys.executable', os.path.realpath(sys.executable), file=sys.stderr)
print('os.getcwd()', os.getcwd(), file=sys.stderr)
""".strip()


@pytest.mark.parametrize(
    "pyinstrument_invocation",
    (["pyinstrument"], [sys.executable, "-m", "pyinstrument"]),
)
class TestCommandLine:
    def test_command_line(self, pyinstrument_invocation, tmp_path: Path):
        busy_wait_py = tmp_path / "busy_wait.py"
        busy_wait_py.write_text(BUSY_WAIT_SCRIPT)

        # need to wrap Paths with str() due to CPython bug 33617 (fixed in Python 3.8)
        output = subprocess.check_output([*pyinstrument_invocation, str(busy_wait_py)])

        assert "busy_wait" in str(output)
        assert "do_nothing" in str(output)

    def test_module_running(self, pyinstrument_invocation, tmp_path: Path):
        (tmp_path / "busy_wait_module").mkdir()
        (tmp_path / "busy_wait_module" / "__init__.py").touch()
        (tmp_path / "busy_wait_module" / "__main__.py").write_text(BUSY_WAIT_SCRIPT)

        output = subprocess.check_output(
            [*pyinstrument_invocation, "-m", "busy_wait_module"], cwd=tmp_path
        )

        assert "busy_wait" in str(output)
        assert "do_nothing" in str(output)

    def test_single_file_module_running(self, pyinstrument_invocation, tmp_path: Path):
        busy_wait_py = tmp_path / "busy_wait.py"
        busy_wait_py.write_text(BUSY_WAIT_SCRIPT)

        output = subprocess.check_output(
            [*pyinstrument_invocation, "-m", "busy_wait"], cwd=tmp_path
        )

        assert "busy_wait" in str(output)
        assert "do_nothing" in str(output)

    def test_running_yourself_as_module(self, pyinstrument_invocation):
        subprocess.check_call(
            [*pyinstrument_invocation, "-m", "pyinstrument"],
        )

    def test_path(self, pyinstrument_invocation, tmp_path: Path, monkeypatch):
        if sys.platform == "win32":
            pytest.skip("--from-path is not supported on Windows")

        program_path = tmp_path / "pyi_test_program"

        program_path.write_text(BUSY_WAIT_SCRIPT)
        program_path.chmod(0x755)
        monkeypatch.setenv("PATH", str(tmp_path), prepend=os.pathsep)

        subprocess.check_call(
            [*pyinstrument_invocation, "--from-path", "--", "pyi_test_program"],
        )

    def test_script_execution_details(self, pyinstrument_invocation, tmp_path: Path):
        program_path = tmp_path / "program.py"
        program_path.write_text(EXECUTION_DETAILS_SCRIPT)

        process_pyi = subprocess.run(
            [*pyinstrument_invocation, str(program_path), "arg1", "arg2"],
            stderr=subprocess.PIPE,
            check=True,
            universal_newlines=True,
        )
        process_native = subprocess.run(
            [sys.executable, str(program_path), "arg1", "arg2"],
            stderr=subprocess.PIPE,
            check=True,
            universal_newlines=True,
        )

        print("process_pyi.stderr", process_pyi.stderr)
        print("process_native.stderr", process_native.stderr)
        assert process_pyi.stderr == process_native.stderr

    def test_module_execution_details(self, pyinstrument_invocation, tmp_path: Path):
        (tmp_path / "test_module").mkdir()
        (tmp_path / "test_module" / "__init__.py").touch()
        (tmp_path / "test_module" / "__main__.py").write_text(EXECUTION_DETAILS_SCRIPT)

        process_pyi = subprocess.run(
            [*pyinstrument_invocation, "-m", "test_module", "arg1", "arg2"],
            # stderr=subprocess.PIPE,
            check=True,
            cwd=tmp_path,
            universal_newlines=True,
        )
        process_native = subprocess.run(
            [sys.executable, "-m", "test_module", "arg1", "arg2"],
            # stderr=subprocess.PIPE,
            check=True,
            cwd=tmp_path,
            universal_newlines=True,
        )

        print("process_pyi.stderr", process_pyi.stderr)
        print("process_native.stderr", process_native.stderr)
        assert process_pyi.stderr == process_native.stderr

    def test_path_execution_details(self, pyinstrument_invocation, tmp_path: Path, monkeypatch):
        if sys.platform == "win32":
            pytest.skip("--from-path is not supported on Windows")

        program_path = tmp_path / "pyi_test_program"
        program_path.write_text(EXECUTION_DETAILS_SCRIPT)
        program_path.chmod(0x755)
        monkeypatch.setenv("PATH", str(tmp_path), prepend=os.pathsep)

        process_pyi = subprocess.run(
            [
                *pyinstrument_invocation,
                "--from-path",
                "--",
                "pyi_test_program",
                "arg1",
                "arg2",
            ],
            stderr=subprocess.PIPE,
            check=True,
            universal_newlines=True,
        )
        process_native = subprocess.run(
            ["pyi_test_program", "arg1", "arg2"],
            stderr=subprocess.PIPE,
            check=True,
            universal_newlines=True,
        )

        print("process_pyi.stderr", process_pyi.stderr)
        print("process_native.stderr", process_native.stderr)
        assert process_pyi.stderr == process_native.stderr
