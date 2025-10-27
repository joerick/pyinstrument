from __future__ import annotations

import threading
import time
from typing import Any, List
from unittest import TestCase

import pytest

from pyinstrument.low_level.stat_profile import setstatprofile

from ..util import busy_wait, do_nothing


class CallCounter:
    def __init__(self, thread) -> None:
        self.thread = thread
        self.count = 0

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        assert self.thread is threading.current_thread()
        self.count += 1


def test_threaded():
    # assert that each thread gets its own callbacks, and check that it
    # doesn't crash!

    counters: list[CallCounter | None] = [None for _ in range(10)]
    stop = False

    def profile_a_busy_wait(i):
        thread = threads[i]
        counter = CallCounter(thread)
        counters[i] = counter

        setstatprofile(counter, 0.001)
        while not stop:
            do_nothing()
        setstatprofile(None)

    threads = [threading.Thread(target=profile_a_busy_wait, args=(i,)) for i in range(10)]
    for thread in threads:
        thread.start()

    while not stop:
        stop = all(c is not None and c.count > 10 for c in counters)

    for thread in threads:
        thread.join()
