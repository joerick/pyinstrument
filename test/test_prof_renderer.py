import time
from pstats import Stats

import pytest

from pyinstrument import Profiler
from pyinstrument.renderers import ProfRenderer


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
    profiler = Profiler()
    profiler.start()

    a()

    profiler.stop()
    return profiler.last_session


def test_prof_renderer(profiler_session, tmp_path):
    fname = tmp_path / "test.prof"
    prof = ProfRenderer().render(profiler_session)
    with open(fname, "wb") as fid:
        fid.write(prof)
    stats = Stats(str(fname))
    # Sanity check
    assert stats.total_tt > 0
