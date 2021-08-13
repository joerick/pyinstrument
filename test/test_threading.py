import threading
import time
from test.fake_time_util import fake_time

import pytest

from pyinstrument import Profiler

from .util import do_nothing


def test_profiler_access_from_multiple_threads():
    profiler = Profiler()

    profiler.start()

    thread_exception = None

    def helper():
        while profiler._active_session and len(profiler._active_session.frame_records) < 10:
            time.sleep(0.0001)

        try:
            profiler.stop()
        except Exception as e:
            nonlocal thread_exception
            thread_exception = e

    t1 = threading.Thread(target=helper)
    t1.start()

    while t1.is_alive():
        do_nothing()
    t1.join()

    with pytest.raises(Exception) as excinfo:
        profiler.output_html()

    assert "this profiler is still running" in excinfo.value.args[0]

    assert thread_exception is not None
    assert (
        "Failed to stop profiling. Make sure that you start/stop profiling on the same thread."
        in thread_exception.args[0]
    )

    # the above stop failed. actually stop the profiler
    profiler.stop()
