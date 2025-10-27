import json

from pyinstrument.renderers.base import Renderer
from pyinstrument.session import Session
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


class SessionRenderer(Renderer):
    output_file_extension: str = "pyisession"

    def xǁSessionRendererǁ__init____mutmut_orig(self, tree_format: bool = False):
        super().__init__()
        self.tree_format = tree_format

    def xǁSessionRendererǁ__init____mutmut_1(self, tree_format: bool = True):
        super().__init__()
        self.tree_format = tree_format

    def xǁSessionRendererǁ__init____mutmut_2(self, tree_format: bool = False):
        super().__init__()
        self.tree_format = None
    
    xǁSessionRendererǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSessionRendererǁ__init____mutmut_1': xǁSessionRendererǁ__init____mutmut_1, 
        'xǁSessionRendererǁ__init____mutmut_2': xǁSessionRendererǁ__init____mutmut_2
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSessionRendererǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSessionRendererǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSessionRendererǁ__init____mutmut_orig)
    xǁSessionRendererǁ__init____mutmut_orig.__name__ = 'xǁSessionRendererǁ__init__'

    def xǁSessionRendererǁrender__mutmut_orig(self, session: Session) -> str:
        return json.dumps(session.to_json())

    def xǁSessionRendererǁrender__mutmut_1(self, session: Session) -> str:
        return json.dumps(None)
    
    xǁSessionRendererǁrender__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSessionRendererǁrender__mutmut_1': xǁSessionRendererǁrender__mutmut_1
    }
    
    def render(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSessionRendererǁrender__mutmut_orig"), object.__getattribute__(self, "xǁSessionRendererǁrender__mutmut_mutants"), args, kwargs, self)
        return result 
    
    render.__signature__ = _mutmut_signature(xǁSessionRendererǁrender__mutmut_orig)
    xǁSessionRendererǁrender__mutmut_orig.__name__ = 'xǁSessionRendererǁrender'
