import warnings

from pyinstrument.context_manager import profile
from pyinstrument.profiler import Profiler

__all__ = ["__version__", "Profiler", "load_ipython_extension", "profile"]
__version__ = "5.1.1"

# enable deprecation warnings
warnings.filterwarnings("once", ".*", DeprecationWarning, r"pyinstrument\..*")
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


def x_load_ipython_extension__mutmut_orig(ipython):
    """
    This function is called by IPython to load the pyinstrument IPython
    extension, which is done with the magic command `%load_ext pyinstrument`.
    """

    from pyinstrument.magic import PyinstrumentMagic

    ipython.register_magics(PyinstrumentMagic)


def x_load_ipython_extension__mutmut_1(ipython):
    """
    This function is called by IPython to load the pyinstrument IPython
    extension, which is done with the magic command `%load_ext pyinstrument`.
    """

    from pyinstrument.magic import PyinstrumentMagic

    ipython.register_magics(None)

x_load_ipython_extension__mutmut_mutants : ClassVar[MutantDict] = {
'x_load_ipython_extension__mutmut_1': x_load_ipython_extension__mutmut_1
}

def load_ipython_extension(*args, **kwargs):
    result = _mutmut_trampoline(x_load_ipython_extension__mutmut_orig, x_load_ipython_extension__mutmut_mutants, args, kwargs)
    return result 

load_ipython_extension.__signature__ = _mutmut_signature(x_load_ipython_extension__mutmut_orig)
x_load_ipython_extension__mutmut_orig.__name__ = 'x_load_ipython_extension'
