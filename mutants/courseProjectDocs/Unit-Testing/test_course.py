from pyinstrument import Profiler
from pyinstrument.frame import Frame
import pytest
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result

# Profiler test
def x_test_create_profiler__mutmut_orig():
    p = Profiler()
    assert p is not None

# Profiler test
def x_test_create_profiler__mutmut_1():
    p = None
    assert p is not None

# Profiler test
def x_test_create_profiler__mutmut_2():
    p = Profiler()
    assert p is None

x_test_create_profiler__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_create_profiler__mutmut_1': x_test_create_profiler__mutmut_1, 
    'x_test_create_profiler__mutmut_2': x_test_create_profiler__mutmut_2
}

def test_create_profiler(*args, **kwargs):
    result = _mutmut_trampoline(x_test_create_profiler__mutmut_orig, x_test_create_profiler__mutmut_mutants, args, kwargs)
    return result 

test_create_profiler.__signature__ = _mutmut_signature(x_test_create_profiler__mutmut_orig)
x_test_create_profiler__mutmut_orig.__name__ = 'x_test_create_profiler'

def x_test_start_and_stop_profiler__mutmut_orig():
    p = Profiler()
    p.start()
    p.stop()
    assert p.is_running is False

def x_test_start_and_stop_profiler__mutmut_1():
    p = None
    p.start()
    p.stop()
    assert p.is_running is False

def x_test_start_and_stop_profiler__mutmut_2():
    p = Profiler()
    p.start()
    p.stop()
    assert p.is_running is not False

def x_test_start_and_stop_profiler__mutmut_3():
    p = Profiler()
    p.start()
    p.stop()
    assert p.is_running is True

x_test_start_and_stop_profiler__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_start_and_stop_profiler__mutmut_1': x_test_start_and_stop_profiler__mutmut_1, 
    'x_test_start_and_stop_profiler__mutmut_2': x_test_start_and_stop_profiler__mutmut_2, 
    'x_test_start_and_stop_profiler__mutmut_3': x_test_start_and_stop_profiler__mutmut_3
}

def test_start_and_stop_profiler(*args, **kwargs):
    result = _mutmut_trampoline(x_test_start_and_stop_profiler__mutmut_orig, x_test_start_and_stop_profiler__mutmut_mutants, args, kwargs)
    return result 

test_start_and_stop_profiler.__signature__ = _mutmut_signature(x_test_start_and_stop_profiler__mutmut_orig)
x_test_start_and_stop_profiler__mutmut_orig.__name__ = 'x_test_start_and_stop_profiler'

def x_test_reset_clears_last_session__mutmut_orig():
    p = Profiler()
    p.start()
    p.stop()
    p.reset()
    assert p.last_session is None

def x_test_reset_clears_last_session__mutmut_1():
    p = None
    p.start()
    p.stop()
    p.reset()
    assert p.last_session is None

def x_test_reset_clears_last_session__mutmut_2():
    p = Profiler()
    p.start()
    p.stop()
    p.reset()
    assert p.last_session is not None

x_test_reset_clears_last_session__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_reset_clears_last_session__mutmut_1': x_test_reset_clears_last_session__mutmut_1, 
    'x_test_reset_clears_last_session__mutmut_2': x_test_reset_clears_last_session__mutmut_2
}

def test_reset_clears_last_session(*args, **kwargs):
    result = _mutmut_trampoline(x_test_reset_clears_last_session__mutmut_orig, x_test_reset_clears_last_session__mutmut_mutants, args, kwargs)
    return result 

test_reset_clears_last_session.__signature__ = _mutmut_signature(x_test_reset_clears_last_session__mutmut_orig)
x_test_reset_clears_last_session__mutmut_orig.__name__ = 'x_test_reset_clears_last_session'

def x_test_profiler_context_manager__mutmut_orig():
    with Profiler() as p:
        pass
    output = p.output_text()
    assert output != ""

def x_test_profiler_context_manager__mutmut_1():
    with Profiler() as p:
        pass
    output = None
    assert output != ""

def x_test_profiler_context_manager__mutmut_2():
    with Profiler() as p:
        pass
    output = p.output_text()
    assert output == ""

def x_test_profiler_context_manager__mutmut_3():
    with Profiler() as p:
        pass
    output = p.output_text()
    assert output != "XXXX"

x_test_profiler_context_manager__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_profiler_context_manager__mutmut_1': x_test_profiler_context_manager__mutmut_1, 
    'x_test_profiler_context_manager__mutmut_2': x_test_profiler_context_manager__mutmut_2, 
    'x_test_profiler_context_manager__mutmut_3': x_test_profiler_context_manager__mutmut_3
}

def test_profiler_context_manager(*args, **kwargs):
    result = _mutmut_trampoline(x_test_profiler_context_manager__mutmut_orig, x_test_profiler_context_manager__mutmut_mutants, args, kwargs)
    return result 

test_profiler_context_manager.__signature__ = _mutmut_signature(x_test_profiler_context_manager__mutmut_orig)
x_test_profiler_context_manager__mutmut_orig.__name__ = 'x_test_profiler_context_manager'

def x_test_output_text_contains_duration__mutmut_orig():
    p = Profiler()
    p.start()
    p.stop()
    output = p.output_text()
    assert "Duration" in output or "duration" in output.lower()

def x_test_output_text_contains_duration__mutmut_1():
    p = None
    p.start()
    p.stop()
    output = p.output_text()
    assert "Duration" in output or "duration" in output.lower()

def x_test_output_text_contains_duration__mutmut_2():
    p = Profiler()
    p.start()
    p.stop()
    output = None
    assert "Duration" in output or "duration" in output.lower()

def x_test_output_text_contains_duration__mutmut_3():
    p = Profiler()
    p.start()
    p.stop()
    output = p.output_text()
    assert "Duration" in output and "duration" in output.lower()

def x_test_output_text_contains_duration__mutmut_4():
    p = Profiler()
    p.start()
    p.stop()
    output = p.output_text()
    assert "XXDurationXX" in output or "duration" in output.lower()

def x_test_output_text_contains_duration__mutmut_5():
    p = Profiler()
    p.start()
    p.stop()
    output = p.output_text()
    assert "duration" in output or "duration" in output.lower()

def x_test_output_text_contains_duration__mutmut_6():
    p = Profiler()
    p.start()
    p.stop()
    output = p.output_text()
    assert "DURATION" in output or "duration" in output.lower()

def x_test_output_text_contains_duration__mutmut_7():
    p = Profiler()
    p.start()
    p.stop()
    output = p.output_text()
    assert "Duration" not in output or "duration" in output.lower()

def x_test_output_text_contains_duration__mutmut_8():
    p = Profiler()
    p.start()
    p.stop()
    output = p.output_text()
    assert "Duration" in output or "XXdurationXX" in output.lower()

def x_test_output_text_contains_duration__mutmut_9():
    p = Profiler()
    p.start()
    p.stop()
    output = p.output_text()
    assert "Duration" in output or "DURATION" in output.lower()

def x_test_output_text_contains_duration__mutmut_10():
    p = Profiler()
    p.start()
    p.stop()
    output = p.output_text()
    assert "Duration" in output or "duration" not in output.lower()

def x_test_output_text_contains_duration__mutmut_11():
    p = Profiler()
    p.start()
    p.stop()
    output = p.output_text()
    assert "Duration" in output or "duration" in output.upper()

x_test_output_text_contains_duration__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_output_text_contains_duration__mutmut_1': x_test_output_text_contains_duration__mutmut_1, 
    'x_test_output_text_contains_duration__mutmut_2': x_test_output_text_contains_duration__mutmut_2, 
    'x_test_output_text_contains_duration__mutmut_3': x_test_output_text_contains_duration__mutmut_3, 
    'x_test_output_text_contains_duration__mutmut_4': x_test_output_text_contains_duration__mutmut_4, 
    'x_test_output_text_contains_duration__mutmut_5': x_test_output_text_contains_duration__mutmut_5, 
    'x_test_output_text_contains_duration__mutmut_6': x_test_output_text_contains_duration__mutmut_6, 
    'x_test_output_text_contains_duration__mutmut_7': x_test_output_text_contains_duration__mutmut_7, 
    'x_test_output_text_contains_duration__mutmut_8': x_test_output_text_contains_duration__mutmut_8, 
    'x_test_output_text_contains_duration__mutmut_9': x_test_output_text_contains_duration__mutmut_9, 
    'x_test_output_text_contains_duration__mutmut_10': x_test_output_text_contains_duration__mutmut_10, 
    'x_test_output_text_contains_duration__mutmut_11': x_test_output_text_contains_duration__mutmut_11
}

def test_output_text_contains_duration(*args, **kwargs):
    result = _mutmut_trampoline(x_test_output_text_contains_duration__mutmut_orig, x_test_output_text_contains_duration__mutmut_mutants, args, kwargs)
    return result 

test_output_text_contains_duration.__signature__ = _mutmut_signature(x_test_output_text_contains_duration__mutmut_orig)
x_test_output_text_contains_duration__mutmut_orig.__name__ = 'x_test_output_text_contains_duration'
# Profiler test

def x_test_no_samples_recorded__mutmut_orig(tmp_path):
    from pyinstrument import Profiler
    prof = Profiler(interval=1.0)
    prof.start()
    prof.stop()
    txt = prof.output_text()
    assert "No samples" in txt or txt.strip() != ""
# Profiler test

def x_test_no_samples_recorded__mutmut_1(tmp_path):
    from pyinstrument import Profiler
    prof = None
    prof.start()
    prof.stop()
    txt = prof.output_text()
    assert "No samples" in txt or txt.strip() != ""
# Profiler test

def x_test_no_samples_recorded__mutmut_2(tmp_path):
    from pyinstrument import Profiler
    prof = Profiler(interval=None)
    prof.start()
    prof.stop()
    txt = prof.output_text()
    assert "No samples" in txt or txt.strip() != ""
# Profiler test

def x_test_no_samples_recorded__mutmut_3(tmp_path):
    from pyinstrument import Profiler
    prof = Profiler(interval=2.0)
    prof.start()
    prof.stop()
    txt = prof.output_text()
    assert "No samples" in txt or txt.strip() != ""
# Profiler test

def x_test_no_samples_recorded__mutmut_4(tmp_path):
    from pyinstrument import Profiler
    prof = Profiler(interval=1.0)
    prof.start()
    prof.stop()
    txt = None
    assert "No samples" in txt or txt.strip() != ""
# Profiler test

def x_test_no_samples_recorded__mutmut_5(tmp_path):
    from pyinstrument import Profiler
    prof = Profiler(interval=1.0)
    prof.start()
    prof.stop()
    txt = prof.output_text()
    assert "No samples" in txt and txt.strip() != ""
# Profiler test

def x_test_no_samples_recorded__mutmut_6(tmp_path):
    from pyinstrument import Profiler
    prof = Profiler(interval=1.0)
    prof.start()
    prof.stop()
    txt = prof.output_text()
    assert "XXNo samplesXX" in txt or txt.strip() != ""
# Profiler test

def x_test_no_samples_recorded__mutmut_7(tmp_path):
    from pyinstrument import Profiler
    prof = Profiler(interval=1.0)
    prof.start()
    prof.stop()
    txt = prof.output_text()
    assert "no samples" in txt or txt.strip() != ""
# Profiler test

def x_test_no_samples_recorded__mutmut_8(tmp_path):
    from pyinstrument import Profiler
    prof = Profiler(interval=1.0)
    prof.start()
    prof.stop()
    txt = prof.output_text()
    assert "NO SAMPLES" in txt or txt.strip() != ""
# Profiler test

def x_test_no_samples_recorded__mutmut_9(tmp_path):
    from pyinstrument import Profiler
    prof = Profiler(interval=1.0)
    prof.start()
    prof.stop()
    txt = prof.output_text()
    assert "No samples" not in txt or txt.strip() != ""
# Profiler test

def x_test_no_samples_recorded__mutmut_10(tmp_path):
    from pyinstrument import Profiler
    prof = Profiler(interval=1.0)
    prof.start()
    prof.stop()
    txt = prof.output_text()
    assert "No samples" in txt or txt.strip() == ""
# Profiler test

def x_test_no_samples_recorded__mutmut_11(tmp_path):
    from pyinstrument import Profiler
    prof = Profiler(interval=1.0)
    prof.start()
    prof.stop()
    txt = prof.output_text()
    assert "No samples" in txt or txt.strip() != "XXXX"

x_test_no_samples_recorded__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_no_samples_recorded__mutmut_1': x_test_no_samples_recorded__mutmut_1, 
    'x_test_no_samples_recorded__mutmut_2': x_test_no_samples_recorded__mutmut_2, 
    'x_test_no_samples_recorded__mutmut_3': x_test_no_samples_recorded__mutmut_3, 
    'x_test_no_samples_recorded__mutmut_4': x_test_no_samples_recorded__mutmut_4, 
    'x_test_no_samples_recorded__mutmut_5': x_test_no_samples_recorded__mutmut_5, 
    'x_test_no_samples_recorded__mutmut_6': x_test_no_samples_recorded__mutmut_6, 
    'x_test_no_samples_recorded__mutmut_7': x_test_no_samples_recorded__mutmut_7, 
    'x_test_no_samples_recorded__mutmut_8': x_test_no_samples_recorded__mutmut_8, 
    'x_test_no_samples_recorded__mutmut_9': x_test_no_samples_recorded__mutmut_9, 
    'x_test_no_samples_recorded__mutmut_10': x_test_no_samples_recorded__mutmut_10, 
    'x_test_no_samples_recorded__mutmut_11': x_test_no_samples_recorded__mutmut_11
}

def test_no_samples_recorded(*args, **kwargs):
    result = _mutmut_trampoline(x_test_no_samples_recorded__mutmut_orig, x_test_no_samples_recorded__mutmut_mutants, args, kwargs)
    return result 

test_no_samples_recorded.__signature__ = _mutmut_signature(x_test_no_samples_recorded__mutmut_orig)
x_test_no_samples_recorded__mutmut_orig.__name__ = 'x_test_no_samples_recorded'

def x_test_invalid_renderer_argument__mutmut_orig():
    from pyinstrument import Profiler
    prof = Profiler()
    prof.start()
    prof.stop()
    with pytest.raises(AttributeError):
        prof.output(renderer="not a renderer")

def x_test_invalid_renderer_argument__mutmut_1():
    from pyinstrument import Profiler
    prof = None
    prof.start()
    prof.stop()
    with pytest.raises(AttributeError):
        prof.output(renderer="not a renderer")

def x_test_invalid_renderer_argument__mutmut_2():
    from pyinstrument import Profiler
    prof = Profiler()
    prof.start()
    prof.stop()
    with pytest.raises(None):
        prof.output(renderer="not a renderer")

def x_test_invalid_renderer_argument__mutmut_3():
    from pyinstrument import Profiler
    prof = Profiler()
    prof.start()
    prof.stop()
    with pytest.raises(AttributeError):
        prof.output(renderer=None)

def x_test_invalid_renderer_argument__mutmut_4():
    from pyinstrument import Profiler
    prof = Profiler()
    prof.start()
    prof.stop()
    with pytest.raises(AttributeError):
        prof.output(renderer="XXnot a rendererXX")

def x_test_invalid_renderer_argument__mutmut_5():
    from pyinstrument import Profiler
    prof = Profiler()
    prof.start()
    prof.stop()
    with pytest.raises(AttributeError):
        prof.output(renderer="NOT A RENDERER")

x_test_invalid_renderer_argument__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_invalid_renderer_argument__mutmut_1': x_test_invalid_renderer_argument__mutmut_1, 
    'x_test_invalid_renderer_argument__mutmut_2': x_test_invalid_renderer_argument__mutmut_2, 
    'x_test_invalid_renderer_argument__mutmut_3': x_test_invalid_renderer_argument__mutmut_3, 
    'x_test_invalid_renderer_argument__mutmut_4': x_test_invalid_renderer_argument__mutmut_4, 
    'x_test_invalid_renderer_argument__mutmut_5': x_test_invalid_renderer_argument__mutmut_5
}

def test_invalid_renderer_argument(*args, **kwargs):
    result = _mutmut_trampoline(x_test_invalid_renderer_argument__mutmut_orig, x_test_invalid_renderer_argument__mutmut_mutants, args, kwargs)
    return result 

test_invalid_renderer_argument.__signature__ = _mutmut_signature(x_test_invalid_renderer_argument__mutmut_orig)
x_test_invalid_renderer_argument__mutmut_orig.__name__ = 'x_test_invalid_renderer_argument'

def x_test_session_load_invalid__mutmut_orig(tmp_path):
    from pyinstrument.session import Session
    bad = tmp_path / "bad.json"
    bad.write_text("not a json")
    with pytest.raises(Exception):
        Session.load(str(bad))

def x_test_session_load_invalid__mutmut_1(tmp_path):
    from pyinstrument.session import Session
    bad = None
    bad.write_text("not a json")
    with pytest.raises(Exception):
        Session.load(str(bad))

def x_test_session_load_invalid__mutmut_2(tmp_path):
    from pyinstrument.session import Session
    bad = tmp_path * "bad.json"
    bad.write_text("not a json")
    with pytest.raises(Exception):
        Session.load(str(bad))

def x_test_session_load_invalid__mutmut_3(tmp_path):
    from pyinstrument.session import Session
    bad = tmp_path / "XXbad.jsonXX"
    bad.write_text("not a json")
    with pytest.raises(Exception):
        Session.load(str(bad))

def x_test_session_load_invalid__mutmut_4(tmp_path):
    from pyinstrument.session import Session
    bad = tmp_path / "BAD.JSON"
    bad.write_text("not a json")
    with pytest.raises(Exception):
        Session.load(str(bad))

def x_test_session_load_invalid__mutmut_5(tmp_path):
    from pyinstrument.session import Session
    bad = tmp_path / "bad.json"
    bad.write_text(None)
    with pytest.raises(Exception):
        Session.load(str(bad))

def x_test_session_load_invalid__mutmut_6(tmp_path):
    from pyinstrument.session import Session
    bad = tmp_path / "bad.json"
    bad.write_text("XXnot a jsonXX")
    with pytest.raises(Exception):
        Session.load(str(bad))

def x_test_session_load_invalid__mutmut_7(tmp_path):
    from pyinstrument.session import Session
    bad = tmp_path / "bad.json"
    bad.write_text("NOT A JSON")
    with pytest.raises(Exception):
        Session.load(str(bad))

def x_test_session_load_invalid__mutmut_8(tmp_path):
    from pyinstrument.session import Session
    bad = tmp_path / "bad.json"
    bad.write_text("not a json")
    with pytest.raises(None):
        Session.load(str(bad))

def x_test_session_load_invalid__mutmut_9(tmp_path):
    from pyinstrument.session import Session
    bad = tmp_path / "bad.json"
    bad.write_text("not a json")
    with pytest.raises(Exception):
        Session.load(None)

def x_test_session_load_invalid__mutmut_10(tmp_path):
    from pyinstrument.session import Session
    bad = tmp_path / "bad.json"
    bad.write_text("not a json")
    with pytest.raises(Exception):
        Session.load(str(None))

x_test_session_load_invalid__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_session_load_invalid__mutmut_1': x_test_session_load_invalid__mutmut_1, 
    'x_test_session_load_invalid__mutmut_2': x_test_session_load_invalid__mutmut_2, 
    'x_test_session_load_invalid__mutmut_3': x_test_session_load_invalid__mutmut_3, 
    'x_test_session_load_invalid__mutmut_4': x_test_session_load_invalid__mutmut_4, 
    'x_test_session_load_invalid__mutmut_5': x_test_session_load_invalid__mutmut_5, 
    'x_test_session_load_invalid__mutmut_6': x_test_session_load_invalid__mutmut_6, 
    'x_test_session_load_invalid__mutmut_7': x_test_session_load_invalid__mutmut_7, 
    'x_test_session_load_invalid__mutmut_8': x_test_session_load_invalid__mutmut_8, 
    'x_test_session_load_invalid__mutmut_9': x_test_session_load_invalid__mutmut_9, 
    'x_test_session_load_invalid__mutmut_10': x_test_session_load_invalid__mutmut_10
}

def test_session_load_invalid(*args, **kwargs):
    result = _mutmut_trampoline(x_test_session_load_invalid__mutmut_orig, x_test_session_load_invalid__mutmut_mutants, args, kwargs)
    return result 

test_session_load_invalid.__signature__ = _mutmut_signature(x_test_session_load_invalid__mutmut_orig)
x_test_session_load_invalid__mutmut_orig.__name__ = 'x_test_session_load_invalid'

def x_test_profiler_double_stop__mutmut_orig():
    from pyinstrument import Profiler
    prof = Profiler()
    prof.start()
    prof.stop()
    with pytest.raises(RuntimeError):
        prof.stop()

def x_test_profiler_double_stop__mutmut_1():
    from pyinstrument import Profiler
    prof = None
    prof.start()
    prof.stop()
    with pytest.raises(RuntimeError):
        prof.stop()

def x_test_profiler_double_stop__mutmut_2():
    from pyinstrument import Profiler
    prof = Profiler()
    prof.start()
    prof.stop()
    with pytest.raises(None):
        prof.stop()

x_test_profiler_double_stop__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_profiler_double_stop__mutmut_1': x_test_profiler_double_stop__mutmut_1, 
    'x_test_profiler_double_stop__mutmut_2': x_test_profiler_double_stop__mutmut_2
}

def test_profiler_double_stop(*args, **kwargs):
    result = _mutmut_trampoline(x_test_profiler_double_stop__mutmut_orig, x_test_profiler_double_stop__mutmut_mutants, args, kwargs)
    return result 

test_profiler_double_stop.__signature__ = _mutmut_signature(x_test_profiler_double_stop__mutmut_orig)
x_test_profiler_double_stop__mutmut_orig.__name__ = 'x_test_profiler_double_stop'

def x_test_empty_session_root_frame_is_none__mutmut_orig():
    from pyinstrument import Profiler
    prof = Profiler(interval=999)
    prof.start()
    prof.stop()
    assert prof.last_session.root_frame() is None

def x_test_empty_session_root_frame_is_none__mutmut_1():
    from pyinstrument import Profiler
    prof = None
    prof.start()
    prof.stop()
    assert prof.last_session.root_frame() is None

def x_test_empty_session_root_frame_is_none__mutmut_2():
    from pyinstrument import Profiler
    prof = Profiler(interval=None)
    prof.start()
    prof.stop()
    assert prof.last_session.root_frame() is None

def x_test_empty_session_root_frame_is_none__mutmut_3():
    from pyinstrument import Profiler
    prof = Profiler(interval=1000)
    prof.start()
    prof.stop()
    assert prof.last_session.root_frame() is None

def x_test_empty_session_root_frame_is_none__mutmut_4():
    from pyinstrument import Profiler
    prof = Profiler(interval=999)
    prof.start()
    prof.stop()
    assert prof.last_session.root_frame() is not None

x_test_empty_session_root_frame_is_none__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_empty_session_root_frame_is_none__mutmut_1': x_test_empty_session_root_frame_is_none__mutmut_1, 
    'x_test_empty_session_root_frame_is_none__mutmut_2': x_test_empty_session_root_frame_is_none__mutmut_2, 
    'x_test_empty_session_root_frame_is_none__mutmut_3': x_test_empty_session_root_frame_is_none__mutmut_3, 
    'x_test_empty_session_root_frame_is_none__mutmut_4': x_test_empty_session_root_frame_is_none__mutmut_4
}

def test_empty_session_root_frame_is_none(*args, **kwargs):
    result = _mutmut_trampoline(x_test_empty_session_root_frame_is_none__mutmut_orig, x_test_empty_session_root_frame_is_none__mutmut_mutants, args, kwargs)
    return result 

test_empty_session_root_frame_is_none.__signature__ = _mutmut_signature(x_test_empty_session_root_frame_is_none__mutmut_orig)
x_test_empty_session_root_frame_is_none__mutmut_orig.__name__ = 'x_test_empty_session_root_frame_is_none'

# Frame Tests
def x_test_add_child_to_parent__mutmut_orig():
    parent = Frame("parent")  
    child = Frame ("child")  
    
    parent.add_child(child)  
    
    assert child in parent.children
    

# Frame Tests
def x_test_add_child_to_parent__mutmut_1():
    parent = None  
    child = Frame ("child")  
    
    parent.add_child(child)  
    
    assert child in parent.children
    

# Frame Tests
def x_test_add_child_to_parent__mutmut_2():
    parent = Frame(None)  
    child = Frame ("child")  
    
    parent.add_child(child)  
    
    assert child in parent.children
    

# Frame Tests
def x_test_add_child_to_parent__mutmut_3():
    parent = Frame("XXparentXX")  
    child = Frame ("child")  
    
    parent.add_child(child)  
    
    assert child in parent.children
    

# Frame Tests
def x_test_add_child_to_parent__mutmut_4():
    parent = Frame("PARENT")  
    child = Frame ("child")  
    
    parent.add_child(child)  
    
    assert child in parent.children
    

# Frame Tests
def x_test_add_child_to_parent__mutmut_5():
    parent = Frame("parent")  
    child = None  
    
    parent.add_child(child)  
    
    assert child in parent.children
    

# Frame Tests
def x_test_add_child_to_parent__mutmut_6():
    parent = Frame("parent")  
    child = Frame (None)  
    
    parent.add_child(child)  
    
    assert child in parent.children
    

# Frame Tests
def x_test_add_child_to_parent__mutmut_7():
    parent = Frame("parent")  
    child = Frame ("XXchildXX")  
    
    parent.add_child(child)  
    
    assert child in parent.children
    

# Frame Tests
def x_test_add_child_to_parent__mutmut_8():
    parent = Frame("parent")  
    child = Frame ("CHILD")  
    
    parent.add_child(child)  
    
    assert child in parent.children
    

# Frame Tests
def x_test_add_child_to_parent__mutmut_9():
    parent = Frame("parent")  
    child = Frame ("child")  
    
    parent.add_child(None)  
    
    assert child in parent.children
    

# Frame Tests
def x_test_add_child_to_parent__mutmut_10():
    parent = Frame("parent")  
    child = Frame ("child")  
    
    parent.add_child(child)  
    
    assert child not in parent.children
    

x_test_add_child_to_parent__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_add_child_to_parent__mutmut_1': x_test_add_child_to_parent__mutmut_1, 
    'x_test_add_child_to_parent__mutmut_2': x_test_add_child_to_parent__mutmut_2, 
    'x_test_add_child_to_parent__mutmut_3': x_test_add_child_to_parent__mutmut_3, 
    'x_test_add_child_to_parent__mutmut_4': x_test_add_child_to_parent__mutmut_4, 
    'x_test_add_child_to_parent__mutmut_5': x_test_add_child_to_parent__mutmut_5, 
    'x_test_add_child_to_parent__mutmut_6': x_test_add_child_to_parent__mutmut_6, 
    'x_test_add_child_to_parent__mutmut_7': x_test_add_child_to_parent__mutmut_7, 
    'x_test_add_child_to_parent__mutmut_8': x_test_add_child_to_parent__mutmut_8, 
    'x_test_add_child_to_parent__mutmut_9': x_test_add_child_to_parent__mutmut_9, 
    'x_test_add_child_to_parent__mutmut_10': x_test_add_child_to_parent__mutmut_10
}

def test_add_child_to_parent(*args, **kwargs):
    result = _mutmut_trampoline(x_test_add_child_to_parent__mutmut_orig, x_test_add_child_to_parent__mutmut_mutants, args, kwargs)
    return result 

test_add_child_to_parent.__signature__ = _mutmut_signature(x_test_add_child_to_parent__mutmut_orig)
x_test_add_child_to_parent__mutmut_orig.__name__ = 'x_test_add_child_to_parent'
def x_test_parents_lenght__mutmut_orig():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert len(parent.children) == 1
def x_test_parents_lenght__mutmut_1():
    parent = None  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert len(parent.children) == 1
def x_test_parents_lenght__mutmut_2():
    parent = Frame(None)  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert len(parent.children) == 1
def x_test_parents_lenght__mutmut_3():
    parent = Frame("XXparentXX")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert len(parent.children) == 1
def x_test_parents_lenght__mutmut_4():
    parent = Frame("PARENT")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert len(parent.children) == 1
def x_test_parents_lenght__mutmut_5():
    parent = Frame("parent")  
    child = None
    
    parent.add_child(child)  
    
    assert len(parent.children) == 1
def x_test_parents_lenght__mutmut_6():
    parent = Frame("parent")  
    child = Frame (None)
    
    parent.add_child(child)  
    
    assert len(parent.children) == 1
def x_test_parents_lenght__mutmut_7():
    parent = Frame("parent")  
    child = Frame ("XXchildXX")
    
    parent.add_child(child)  
    
    assert len(parent.children) == 1
def x_test_parents_lenght__mutmut_8():
    parent = Frame("parent")  
    child = Frame ("CHILD")
    
    parent.add_child(child)  
    
    assert len(parent.children) == 1
def x_test_parents_lenght__mutmut_9():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(None)  
    
    assert len(parent.children) == 1
def x_test_parents_lenght__mutmut_10():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert len(parent.children) != 1
def x_test_parents_lenght__mutmut_11():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert len(parent.children) == 2

x_test_parents_lenght__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_parents_lenght__mutmut_1': x_test_parents_lenght__mutmut_1, 
    'x_test_parents_lenght__mutmut_2': x_test_parents_lenght__mutmut_2, 
    'x_test_parents_lenght__mutmut_3': x_test_parents_lenght__mutmut_3, 
    'x_test_parents_lenght__mutmut_4': x_test_parents_lenght__mutmut_4, 
    'x_test_parents_lenght__mutmut_5': x_test_parents_lenght__mutmut_5, 
    'x_test_parents_lenght__mutmut_6': x_test_parents_lenght__mutmut_6, 
    'x_test_parents_lenght__mutmut_7': x_test_parents_lenght__mutmut_7, 
    'x_test_parents_lenght__mutmut_8': x_test_parents_lenght__mutmut_8, 
    'x_test_parents_lenght__mutmut_9': x_test_parents_lenght__mutmut_9, 
    'x_test_parents_lenght__mutmut_10': x_test_parents_lenght__mutmut_10, 
    'x_test_parents_lenght__mutmut_11': x_test_parents_lenght__mutmut_11
}

def test_parents_lenght(*args, **kwargs):
    result = _mutmut_trampoline(x_test_parents_lenght__mutmut_orig, x_test_parents_lenght__mutmut_mutants, args, kwargs)
    return result 

test_parents_lenght.__signature__ = _mutmut_signature(x_test_parents_lenght__mutmut_orig)
x_test_parents_lenght__mutmut_orig.__name__ = 'x_test_parents_lenght'

def x_test_child_reference__mutmut_orig():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert hasattr(child, "parent")

def x_test_child_reference__mutmut_1():
    parent = None  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert hasattr(child, "parent")

def x_test_child_reference__mutmut_2():
    parent = Frame(None)  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert hasattr(child, "parent")

def x_test_child_reference__mutmut_3():
    parent = Frame("XXparentXX")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert hasattr(child, "parent")

def x_test_child_reference__mutmut_4():
    parent = Frame("PARENT")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert hasattr(child, "parent")

def x_test_child_reference__mutmut_5():
    parent = Frame("parent")  
    child = None
    
    parent.add_child(child)  
    
    assert hasattr(child, "parent")

def x_test_child_reference__mutmut_6():
    parent = Frame("parent")  
    child = Frame (None)
    
    parent.add_child(child)  
    
    assert hasattr(child, "parent")

def x_test_child_reference__mutmut_7():
    parent = Frame("parent")  
    child = Frame ("XXchildXX")
    
    parent.add_child(child)  
    
    assert hasattr(child, "parent")

def x_test_child_reference__mutmut_8():
    parent = Frame("parent")  
    child = Frame ("CHILD")
    
    parent.add_child(child)  
    
    assert hasattr(child, "parent")

def x_test_child_reference__mutmut_9():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(None)  
    
    assert hasattr(child, "parent")

def x_test_child_reference__mutmut_10():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert hasattr(None, "parent")

def x_test_child_reference__mutmut_11():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert hasattr(child, None)

def x_test_child_reference__mutmut_12():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert hasattr("parent")

def x_test_child_reference__mutmut_13():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert hasattr(child, )

def x_test_child_reference__mutmut_14():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert hasattr(child, "XXparentXX")

def x_test_child_reference__mutmut_15():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert hasattr(child, "PARENT")

x_test_child_reference__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_child_reference__mutmut_1': x_test_child_reference__mutmut_1, 
    'x_test_child_reference__mutmut_2': x_test_child_reference__mutmut_2, 
    'x_test_child_reference__mutmut_3': x_test_child_reference__mutmut_3, 
    'x_test_child_reference__mutmut_4': x_test_child_reference__mutmut_4, 
    'x_test_child_reference__mutmut_5': x_test_child_reference__mutmut_5, 
    'x_test_child_reference__mutmut_6': x_test_child_reference__mutmut_6, 
    'x_test_child_reference__mutmut_7': x_test_child_reference__mutmut_7, 
    'x_test_child_reference__mutmut_8': x_test_child_reference__mutmut_8, 
    'x_test_child_reference__mutmut_9': x_test_child_reference__mutmut_9, 
    'x_test_child_reference__mutmut_10': x_test_child_reference__mutmut_10, 
    'x_test_child_reference__mutmut_11': x_test_child_reference__mutmut_11, 
    'x_test_child_reference__mutmut_12': x_test_child_reference__mutmut_12, 
    'x_test_child_reference__mutmut_13': x_test_child_reference__mutmut_13, 
    'x_test_child_reference__mutmut_14': x_test_child_reference__mutmut_14, 
    'x_test_child_reference__mutmut_15': x_test_child_reference__mutmut_15
}

def test_child_reference(*args, **kwargs):
    result = _mutmut_trampoline(x_test_child_reference__mutmut_orig, x_test_child_reference__mutmut_mutants, args, kwargs)
    return result 

test_child_reference.__signature__ = _mutmut_signature(x_test_child_reference__mutmut_orig)
x_test_child_reference__mutmut_orig.__name__ = 'x_test_child_reference'

def x_test_child_parent_reference__mutmut_orig():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert child.parent is parent
    

def x_test_child_parent_reference__mutmut_1():
    parent = None  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert child.parent is parent
    

def x_test_child_parent_reference__mutmut_2():
    parent = Frame(None)  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert child.parent is parent
    

def x_test_child_parent_reference__mutmut_3():
    parent = Frame("XXparentXX")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert child.parent is parent
    

def x_test_child_parent_reference__mutmut_4():
    parent = Frame("PARENT")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert child.parent is parent
    

def x_test_child_parent_reference__mutmut_5():
    parent = Frame("parent")  
    child = None
    
    parent.add_child(child)  
    
    assert child.parent is parent
    

def x_test_child_parent_reference__mutmut_6():
    parent = Frame("parent")  
    child = Frame (None)
    
    parent.add_child(child)  
    
    assert child.parent is parent
    

def x_test_child_parent_reference__mutmut_7():
    parent = Frame("parent")  
    child = Frame ("XXchildXX")
    
    parent.add_child(child)  
    
    assert child.parent is parent
    

def x_test_child_parent_reference__mutmut_8():
    parent = Frame("parent")  
    child = Frame ("CHILD")
    
    parent.add_child(child)  
    
    assert child.parent is parent
    

def x_test_child_parent_reference__mutmut_9():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(None)  
    
    assert child.parent is parent
    

def x_test_child_parent_reference__mutmut_10():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert child.parent is not parent
    

x_test_child_parent_reference__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_child_parent_reference__mutmut_1': x_test_child_parent_reference__mutmut_1, 
    'x_test_child_parent_reference__mutmut_2': x_test_child_parent_reference__mutmut_2, 
    'x_test_child_parent_reference__mutmut_3': x_test_child_parent_reference__mutmut_3, 
    'x_test_child_parent_reference__mutmut_4': x_test_child_parent_reference__mutmut_4, 
    'x_test_child_parent_reference__mutmut_5': x_test_child_parent_reference__mutmut_5, 
    'x_test_child_parent_reference__mutmut_6': x_test_child_parent_reference__mutmut_6, 
    'x_test_child_parent_reference__mutmut_7': x_test_child_parent_reference__mutmut_7, 
    'x_test_child_parent_reference__mutmut_8': x_test_child_parent_reference__mutmut_8, 
    'x_test_child_parent_reference__mutmut_9': x_test_child_parent_reference__mutmut_9, 
    'x_test_child_parent_reference__mutmut_10': x_test_child_parent_reference__mutmut_10
}

def test_child_parent_reference(*args, **kwargs):
    result = _mutmut_trampoline(x_test_child_parent_reference__mutmut_orig, x_test_child_parent_reference__mutmut_mutants, args, kwargs)
    return result 

test_child_parent_reference.__signature__ = _mutmut_signature(x_test_child_parent_reference__mutmut_orig)
x_test_child_parent_reference__mutmut_orig.__name__ = 'x_test_child_parent_reference'
def x_test_add_multi_child_to_parent__mutmut_orig():
    parent = Frame("parent")  
    child = Frame("child")
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_1():
    parent = None  
    child = Frame("child")
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_2():
    parent = Frame(None)  
    child = Frame("child")
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_3():
    parent = Frame("XXparentXX")  
    child = Frame("child")
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_4():
    parent = Frame("PARENT")  
    child = Frame("child")
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_5():
    parent = Frame("parent")  
    child = None
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_6():
    parent = Frame("parent")  
    child = Frame(None)
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_7():
    parent = Frame("parent")  
    child = Frame("XXchildXX")
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_8():
    parent = Frame("parent")  
    child = Frame("CHILD")
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_9():
    parent = Frame("parent")  
    child = Frame("child")
    child2 = None
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_10():
    parent = Frame("parent")  
    child = Frame("child")
    child2 = Frame(None)
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_11():
    parent = Frame("parent")  
    child = Frame("child")
    child2 = Frame("XXchild2XX")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_12():
    parent = Frame("parent")  
    child = Frame("child")
    child2 = Frame("CHILD2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_13():
    parent = Frame("parent")  
    child = Frame("child")
    child2 = Frame("child2")
    
    parent.add_child(None)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_14():
    parent = Frame("parent")  
    child = Frame("child")
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(None)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_15():
    parent = Frame("parent")  
    child = Frame("child")
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) != 2
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_16():
    parent = Frame("parent")  
    child = Frame("child")
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 3
    assert parent.children[0] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_17():
    parent = Frame("parent")  
    child = Frame("child")
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[1] == child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_18():
    parent = Frame("parent")  
    child = Frame("child")
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] != child
    assert parent.children[1] == child2
def x_test_add_multi_child_to_parent__mutmut_19():
    parent = Frame("parent")  
    child = Frame("child")
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[2] == child2
def x_test_add_multi_child_to_parent__mutmut_20():
    parent = Frame("parent")  
    child = Frame("child")
    child2 = Frame("child2")
    
    parent.add_child(child)
    parent.add_child(child2)
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] != child2

x_test_add_multi_child_to_parent__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_add_multi_child_to_parent__mutmut_1': x_test_add_multi_child_to_parent__mutmut_1, 
    'x_test_add_multi_child_to_parent__mutmut_2': x_test_add_multi_child_to_parent__mutmut_2, 
    'x_test_add_multi_child_to_parent__mutmut_3': x_test_add_multi_child_to_parent__mutmut_3, 
    'x_test_add_multi_child_to_parent__mutmut_4': x_test_add_multi_child_to_parent__mutmut_4, 
    'x_test_add_multi_child_to_parent__mutmut_5': x_test_add_multi_child_to_parent__mutmut_5, 
    'x_test_add_multi_child_to_parent__mutmut_6': x_test_add_multi_child_to_parent__mutmut_6, 
    'x_test_add_multi_child_to_parent__mutmut_7': x_test_add_multi_child_to_parent__mutmut_7, 
    'x_test_add_multi_child_to_parent__mutmut_8': x_test_add_multi_child_to_parent__mutmut_8, 
    'x_test_add_multi_child_to_parent__mutmut_9': x_test_add_multi_child_to_parent__mutmut_9, 
    'x_test_add_multi_child_to_parent__mutmut_10': x_test_add_multi_child_to_parent__mutmut_10, 
    'x_test_add_multi_child_to_parent__mutmut_11': x_test_add_multi_child_to_parent__mutmut_11, 
    'x_test_add_multi_child_to_parent__mutmut_12': x_test_add_multi_child_to_parent__mutmut_12, 
    'x_test_add_multi_child_to_parent__mutmut_13': x_test_add_multi_child_to_parent__mutmut_13, 
    'x_test_add_multi_child_to_parent__mutmut_14': x_test_add_multi_child_to_parent__mutmut_14, 
    'x_test_add_multi_child_to_parent__mutmut_15': x_test_add_multi_child_to_parent__mutmut_15, 
    'x_test_add_multi_child_to_parent__mutmut_16': x_test_add_multi_child_to_parent__mutmut_16, 
    'x_test_add_multi_child_to_parent__mutmut_17': x_test_add_multi_child_to_parent__mutmut_17, 
    'x_test_add_multi_child_to_parent__mutmut_18': x_test_add_multi_child_to_parent__mutmut_18, 
    'x_test_add_multi_child_to_parent__mutmut_19': x_test_add_multi_child_to_parent__mutmut_19, 
    'x_test_add_multi_child_to_parent__mutmut_20': x_test_add_multi_child_to_parent__mutmut_20
}

def test_add_multi_child_to_parent(*args, **kwargs):
    result = _mutmut_trampoline(x_test_add_multi_child_to_parent__mutmut_orig, x_test_add_multi_child_to_parent__mutmut_mutants, args, kwargs)
    return result 

test_add_multi_child_to_parent.__signature__ = _mutmut_signature(x_test_add_multi_child_to_parent__mutmut_orig)
x_test_add_multi_child_to_parent__mutmut_orig.__name__ = 'x_test_add_multi_child_to_parent'