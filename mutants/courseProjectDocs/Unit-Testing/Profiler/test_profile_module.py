# from unittest.mock import patch, MagicMock
# import profile_module

# def test_save_profile_called_once():
#     with patch("profile_module.save_profile_to_db") as mock_save:
#         profile_module.run_and_save_profile()
#         assert mock_save.call_count == 1

# def test_save_profile_called_with_string():
#     with patch("profile_module.save_profile_to_db") as mock_save:
#         profile_module.run_and_save_profile()
#         args, _ = mock_save.call_args
#         assert isinstance(args[0], str)

# def test_profiler_methods_called():
#     with patch("profile_module.Profiler") as MockProfiler:
#         mock_instance = MagicMock()
#         MockProfiler.return_value = mock_instance
#         mock_instance.output_text.return_value = "Mocked profiling report"

#         report = profile_module.run_profiler_and_report()

#         mock_instance.start.assert_called_once()
#         mock_instance.stop.assert_called_once()
#         mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
#         assert report == "Mocked profiling report"

# def test_run_heavy_task_completes():
#     result = profile_module.run_heavy_task()
#     assert result > 0
#     assert isinstance(result, int)
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