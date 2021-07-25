from typing import Any

from .util import parametrize_setstatprofile


class CallCounter:
    def __init__(self) -> None:
        self.count = 0

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.count += 1


@parametrize_setstatprofile
def test_increment(setstatprofile):
    time = 0.0

    def fake_time():
        return time

    def fake_sleep(duration):
        nonlocal time
        time += duration

    counter = CallCounter()

    setstatprofile(counter, timer_func=fake_time)

    for _ in range(100):
        fake_sleep(1.0)

    setstatprofile(None)

    assert counter.count == 100
