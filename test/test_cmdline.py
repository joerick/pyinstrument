import json
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from .util import BUSY_WAIT_SCRIPT, flaky_in_ci

EXECUTION_DETAILS_SCRIPT = f"""
#!{sys.executable}
import sys, os
print('__name__', __name__, file=sys.stderr)
print('main globals', vars(sys.modules['__main__']) is globals(), file=sys.stderr)
print('sys.argv', sys.argv, file=sys.stderr)
print('sys.executable', os.path.realpath(sys.executable), file=sys.stderr)
print('os.getcwd()', os.getcwd(), file=sys.stderr)
""".strip()


@pytest.mark.parametrize(
    "pyinstrument_invocation",
    (["pyinstrument"], [sys.executable, "-m", "pyinstrument"]),
)
class TestCommandLine:
    @pytest.fixture(autouse=True)
    def _suppress_warnings(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("PYINSTRUMENT_IGNORE_OVERHEAD_WARNING", "1")

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
            [*pyinstrument_invocation, "-m", "pyinstrument", "--help"],
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

    @flaky_in_ci
    def test_program_passed_as_string(self, pyinstrument_invocation, tmp_path: Path):
        # check the program actually runs
        output_file = tmp_path / "output.txt"
        output = subprocess.check_output(
            [
                *pyinstrument_invocation,
                "-c",
                textwrap.dedent(
                    f"""
                    import sys
                    from pathlib import Path
                    output_file = Path(sys.argv[1])
                    output_file.write_text("Hello World")
                    print("Finished.")
                    """
                ),
                str(output_file),
            ],
        )

        assert "Finished." in str(output)
        assert output_file.read_text() == "Hello World"

        # check the output
        output = subprocess.check_output([*pyinstrument_invocation, "-c", BUSY_WAIT_SCRIPT])

        print(output.decode("utf-8"))

        assert "busy_wait" in str(output)
        assert "do_nothing" in str(output)

    def test_program_passed_as_string_pickle(self, pyinstrument_invocation):
        program = textwrap.dedent("""
            import pickle

            class Example:
                def __init__(self, value):
                    self.value = value

            restored = pickle.loads(pickle.dumps(Example(42)))
            assert type(restored) is Example
            assert restored.value == 42
            print("pickle round trip succeeded")
        """)
        output = subprocess.check_output([*pyinstrument_invocation, "-c", program], text=True)

        assert "pickle round trip succeeded" in output

    def test_script_execution_details(self, pyinstrument_invocation, tmp_path: Path):
        program_path = tmp_path / "program.py"
        program_path.write_text(EXECUTION_DETAILS_SCRIPT)

        process_pyi = subprocess.run(
            [*pyinstrument_invocation, str(program_path), "arg1", "arg2"],
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
        process_native = subprocess.run(
            [sys.executable, str(program_path), "arg1", "arg2"],
            stderr=subprocess.PIPE,
            check=True,
            text=True,
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
            stderr=subprocess.PIPE,
            check=True,
            cwd=tmp_path,
            text=True,
        )
        process_native = subprocess.run(
            [sys.executable, "-m", "test_module", "arg1", "arg2"],
            stderr=subprocess.PIPE,
            check=True,
            cwd=tmp_path,
            text=True,
        )

        print("process_pyi.stderr", process_pyi.stderr)
        print("process_native.stderr", process_native.stderr)
        assert process_native.stderr
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
            text=True,
        )
        process_native = subprocess.run(
            ["pyi_test_program", "arg1", "arg2"],
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )

        print("process_pyi.stderr", process_pyi.stderr)
        print("process_native.stderr", process_native.stderr)
        assert process_pyi.stderr == process_native.stderr

    def test_program_passed_as_string_execution_details(
        self, pyinstrument_invocation, tmp_path: Path
    ):
        process_pyi = subprocess.run(
            [*pyinstrument_invocation, "-c", EXECUTION_DETAILS_SCRIPT],
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
        process_native = subprocess.run(
            [sys.executable, "-c", EXECUTION_DETAILS_SCRIPT],
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )

        print("process_pyi.stderr", process_pyi.stderr)
        print("process_native.stderr", process_native.stderr)
        assert process_native.stderr
        assert process_pyi.stderr == process_native.stderr

    def test_session_save_and_load(self, pyinstrument_invocation, tmp_path: Path):
        busy_wait_py = tmp_path / "busy_wait.py"
        busy_wait_py.write_text(BUSY_WAIT_SCRIPT)

        session_file = tmp_path / "session.pyisession"

        subprocess.check_call(
            [
                *pyinstrument_invocation,
                "--renderer=session",
                f"--outfile={session_file}",
                str(busy_wait_py),
            ]
        )

        # check it's a valid Session file
        from pyinstrument.session import Session

        Session.load(session_file)

        # run pyinstrument again to render the output
        output = subprocess.check_output([*pyinstrument_invocation, f"--load={session_file}"])
        assert "busy_wait" in str(output)
        assert "do_nothing" in str(output)

    def test_interval(self, pyinstrument_invocation, tmp_path: Path):
        busy_wait_py = tmp_path / "busy_wait.py"
        busy_wait_py.write_text(BUSY_WAIT_SCRIPT)

        output = subprocess.check_output(
            [
                *pyinstrument_invocation,
                "--interval",
                "0.002",
                str(busy_wait_py),
            ]
        )

        assert "busy_wait" in str(output)
        assert "do_nothing" in str(output)

    def test_invocation_machinery_is_trimmed(self, pyinstrument_invocation, tmp_path: Path):
        busy_wait_py = tmp_path / "busy_wait.py"
        busy_wait_py.write_text(BUSY_WAIT_SCRIPT)

        output = subprocess.check_output(
            [
                *pyinstrument_invocation,
                "--show-all",
                str(busy_wait_py),
            ],
            universal_newlines=True,
        )

        print("Output:")
        print(output)

        first_profiling_line = re.search(r"^\d+(\.\d+)?\s+([^\s]+)\s+(.*)", output, re.MULTILINE)
        assert first_profiling_line

        function_name = first_profiling_line.group(2)
        location = first_profiling_line.group(3)

        assert function_name == "<module>"
        assert "busy_wait.py" in location

    def test_target_description(self, pyinstrument_invocation, tmp_path: Path):
        busy_wait_py = tmp_path / "busy_wait.py"
        busy_wait_py.write_text(BUSY_WAIT_SCRIPT)

        output = subprocess.check_output(
            [
                *pyinstrument_invocation,
                "--target-description",
                "'foobar'",
                str(busy_wait_py),
            ]
        )

        assert "foobar" in str(output)

    def test_target_description_format(self, pyinstrument_invocation, tmp_path: Path):
        busy_wait_py = tmp_path / "busy_wait.py"
        busy_wait_py.write_text(BUSY_WAIT_SCRIPT)

        output = subprocess.check_output(
            [
                *pyinstrument_invocation,
                "--target-description",
                "'foobar {args}'",
                str(busy_wait_py),
            ],
            text=True,
        )

        assert f"foobar {busy_wait_py}" in output

    def test_target_description_format_errors(self, pyinstrument_invocation, tmp_path: Path):
        busy_wait_py = tmp_path / "busy_wait.py"
        busy_wait_py.write_text(BUSY_WAIT_SCRIPT)

        result = subprocess.run(
            [
                *pyinstrument_invocation,
                "--target-description",
                "''{foo}'",
                str(busy_wait_py),
            ],
            text=True,
            stderr=subprocess.PIPE,
        )

        assert f"Unknown placeholder 'foo'" in str(result.stderr)
        assert result.returncode == 2

        result = subprocess.run(
            [
                *pyinstrument_invocation,
                "--target-description",
                "''{}'",
                str(busy_wait_py),
            ],
            text=True,
            stderr=subprocess.PIPE,
        )

        assert f"Empty placeholder" in str(result.stderr)
        assert result.returncode == 2

    def test_binary_output(self, pyinstrument_invocation, tmp_path: Path):
        busy_wait_py = tmp_path / "busy_wait.py"
        busy_wait_py.write_text(BUSY_WAIT_SCRIPT)

        output_file = tmp_path / "output.pstats"

        subprocess.check_call(
            [
                *pyinstrument_invocation,
                "--renderer=pstats",
                f"--outfile={output_file}",
                str(busy_wait_py),
            ],
            universal_newlines=True,
        )

        assert output_file.exists()

        # check it can be loaded
        import pstats

        stats = pstats.Stats(str(output_file))
        assert stats

    def test_multiple_outfiles(self, pyinstrument_invocation, tmp_path: Path):
        busy_wait_py = tmp_path / "busy_wait.py"
        busy_wait_py.write_text(BUSY_WAIT_SCRIPT)

        html_file = tmp_path / "profile.html"
        text_file = tmp_path / "profile.txt"
        session_file = tmp_path / "profile.pyisession"

        subprocess.check_call(
            [
                *pyinstrument_invocation,
                "-o",
                str(html_file),
                "-o",
                str(text_file),
                f"--outfile={session_file}",
                str(busy_wait_py),
            ],
        )

        # each outfile gets the format that matches its extension
        assert "<html" in html_file.read_text()
        text_output = text_file.read_text()
        assert "busy_wait" in text_output
        assert "<html" not in text_output

        from pyinstrument.session import Session

        Session.load(session_file)

    def test_single_renderer_applies_to_all_outfiles(self, pyinstrument_invocation, tmp_path: Path):
        busy_wait_py = tmp_path / "busy_wait.py"
        busy_wait_py.write_text(BUSY_WAIT_SCRIPT)

        html_file = tmp_path / "profile.html"
        text_file = tmp_path / "profile.txt"

        subprocess.check_call(
            [
                *pyinstrument_invocation,
                "-o",
                str(html_file),
                "-r",
                "json",
                "-o",
                str(text_file),
                str(busy_wait_py),
            ],
        )

        assert "root_frame" in json.loads(html_file.read_text())
        assert "root_frame" in json.loads(text_file.read_text())

    def test_multiple_renderers(self, pyinstrument_invocation, tmp_path: Path):
        busy_wait_py = tmp_path / "busy_wait.py"
        busy_wait_py.write_text(BUSY_WAIT_SCRIPT)

        guessed_file = tmp_path / "guessed.html"
        text_file_1 = tmp_path / "profile1.log"
        text_file_2 = tmp_path / "profile2.log"
        json_file = tmp_path / "profile.data"

        subprocess.check_call(
            [
                *pyinstrument_invocation,
                "-o",
                str(guessed_file),
                "-r",
                "text",
                "-o",
                str(text_file_1),
                "-o",
                str(text_file_2),
                "--renderer=json",
                "-o",
                str(json_file),
                str(busy_wait_py),
            ],
        )

        # an outfile before the first --renderer still uses its extension
        assert "<html" in guessed_file.read_text()
        assert "busy_wait" in text_file_1.read_text()
        assert "busy_wait" in text_file_2.read_text()
        assert "root_frame" in json.loads(json_file.read_text())

    @pytest.mark.parametrize(
        "output_args",
        [
            ["-r", "text", "-r", "json"],
            ["-r", "text", "-r", "json", "-o", "profile.json"],
            ["-r", "text", "-o", "profile.txt", "-r", "json"],
        ],
    )
    def test_multiple_renderers_need_an_outfile_each(
        self, pyinstrument_invocation, tmp_path: Path, output_args
    ):
        busy_wait_py = tmp_path / "busy_wait.py"
        busy_wait_py.write_text(BUSY_WAIT_SCRIPT)

        result = subprocess.run(
            [*pyinstrument_invocation, *output_args, str(busy_wait_py)],
            cwd=tmp_path,
            stderr=subprocess.PIPE,
            text=True,
        )

        assert result.returncode == 2
        assert "--renderer" in result.stderr
        assert "--outfile" in result.stderr
        # nothing is written when the options are invalid
        assert not (tmp_path / "profile.json").exists()
        assert not (tmp_path / "profile.txt").exists()

    def test_program_exit_code(self, pyinstrument_invocation, tmp_path: Path):
        exit_1_py = tmp_path / "exit_1.py"
        exit_1_py.write_text("""import sys; sys.exit(1)""")

        retcode = subprocess.call(
            [
                *pyinstrument_invocation,
                str(exit_1_py),
            ],
        )

        assert retcode == 1
