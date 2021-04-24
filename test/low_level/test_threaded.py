from typing import Any
from unittest import TestCase
import time, threading

from pyinstrument.low_level.stat_profile import setstatprofile
from ..util import busy_wait


class CallCounter:
    def __init__(self) -> None:
        self.count = 0

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.count += 1


def test_threaded():
    counter = CallCounter()

    def profile_a_busy_wait():
        setstatprofile(counter, 0.1)
        busy_wait(1.0)
        setstatprofile(None)

    threads = [threading.Thread(target=profile_a_busy_wait) for _ in range(10)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # threaded counts can be way lower, presumably due to the GIL.
    # Really we only care that it didn't crash!
    assert 50 < counter.count < 125
