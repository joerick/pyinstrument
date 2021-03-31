from __future__ import print_function
import os, subprocess, sys, textwrap
from pathlib import Path

import pytest

# this script just does a busywait for 0.25 seconds.
busy_wait_script = '''
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
'''


@pytest.mark.parametrize('invocation', (['pyinstrument'], [sys.executable, '-m', 'pyinstrument']))
class TestCommandLine:
    def test_command_line(self, invocation, tmp_path: Path):
        busy_wait_py = tmp_path / 'busy_wait.py'
        busy_wait_py.write_text(busy_wait_script)

        output = subprocess.check_output([*invocation, busy_wait_py])

        assert 'busy_wait' in str(output)
        assert 'do_nothing' in str(output)

    def test_module_running(self, invocation, tmp_path: Path):
        (tmp_path / 'busy_wait_module').mkdir()
        (tmp_path / 'busy_wait_module' / '__init__.py').touch()
        (tmp_path / 'busy_wait_module' / '__main__.py').write_text(busy_wait_script)

        output = subprocess.check_output(
            [*invocation, '-m', 'busy_wait_module'],
            cwd=tmp_path
        )

        assert 'busy_wait' in str(output)
        assert 'do_nothing' in str(output)


    def test_single_file_module_running(self, invocation, tmp_path: Path):
        busy_wait_py = tmp_path / 'busy_wait.py'
        busy_wait_py.write_text(busy_wait_script)

        output = subprocess.check_output(
            [*invocation, '-m', 'busy_wait'],
            cwd=tmp_path
        )

        assert 'busy_wait' in str(output)
        assert 'do_nothing' in str(output)

    def test_module_args(self, invocation, tmp_path: Path):
        (tmp_path / 'busy_wait_module').mkdir()
        (tmp_path / 'busy_wait_module' / '__init__.py').touch()
        (tmp_path / 'busy_wait_module' / '__main__.py').write_text(busy_wait_script)

        output = subprocess.check_output(
            [*invocation, '-m', 'busy_wait_module', '--test-argument'],
            cwd=tmp_path
        )

        assert "sys.argv:  ['busy_wait_module', '--test-argument']" in str(output)

    def test_running_yourself_as_module(self, invocation):
        subprocess.check_call(
            [*invocation, '-m', 'pyinstrument'],
        )

    def test_path(self, invocation, tmp_path: Path):
        PROGRAM_FILENAME = 'program'
        program_path = tmp_path / PROGRAM_FILENAME
        program_path.write_text(busy_wait_script)
        program_path.chmod(0x755)

        subprocess.check_call(
            [*invocation, '--from-path', '--', PROGRAM_FILENAME],
            env={'PATH': str(tmp_path) + os.pathsep + os.getenv('PATH')},
        )

    def test_path_execution_details(self, invocation, tmp_path: Path, monkeypatch):
        PROGRAM_FILENAME = 'program'
        program_path = tmp_path / PROGRAM_FILENAME
        program_path.write_text(textwrap.dedent(f'''
            #!{sys.executable}
            import sys, os
            print('__name__', __name__, file=sys.stderr)
            print('sys.argv', sys.argv, file=sys.stderr)
            print('sys.path', sys.path, file=sys.stderr)
            print('sys.executable', os.path.realpath(sys.executable), file=sys.stderr)
            print('os.getcwd()', os.getcwd(), file=sys.stderr)
        ''').strip())
        program_path.chmod(0x755)
        monkeypatch.setenv("PATH", str(tmp_path), prepend=os.pathsep)

        process_pyi = subprocess.run(
            [*invocation, '--from-path', '--', PROGRAM_FILENAME, 'arg1', 'arg2'],
            stderr=subprocess.PIPE,
            check=True,
        )
        process_native = subprocess.run(
            [PROGRAM_FILENAME, 'arg1', 'arg2'],
            stderr=subprocess.PIPE,
            check=True,
        )

        # check the execution environments match
        print('process_pyi.stderr', process_pyi.stderr)
        print('process_native.stderr', process_native.stderr)
        assert process_pyi.stderr == process_native.stderr
