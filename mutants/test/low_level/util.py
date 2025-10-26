import functools

import pytest

from pyinstrument.low_level.stat_profile import setstatprofile as setstatprofile_c
from pyinstrument.low_level.stat_profile_python import setstatprofile as setstatprofile_python

"""
Parametrizes the test with both the C and Python setstatprofile, just to check
that the Python one is up-to-date with the C version.
"""
parametrize_setstatprofile = pytest.mark.parametrize(
    "setstatprofile",
    [setstatprofile_c, setstatprofile_python],
)
