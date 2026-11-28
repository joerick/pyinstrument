import subprocess
import sys
import textwrap
import threading
import time

import pytest

from pyinstrument import Profiler
from test.fake_time_util import fake_time

from .util import do_nothing


def test_sampling_does_not_register_dummy_threads():
    # gevent can change get_ident before updating threading's registry. Keep
    # that temporary inconsistency isolated from the test runner's threads.
    code = textwrap.dedent(
        """
        import threading
        import time
        from pyinstrument import Profiler

        before = threading.enumerate()
        original_get_ident = threading.get_ident
        profiler = Profiler()
        profiler.start()
        try:
            threading.get_ident = lambda: -1
            for _ in range(5):
                time.sleep(0.01)
        finally:
            threading.get_ident = original_get_ident
            profiler.stop()

        assert profiler.last_session is not None
        assert profiler.last_session.frame_records
        assert threading.enumerate() == before, "Sampling registered a dummy thread"
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_sampling_uses_updated_thread_name():
    thread = threading.current_thread()
    original_name = thread.name
    profiler = Profiler()
    try:
        profiler.start()
        thread.name = "renamed-profiled-thread"
        time.sleep(0.05)
        session = profiler.stop()
    finally:
        thread.name = original_name

    assert any(
        stack[0].startswith("renamed-profiled-thread\x00<thread>\x00")
        for stack, _ in session.frame_records
    )


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
