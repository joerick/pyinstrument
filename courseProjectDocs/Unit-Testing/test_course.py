from pyinstrument import Profiler

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
