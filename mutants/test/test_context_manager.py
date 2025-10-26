from test.fake_time_util import fake_time

import pytest

import pyinstrument
from pyinstrument.context_manager import ProfileContext


def test_profile_context_decorator(capfd):
    with fake_time() as clock:

        @pyinstrument.profile
        def my_function():
            clock.sleep(1.0)

        my_function()

    out, err = capfd.readouterr()
    print(err)
    assert "Function test_profile_context_decorator" in err
    assert "1.000 my_function" in err


def test_profile_context_manager(capfd):
    with fake_time() as clock:
        with pyinstrument.profile():

            def my_function():
                clock.sleep(1.0)

            my_function()

    out, err = capfd.readouterr()
    print(err)
    assert "Block at" in err
    assert "1.000 my_function" in err
