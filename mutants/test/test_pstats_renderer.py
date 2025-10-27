import os
import time
from pathlib import Path
from pstats import Stats
from test.fake_time_util import FakeClock, fake_time
from typing import Any

import pytest

from pyinstrument import Profiler
from pyinstrument.renderers import PstatsRenderer


def a():
    b()
    c()


def b():
    d()


def c():
    d()


def d():
    e()


def e():
    time.sleep(1)


@pytest.fixture(scope="module")
def profiler_session():
    with fake_time():
        profiler = Profiler()
        profiler.start()

        a()

        profiler.stop()
        return profiler.last_session


def test_pstats_renderer(profiler_session, tmp_path):
    fname = tmp_path / "test.pstats"
    pstats_data = PstatsRenderer().render(profiler_session)
    with open(fname, "wb") as fid:
        fid.write(pstats_data.encode(encoding="utf-8", errors="surrogateescape"))
    stats: Any = Stats(str(fname))
    # Sanity check
    assert stats.total_tt > 0
    # The graph is
    # a() -> b() -> d() -> e() -> time.sleep()
    #    \-> c() /
    # so make sure d has callers of b, c, and that the times make sense

    # in stats,
    #   keys are tuples (file_path, line, func)
    #   values are tuples (calltime, numcalls, selftime, cumtime, callers)
    # in callers,
    #   keys are the same as in stats
    #   values are the same as stats but without callers

    # check the time of d
    d_key = [k for k in stats.stats.keys() if k[2] == "d"][0]
    d_val = stats.stats[d_key]
    d_cumtime = d_val[3]
    assert d_cumtime == pytest.approx(2)

    # check d's callers times are split
    b_key = [k for k in stats.stats.keys() if k[2] == "b"][0]
    c_key = [k for k in stats.stats.keys() if k[2] == "c"][0]
    d_callers = d_val[4]
    b_cumtime = d_callers[b_key][3]
    c_cumtime = d_callers[c_key][3]
    assert b_cumtime == pytest.approx(1)
    assert c_cumtime == pytest.approx(1)

    # check the time of e
    e_key = [k for k in stats.stats.keys() if k[2] == "e"][0]
    e_val = stats.stats[e_key]
    e_cumtime = e_val[3]
    assert e_cumtime == pytest.approx(2)


def test_round_trip_encoding_of_binary_data(tmp_path: Path):
    # as used by the pstats renderer
    data_blob = os.urandom(1024)
    file = tmp_path / "file.dat"

    data_blob_string = data_blob.decode(encoding="utf-8", errors="surrogateescape")

    # newline='' is required to prevent the default newline translation
    with open(file, mode="w", encoding="utf-8", errors="surrogateescape", newline="") as f:
        f.write(data_blob_string)

    assert data_blob == data_blob_string.encode(encoding="utf-8", errors="surrogateescape")
    assert data_blob == file.read_bytes()


def sleep_and_busy_wait(clock: FakeClock):
    time.sleep(1.0)
    # this looks like a busy wait to the profiler
    clock.time += 1.0


def test_sum_of_tottime(tmp_path):
    # Check that the sum of the tottime of all the functions is equal to the
    # total time of the profile

    with fake_time() as clock:
        profiler = Profiler()
        profiler.start()

        sleep_and_busy_wait(clock)

        profiler.stop()
        profiler_session = profiler.last_session

    assert profiler_session

    pstats_data = PstatsRenderer().render(profiler_session)
    fname = tmp_path / "test.pstats"
    with open(fname, "wb") as fid:
        fid.write(pstats_data.encode(encoding="utf-8", errors="surrogateescape"))
    stats: Any = Stats(str(fname))
    assert stats.total_tt == pytest.approx(2)
