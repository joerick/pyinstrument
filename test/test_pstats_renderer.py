import time
from pstats import Stats
from test.fake_time_util import fake_time
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
    pstats = PstatsRenderer().render(profiler_session)
    with open(fname, "w", encoding="utf-8", errors="surrogateescape") as fid:
        fid.write(pstats)
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
