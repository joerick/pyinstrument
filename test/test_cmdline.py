from __future__ import print_function
import sys, subprocess, os
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

def test_command_line(tmp_path: Path):
    busy_wait_py = tmp_path / 'busy_wait.py'
    busy_wait_py.write_text(busy_wait_script)
    
    output = subprocess.check_output([sys.executable, '-m', 'pyinstrument', busy_wait_py])

    assert 'busy_wait' in str(output)
    assert 'do_nothing' in str(output)

def test_module_running(tmp_path: Path):
    (tmp_path / 'busy_wait_module').mkdir()
    (tmp_path / 'busy_wait_module' / '__init__.py').touch()
    (tmp_path / 'busy_wait_module' / '__main__.py').write_text(busy_wait_script)

    output = subprocess.check_output(
        [sys.executable, '-m', 'pyinstrument', '-m', 'busy_wait_module'],
        cwd=tmp_path
    )

    assert 'busy_wait' in str(output)
    assert 'do_nothing' in str(output)


def test_single_file_module_running(tmp_path: Path):
    busy_wait_py = tmp_path / 'busy_wait.py'
    busy_wait_py.write_text(busy_wait_script)

    output = subprocess.check_output(
        [sys.executable, '-m', 'pyinstrument', '-m', 'busy_wait'],
        cwd=tmp_path
    )

    assert 'busy_wait' in str(output)
    assert 'do_nothing' in str(output)


def test_module_args(tmp_path: Path):
    (tmp_path / 'busy_wait_module').mkdir()
    (tmp_path / 'busy_wait_module' / '__init__.py').touch()
    (tmp_path / 'busy_wait_module' / '__main__.py').write_text(busy_wait_script)

    output = subprocess.check_output(
        [sys.executable, '-m', 'pyinstrument', '-m', 'busy_wait_module', '--test-argument'],
        cwd=tmp_path
    )

    assert "sys.argv:  ['busy_wait_module', '--test-argument']" in str(output)

def test_running_yourself_as_module():
    subprocess.check_call(
        [sys.executable, '-m', 'pyinstrument', '-m', 'pyinstrument'],
    )
