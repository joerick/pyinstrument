from pyinstrument import Profiler
from pyinstrument.renderers import HTMLRenderer
import time
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

def x_sleepyRender_html__mutmut_orig():
    profiler = Profiler()
    profiler.start()
    time.sleep(1.5)
    profiler.stop()

    renderer = HTMLRenderer()
    html_output = profiler.output(renderer=renderer)
    save_html_report(html_output)

def x_sleepyRender_html__mutmut_1():
    profiler = None
    profiler.start()
    time.sleep(1.5)
    profiler.stop()

    renderer = HTMLRenderer()
    html_output = profiler.output(renderer=renderer)
    save_html_report(html_output)

def x_sleepyRender_html__mutmut_2():
    profiler = Profiler()
    profiler.start()
    time.sleep(None)
    profiler.stop()

    renderer = HTMLRenderer()
    html_output = profiler.output(renderer=renderer)
    save_html_report(html_output)

def x_sleepyRender_html__mutmut_3():
    profiler = Profiler()
    profiler.start()
    time.sleep(2.5)
    profiler.stop()

    renderer = HTMLRenderer()
    html_output = profiler.output(renderer=renderer)
    save_html_report(html_output)

def x_sleepyRender_html__mutmut_4():
    profiler = Profiler()
    profiler.start()
    time.sleep(1.5)
    profiler.stop()

    renderer = None
    html_output = profiler.output(renderer=renderer)
    save_html_report(html_output)

def x_sleepyRender_html__mutmut_5():
    profiler = Profiler()
    profiler.start()
    time.sleep(1.5)
    profiler.stop()

    renderer = HTMLRenderer()
    html_output = None
    save_html_report(html_output)

def x_sleepyRender_html__mutmut_6():
    profiler = Profiler()
    profiler.start()
    time.sleep(1.5)
    profiler.stop()

    renderer = HTMLRenderer()
    html_output = profiler.output(renderer=None)
    save_html_report(html_output)

def x_sleepyRender_html__mutmut_7():
    profiler = Profiler()
    profiler.start()
    time.sleep(1.5)
    profiler.stop()

    renderer = HTMLRenderer()
    html_output = profiler.output(renderer=renderer)
    save_html_report(None)

x_sleepyRender_html__mutmut_mutants : ClassVar[MutantDict] = {
'x_sleepyRender_html__mutmut_1': x_sleepyRender_html__mutmut_1, 
    'x_sleepyRender_html__mutmut_2': x_sleepyRender_html__mutmut_2, 
    'x_sleepyRender_html__mutmut_3': x_sleepyRender_html__mutmut_3, 
    'x_sleepyRender_html__mutmut_4': x_sleepyRender_html__mutmut_4, 
    'x_sleepyRender_html__mutmut_5': x_sleepyRender_html__mutmut_5, 
    'x_sleepyRender_html__mutmut_6': x_sleepyRender_html__mutmut_6, 
    'x_sleepyRender_html__mutmut_7': x_sleepyRender_html__mutmut_7
}

def sleepyRender_html(*args, **kwargs):
    result = _mutmut_trampoline(x_sleepyRender_html__mutmut_orig, x_sleepyRender_html__mutmut_mutants, args, kwargs)
    return result 

sleepyRender_html.__signature__ = _mutmut_signature(x_sleepyRender_html__mutmut_orig)
x_sleepyRender_html__mutmut_orig.__name__ = 'x_sleepyRender_html'

def save_html_report(html_content):
    # This could save to disk or a DB
    pass
