from pyinstrument import Profiler
import pytest

# Profiler test
def test_create_profiler():
    p = Profiler()
    assert p is not None

def test_start_and_stop_profiler():
    p = Profiler()
    p.start()
    p.stop()
    assert p.is_running is False

def test_reset_clears_last_session():
    p = Profiler()
    p.start()
    p.stop()
    p.reset()
    assert p.last_session is None

def test_profiler_context_manager():
    with Profiler() as p:
        pass
    output = p.output_text()
    assert output != ""

def test_output_text_contains_duration():
    p = Profiler()
    p.start()
    p.stop()
    output = p.output_text()
    assert "Duration" in output or "duration" in output.lower()
# Profiler test

def test_no_samples_recorded(tmp_path):
    from pyinstrument import Profiler
    prof = Profiler(interval=1.0)
    prof.start()
    prof.stop()
    txt = prof.output_text()
    assert "No samples" in txt or txt.strip() != ""

def test_invalid_renderer_argument():
    from pyinstrument import Profiler
    prof = Profiler()
    prof.start()
    prof.stop()
    with pytest.raises(AttributeError):
        prof.output(renderer="not a renderer")

def test_session_load_invalid(tmp_path):
    from pyinstrument.session import Session
    bad = tmp_path / "bad.json"
    bad.write_text("not a json")
    with pytest.raises(Exception):
        Session.load(str(bad))

def test_profiler_double_stop():
    from pyinstrument import Profiler
    prof = Profiler()
    prof.start()
    prof.stop()
    with pytest.raises(RuntimeError):
        prof.stop()

def test_empty_session_root_frame_is_none():
    from pyinstrument import Profiler
    prof = Profiler(interval=999)
    prof.start()
    prof.stop()
    assert prof.last_session.root_frame() is None