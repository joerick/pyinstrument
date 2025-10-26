from unittest.mock import patch
import renderer_module
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

def x_test_save_html_called_once__mutmut_orig():
    with patch('renderer_module.save_html_report') as mock_save:
        renderer_module.sleepyRender_html()
        assert mock_save.call_count == 1

def x_test_save_html_called_once__mutmut_1():
    with patch(None) as mock_save:
        renderer_module.sleepyRender_html()
        assert mock_save.call_count == 1

def x_test_save_html_called_once__mutmut_2():
    with patch('XXrenderer_module.save_html_reportXX') as mock_save:
        renderer_module.sleepyRender_html()
        assert mock_save.call_count == 1

def x_test_save_html_called_once__mutmut_3():
    with patch('RENDERER_MODULE.SAVE_HTML_REPORT') as mock_save:
        renderer_module.sleepyRender_html()
        assert mock_save.call_count == 1

def x_test_save_html_called_once__mutmut_4():
    with patch('renderer_module.save_html_report') as mock_save:
        renderer_module.sleepyRender_html()
        assert mock_save.call_count != 1

def x_test_save_html_called_once__mutmut_5():
    with patch('renderer_module.save_html_report') as mock_save:
        renderer_module.sleepyRender_html()
        assert mock_save.call_count == 2

x_test_save_html_called_once__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_save_html_called_once__mutmut_1': x_test_save_html_called_once__mutmut_1, 
    'x_test_save_html_called_once__mutmut_2': x_test_save_html_called_once__mutmut_2, 
    'x_test_save_html_called_once__mutmut_3': x_test_save_html_called_once__mutmut_3, 
    'x_test_save_html_called_once__mutmut_4': x_test_save_html_called_once__mutmut_4, 
    'x_test_save_html_called_once__mutmut_5': x_test_save_html_called_once__mutmut_5
}

def test_save_html_called_once(*args, **kwargs):
    result = _mutmut_trampoline(x_test_save_html_called_once__mutmut_orig, x_test_save_html_called_once__mutmut_mutants, args, kwargs)
    return result 

test_save_html_called_once.__signature__ = _mutmut_signature(x_test_save_html_called_once__mutmut_orig)
x_test_save_html_called_once__mutmut_orig.__name__ = 'x_test_save_html_called_once'

def x_test_saved_content_is_html__mutmut_orig():
    with patch('renderer_module.save_html_report') as mock_save:
        renderer_module.sleepyRender_html()
        args, _ = mock_save.call_args
        html_output = args[0]
        assert "<html" in html_output.lower()

def x_test_saved_content_is_html__mutmut_1():
    with patch(None) as mock_save:
        renderer_module.sleepyRender_html()
        args, _ = mock_save.call_args
        html_output = args[0]
        assert "<html" in html_output.lower()

def x_test_saved_content_is_html__mutmut_2():
    with patch('XXrenderer_module.save_html_reportXX') as mock_save:
        renderer_module.sleepyRender_html()
        args, _ = mock_save.call_args
        html_output = args[0]
        assert "<html" in html_output.lower()

def x_test_saved_content_is_html__mutmut_3():
    with patch('RENDERER_MODULE.SAVE_HTML_REPORT') as mock_save:
        renderer_module.sleepyRender_html()
        args, _ = mock_save.call_args
        html_output = args[0]
        assert "<html" in html_output.lower()

def x_test_saved_content_is_html__mutmut_4():
    with patch('renderer_module.save_html_report') as mock_save:
        renderer_module.sleepyRender_html()
        args, _ = None
        html_output = args[0]
        assert "<html" in html_output.lower()

def x_test_saved_content_is_html__mutmut_5():
    with patch('renderer_module.save_html_report') as mock_save:
        renderer_module.sleepyRender_html()
        args, _ = mock_save.call_args
        html_output = None
        assert "<html" in html_output.lower()

def x_test_saved_content_is_html__mutmut_6():
    with patch('renderer_module.save_html_report') as mock_save:
        renderer_module.sleepyRender_html()
        args, _ = mock_save.call_args
        html_output = args[1]
        assert "<html" in html_output.lower()

def x_test_saved_content_is_html__mutmut_7():
    with patch('renderer_module.save_html_report') as mock_save:
        renderer_module.sleepyRender_html()
        args, _ = mock_save.call_args
        html_output = args[0]
        assert "XX<htmlXX" in html_output.lower()

def x_test_saved_content_is_html__mutmut_8():
    with patch('renderer_module.save_html_report') as mock_save:
        renderer_module.sleepyRender_html()
        args, _ = mock_save.call_args
        html_output = args[0]
        assert "<HTML" in html_output.lower()

def x_test_saved_content_is_html__mutmut_9():
    with patch('renderer_module.save_html_report') as mock_save:
        renderer_module.sleepyRender_html()
        args, _ = mock_save.call_args
        html_output = args[0]
        assert "<html" not in html_output.lower()

def x_test_saved_content_is_html__mutmut_10():
    with patch('renderer_module.save_html_report') as mock_save:
        renderer_module.sleepyRender_html()
        args, _ = mock_save.call_args
        html_output = args[0]
        assert "<html" in html_output.upper()

x_test_saved_content_is_html__mutmut_mutants : ClassVar[MutantDict] = {
'x_test_saved_content_is_html__mutmut_1': x_test_saved_content_is_html__mutmut_1, 
    'x_test_saved_content_is_html__mutmut_2': x_test_saved_content_is_html__mutmut_2, 
    'x_test_saved_content_is_html__mutmut_3': x_test_saved_content_is_html__mutmut_3, 
    'x_test_saved_content_is_html__mutmut_4': x_test_saved_content_is_html__mutmut_4, 
    'x_test_saved_content_is_html__mutmut_5': x_test_saved_content_is_html__mutmut_5, 
    'x_test_saved_content_is_html__mutmut_6': x_test_saved_content_is_html__mutmut_6, 
    'x_test_saved_content_is_html__mutmut_7': x_test_saved_content_is_html__mutmut_7, 
    'x_test_saved_content_is_html__mutmut_8': x_test_saved_content_is_html__mutmut_8, 
    'x_test_saved_content_is_html__mutmut_9': x_test_saved_content_is_html__mutmut_9, 
    'x_test_saved_content_is_html__mutmut_10': x_test_saved_content_is_html__mutmut_10
}

def test_saved_content_is_html(*args, **kwargs):
    result = _mutmut_trampoline(x_test_saved_content_is_html__mutmut_orig, x_test_saved_content_is_html__mutmut_mutants, args, kwargs)
    return result 

test_saved_content_is_html.__signature__ = _mutmut_signature(x_test_saved_content_is_html__mutmut_orig)
x_test_saved_content_is_html__mutmut_orig.__name__ = 'x_test_saved_content_is_html'
