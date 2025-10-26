from unittest.mock import patch, MagicMock
import profile_module
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

def x_test_save_profile_called_once__mutmut_orig():
    with patch("profile_module.save_profile_to_db") as mock_save:
        profile_module.run_and_save_profile()
        assert mock_save.call_count == 1

def x_test_save_profile_called_once__mutmut_1():
    with patch(None) as mock_save:
        profile_module.run_and_save_profile()
        assert mock_save.call_count == 1

def x_test_save_profile_called_once__mutmut_2():
    with patch("XXprofile_module.save_profile_to_dbXX") as mock_save:
        profile_module.run_and_save_profile()
        assert mock_save.call_count == 1

def x_test_save_profile_called_once__mutmut_3():
    with patch("PROFILE_MODULE.SAVE_PROFILE_TO_DB") as mock_save:
        profile_module.run_and_save_profile()
        assert mock_save.call_count == 1

def x_test_save_profile_called_once__mutmut_4():
    with patch("profile_module.save_profile_to_db") as mock_save:
        profile_module.run_and_save_profile()
        assert mock_save.call_count != 1

def x_test_save_profile_called_once__mutmut_5():
    with patch("profile_module.save_profile_to_db") as mock_save:
        profile_module.run_and_save_profile()
        assert mock_save.call_count == 2

x_test_save_profile_called_once__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_save_profile_called_once__mutmut_1': x_test_save_profile_called_once__mutmut_1, 
    'x_test_save_profile_called_once__mutmut_2': x_test_save_profile_called_once__mutmut_2, 
    'x_test_save_profile_called_once__mutmut_3': x_test_save_profile_called_once__mutmut_3, 
    'x_test_save_profile_called_once__mutmut_4': x_test_save_profile_called_once__mutmut_4, 
    'x_test_save_profile_called_once__mutmut_5': x_test_save_profile_called_once__mutmut_5
}

def test_save_profile_called_once(*args, **kwargs):
    result = _mutmut_trampoline(x_test_save_profile_called_once__mutmut_orig, x_test_save_profile_called_once__mutmut_mutants, args, kwargs)
    return result 

test_save_profile_called_once.__signature__ = _mutmut_signature(x_test_save_profile_called_once__mutmut_orig)
x_test_save_profile_called_once__mutmut_orig.__name__ = 'x_test_save_profile_called_once'

def x_test_save_profile_called_with_string__mutmut_orig():
    with patch("profile_module.save_profile_to_db") as mock_save:
        profile_module.run_and_save_profile()
        args, _ = mock_save.call_args
        assert isinstance(args[0], str)

def x_test_save_profile_called_with_string__mutmut_1():
    with patch(None) as mock_save:
        profile_module.run_and_save_profile()
        args, _ = mock_save.call_args
        assert isinstance(args[0], str)

def x_test_save_profile_called_with_string__mutmut_2():
    with patch("XXprofile_module.save_profile_to_dbXX") as mock_save:
        profile_module.run_and_save_profile()
        args, _ = mock_save.call_args
        assert isinstance(args[0], str)

def x_test_save_profile_called_with_string__mutmut_3():
    with patch("PROFILE_MODULE.SAVE_PROFILE_TO_DB") as mock_save:
        profile_module.run_and_save_profile()
        args, _ = mock_save.call_args
        assert isinstance(args[0], str)

def x_test_save_profile_called_with_string__mutmut_4():
    with patch("profile_module.save_profile_to_db") as mock_save:
        profile_module.run_and_save_profile()
        args, _ = None
        assert isinstance(args[0], str)

x_test_save_profile_called_with_string__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_save_profile_called_with_string__mutmut_1': x_test_save_profile_called_with_string__mutmut_1, 
    'x_test_save_profile_called_with_string__mutmut_2': x_test_save_profile_called_with_string__mutmut_2, 
    'x_test_save_profile_called_with_string__mutmut_3': x_test_save_profile_called_with_string__mutmut_3, 
    'x_test_save_profile_called_with_string__mutmut_4': x_test_save_profile_called_with_string__mutmut_4
}

def test_save_profile_called_with_string(*args, **kwargs):
    result = _mutmut_trampoline(x_test_save_profile_called_with_string__mutmut_orig, x_test_save_profile_called_with_string__mutmut_mutants, args, kwargs)
    return result 

test_save_profile_called_with_string.__signature__ = _mutmut_signature(x_test_save_profile_called_with_string__mutmut_orig)
x_test_save_profile_called_with_string__mutmut_orig.__name__ = 'x_test_save_profile_called_with_string'

def x_test_profiler_methods_called__mutmut_orig():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_1():
    with patch(None) as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_2():
    with patch("XXprofile_module.ProfilerXX") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_3():
    with patch("profile_module.profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_4():
    with patch("PROFILE_MODULE.PROFILER") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_5():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = None
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_6():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = None
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_7():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = None

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_8():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "XXMocked profiling reportXX"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_9():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_10():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "MOCKED PROFILING REPORT"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_11():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = None

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_12():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=None, color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_13():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=None)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_14():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_15():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, )
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_16():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=False, color=False)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_17():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=True)
        assert report == "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_18():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report != "Mocked profiling report"

def x_test_profiler_methods_called__mutmut_19():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "XXMocked profiling reportXX"

def x_test_profiler_methods_called__mutmut_20():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "mocked profiling report"

def x_test_profiler_methods_called__mutmut_21():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "MOCKED PROFILING REPORT"

x_test_profiler_methods_called__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_profiler_methods_called__mutmut_1': x_test_profiler_methods_called__mutmut_1, 
    'x_test_profiler_methods_called__mutmut_2': x_test_profiler_methods_called__mutmut_2, 
    'x_test_profiler_methods_called__mutmut_3': x_test_profiler_methods_called__mutmut_3, 
    'x_test_profiler_methods_called__mutmut_4': x_test_profiler_methods_called__mutmut_4, 
    'x_test_profiler_methods_called__mutmut_5': x_test_profiler_methods_called__mutmut_5, 
    'x_test_profiler_methods_called__mutmut_6': x_test_profiler_methods_called__mutmut_6, 
    'x_test_profiler_methods_called__mutmut_7': x_test_profiler_methods_called__mutmut_7, 
    'x_test_profiler_methods_called__mutmut_8': x_test_profiler_methods_called__mutmut_8, 
    'x_test_profiler_methods_called__mutmut_9': x_test_profiler_methods_called__mutmut_9, 
    'x_test_profiler_methods_called__mutmut_10': x_test_profiler_methods_called__mutmut_10, 
    'x_test_profiler_methods_called__mutmut_11': x_test_profiler_methods_called__mutmut_11, 
    'x_test_profiler_methods_called__mutmut_12': x_test_profiler_methods_called__mutmut_12, 
    'x_test_profiler_methods_called__mutmut_13': x_test_profiler_methods_called__mutmut_13, 
    'x_test_profiler_methods_called__mutmut_14': x_test_profiler_methods_called__mutmut_14, 
    'x_test_profiler_methods_called__mutmut_15': x_test_profiler_methods_called__mutmut_15, 
    'x_test_profiler_methods_called__mutmut_16': x_test_profiler_methods_called__mutmut_16, 
    'x_test_profiler_methods_called__mutmut_17': x_test_profiler_methods_called__mutmut_17, 
    'x_test_profiler_methods_called__mutmut_18': x_test_profiler_methods_called__mutmut_18, 
    'x_test_profiler_methods_called__mutmut_19': x_test_profiler_methods_called__mutmut_19, 
    'x_test_profiler_methods_called__mutmut_20': x_test_profiler_methods_called__mutmut_20, 
    'x_test_profiler_methods_called__mutmut_21': x_test_profiler_methods_called__mutmut_21
}

def test_profiler_methods_called(*args, **kwargs):
    result = _mutmut_trampoline(x_test_profiler_methods_called__mutmut_orig, x_test_profiler_methods_called__mutmut_mutants, args, kwargs)
    return result 

test_profiler_methods_called.__signature__ = _mutmut_signature(x_test_profiler_methods_called__mutmut_orig)
x_test_profiler_methods_called__mutmut_orig.__name__ = 'x_test_profiler_methods_called'

def x_test_run_heavy_task_completes__mutmut_orig():
    result = profile_module.run_heavy_task()
    assert result > 0
    assert isinstance(result, int)

def x_test_run_heavy_task_completes__mutmut_1():
    result = None
    assert result > 0
    assert isinstance(result, int)

def x_test_run_heavy_task_completes__mutmut_2():
    result = profile_module.run_heavy_task()
    assert result >= 0
    assert isinstance(result, int)

def x_test_run_heavy_task_completes__mutmut_3():
    result = profile_module.run_heavy_task()
    assert result > 1
    assert isinstance(result, int)

x_test_run_heavy_task_completes__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_run_heavy_task_completes__mutmut_1': x_test_run_heavy_task_completes__mutmut_1, 
    'x_test_run_heavy_task_completes__mutmut_2': x_test_run_heavy_task_completes__mutmut_2, 
    'x_test_run_heavy_task_completes__mutmut_3': x_test_run_heavy_task_completes__mutmut_3
}

def test_run_heavy_task_completes(*args, **kwargs):
    result = _mutmut_trampoline(x_test_run_heavy_task_completes__mutmut_orig, x_test_run_heavy_task_completes__mutmut_mutants, args, kwargs)
    return result 

test_run_heavy_task_completes.__signature__ = _mutmut_signature(x_test_run_heavy_task_completes__mutmut_orig)
x_test_run_heavy_task_completes__mutmut_orig.__name__ = 'x_test_run_heavy_task_completes'