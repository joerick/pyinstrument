import os
from typing import NoReturn
import time

from flaky import flaky

if "CI" in os.environ:
    # a decorator that allows some test flakyness in CI environments, presumably
    # due to contention. Useful for tests that rely on real time measurments.
    flaky_in_ci = flaky(max_runs=5, min_passes=2)
else:
    flaky_in_ci = lambda a: a


def assert_never(x: NoReturn) -> NoReturn:
    raise AssertionError(f"Invalid value: {x!r}")


def do_nothing():
    pass


def busy_wait(duration):
    end_time = time.time() + duration

    while time.time() < end_time:
        do_nothing()
