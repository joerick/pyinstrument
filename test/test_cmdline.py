from __future__ import print_function
import time, sys, subprocess, os
import pytest

def test_command_line():
    test_script = os.path.join(os.path.dirname(__file__), 'busywait.py')
    output = subprocess.check_output([sys.executable, '-m', 'pyinstrument', test_script])

    assert 'busy_wait' in str(output)
    assert 'do_nothing' in str(output)

def test_module_running():
    working_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    output = subprocess.check_output(
        [sys.executable, '-m', 'pyinstrument', '-m', 'test.busywait_module'],
        cwd=working_dir
    )

    assert 'busy_wait' in str(output)
    assert 'do_nothing' in str(output)

