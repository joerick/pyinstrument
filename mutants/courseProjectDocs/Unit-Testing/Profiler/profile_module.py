from pyinstrument import Profiler
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

def save_profile_to_db(profile):
    # This is where we would save the profile data to the database
    pass

def x_run_and_save_profile__mutmut_orig():
    profiler = Profiler()
    profiler.start()
    total = sum(range(1000))
    profiler.stop()
    save_profile_to_db(profiler.output_text())

def x_run_and_save_profile__mutmut_1():
    profiler = None
    profiler.start()
    total = sum(range(1000))
    profiler.stop()
    save_profile_to_db(profiler.output_text())

def x_run_and_save_profile__mutmut_2():
    profiler = Profiler()
    profiler.start()
    total = None
    profiler.stop()
    save_profile_to_db(profiler.output_text())

def x_run_and_save_profile__mutmut_3():
    profiler = Profiler()
    profiler.start()
    total = sum(None)
    profiler.stop()
    save_profile_to_db(profiler.output_text())

def x_run_and_save_profile__mutmut_4():
    profiler = Profiler()
    profiler.start()
    total = sum(range(None))
    profiler.stop()
    save_profile_to_db(profiler.output_text())

def x_run_and_save_profile__mutmut_5():
    profiler = Profiler()
    profiler.start()
    total = sum(range(1001))
    profiler.stop()
    save_profile_to_db(profiler.output_text())

def x_run_and_save_profile__mutmut_6():
    profiler = Profiler()
    profiler.start()
    total = sum(range(1000))
    profiler.stop()
    save_profile_to_db(None)

x_run_and_save_profile__mutmut_mutants : ClassVar[MutantDict] = {
'x_run_and_save_profile__mutmut_1': x_run_and_save_profile__mutmut_1, 
    'x_run_and_save_profile__mutmut_2': x_run_and_save_profile__mutmut_2, 
    'x_run_and_save_profile__mutmut_3': x_run_and_save_profile__mutmut_3, 
    'x_run_and_save_profile__mutmut_4': x_run_and_save_profile__mutmut_4, 
    'x_run_and_save_profile__mutmut_5': x_run_and_save_profile__mutmut_5, 
    'x_run_and_save_profile__mutmut_6': x_run_and_save_profile__mutmut_6
}

def run_and_save_profile(*args, **kwargs):
    result = _mutmut_trampoline(x_run_and_save_profile__mutmut_orig, x_run_and_save_profile__mutmut_mutants, args, kwargs)
    return result 

run_and_save_profile.__signature__ = _mutmut_signature(x_run_and_save_profile__mutmut_orig)
x_run_and_save_profile__mutmut_orig.__name__ = 'x_run_and_save_profile'


def x_run_heavy_task__mutmut_orig():
    total = 0
    for i in range(10_000):
        total += i ** 2
    return total


def x_run_heavy_task__mutmut_1():
    total = None
    for i in range(10_000):
        total += i ** 2
    return total


def x_run_heavy_task__mutmut_2():
    total = 1
    for i in range(10_000):
        total += i ** 2
    return total


def x_run_heavy_task__mutmut_3():
    total = 0
    for i in range(None):
        total += i ** 2
    return total


def x_run_heavy_task__mutmut_4():
    total = 0
    for i in range(10001):
        total += i ** 2
    return total


def x_run_heavy_task__mutmut_5():
    total = 0
    for i in range(10_000):
        total = i ** 2
    return total


def x_run_heavy_task__mutmut_6():
    total = 0
    for i in range(10_000):
        total -= i ** 2
    return total


def x_run_heavy_task__mutmut_7():
    total = 0
    for i in range(10_000):
        total += i * 2
    return total


def x_run_heavy_task__mutmut_8():
    total = 0
    for i in range(10_000):
        total += i ** 3
    return total

x_run_heavy_task__mutmut_mutants : ClassVar[MutantDict] = {
'x_run_heavy_task__mutmut_1': x_run_heavy_task__mutmut_1, 
    'x_run_heavy_task__mutmut_2': x_run_heavy_task__mutmut_2, 
    'x_run_heavy_task__mutmut_3': x_run_heavy_task__mutmut_3, 
    'x_run_heavy_task__mutmut_4': x_run_heavy_task__mutmut_4, 
    'x_run_heavy_task__mutmut_5': x_run_heavy_task__mutmut_5, 
    'x_run_heavy_task__mutmut_6': x_run_heavy_task__mutmut_6, 
    'x_run_heavy_task__mutmut_7': x_run_heavy_task__mutmut_7, 
    'x_run_heavy_task__mutmut_8': x_run_heavy_task__mutmut_8
}

def run_heavy_task(*args, **kwargs):
    result = _mutmut_trampoline(x_run_heavy_task__mutmut_orig, x_run_heavy_task__mutmut_mutants, args, kwargs)
    return result 

run_heavy_task.__signature__ = _mutmut_signature(x_run_heavy_task__mutmut_orig)
x_run_heavy_task__mutmut_orig.__name__ = 'x_run_heavy_task'

def x_run_profiler_and_report__mutmut_orig():
    profiler = Profiler()
    profiler.start()
    run_heavy_task()
    profiler.stop()

    report = profiler.output_text(unicode=True, color=False)
    print(report)
    return report

def x_run_profiler_and_report__mutmut_1():
    profiler = None
    profiler.start()
    run_heavy_task()
    profiler.stop()

    report = profiler.output_text(unicode=True, color=False)
    print(report)
    return report

def x_run_profiler_and_report__mutmut_2():
    profiler = Profiler()
    profiler.start()
    run_heavy_task()
    profiler.stop()

    report = None
    print(report)
    return report

def x_run_profiler_and_report__mutmut_3():
    profiler = Profiler()
    profiler.start()
    run_heavy_task()
    profiler.stop()

    report = profiler.output_text(unicode=None, color=False)
    print(report)
    return report

def x_run_profiler_and_report__mutmut_4():
    profiler = Profiler()
    profiler.start()
    run_heavy_task()
    profiler.stop()

    report = profiler.output_text(unicode=True, color=None)
    print(report)
    return report

def x_run_profiler_and_report__mutmut_5():
    profiler = Profiler()
    profiler.start()
    run_heavy_task()
    profiler.stop()

    report = profiler.output_text(color=False)
    print(report)
    return report

def x_run_profiler_and_report__mutmut_6():
    profiler = Profiler()
    profiler.start()
    run_heavy_task()
    profiler.stop()

    report = profiler.output_text(unicode=True, )
    print(report)
    return report

def x_run_profiler_and_report__mutmut_7():
    profiler = Profiler()
    profiler.start()
    run_heavy_task()
    profiler.stop()

    report = profiler.output_text(unicode=False, color=False)
    print(report)
    return report

def x_run_profiler_and_report__mutmut_8():
    profiler = Profiler()
    profiler.start()
    run_heavy_task()
    profiler.stop()

    report = profiler.output_text(unicode=True, color=True)
    print(report)
    return report

def x_run_profiler_and_report__mutmut_9():
    profiler = Profiler()
    profiler.start()
    run_heavy_task()
    profiler.stop()

    report = profiler.output_text(unicode=True, color=False)
    print(None)
    return report

x_run_profiler_and_report__mutmut_mutants : ClassVar[MutantDict] = {
'x_run_profiler_and_report__mutmut_1': x_run_profiler_and_report__mutmut_1, 
    'x_run_profiler_and_report__mutmut_2': x_run_profiler_and_report__mutmut_2, 
    'x_run_profiler_and_report__mutmut_3': x_run_profiler_and_report__mutmut_3, 
    'x_run_profiler_and_report__mutmut_4': x_run_profiler_and_report__mutmut_4, 
    'x_run_profiler_and_report__mutmut_5': x_run_profiler_and_report__mutmut_5, 
    'x_run_profiler_and_report__mutmut_6': x_run_profiler_and_report__mutmut_6, 
    'x_run_profiler_and_report__mutmut_7': x_run_profiler_and_report__mutmut_7, 
    'x_run_profiler_and_report__mutmut_8': x_run_profiler_and_report__mutmut_8, 
    'x_run_profiler_and_report__mutmut_9': x_run_profiler_and_report__mutmut_9
}

def run_profiler_and_report(*args, **kwargs):
    result = _mutmut_trampoline(x_run_profiler_and_report__mutmut_orig, x_run_profiler_and_report__mutmut_mutants, args, kwargs)
    return result 

run_profiler_and_report.__signature__ = _mutmut_signature(x_run_profiler_and_report__mutmut_orig)
x_run_profiler_and_report__mutmut_orig.__name__ = 'x_run_profiler_and_report'