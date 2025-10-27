from typing import List, Tuple

# pyright: strict


IDENTIFIER_SEP = "\x00"
ATTRIBUTES_SEP = "\x01"

ATTRIBUTE_MARKER_CLASS_NAME = "c"
ATTRIBUTE_MARKER_LINE_NUMBER = "l"
ATTRIBUTE_MARKER_TRACEBACKHIDE = "h"
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


def x_parse_frame_info__mutmut_orig(frame_info: str) -> Tuple[str, List[str]]:
    """
    Parses a frame_info string, returns a tuple of (identifier, attributes),
    where `identifier` is a unique identifier for this code (e.g. a function
    or method), and `attributes` is a list of invocation-specific attributes
    that were captured at profile-time.
    """

    identifier, _, attributes_str = frame_info.partition(ATTRIBUTES_SEP)

    if not attributes_str:
        return identifier, []

    return identifier, attributes_str.split(ATTRIBUTES_SEP)


def x_parse_frame_info__mutmut_1(frame_info: str) -> Tuple[str, List[str]]:
    """
    Parses a frame_info string, returns a tuple of (identifier, attributes),
    where `identifier` is a unique identifier for this code (e.g. a function
    or method), and `attributes` is a list of invocation-specific attributes
    that were captured at profile-time.
    """

    identifier, _, attributes_str = None

    if not attributes_str:
        return identifier, []

    return identifier, attributes_str.split(ATTRIBUTES_SEP)


def x_parse_frame_info__mutmut_2(frame_info: str) -> Tuple[str, List[str]]:
    """
    Parses a frame_info string, returns a tuple of (identifier, attributes),
    where `identifier` is a unique identifier for this code (e.g. a function
    or method), and `attributes` is a list of invocation-specific attributes
    that were captured at profile-time.
    """

    identifier, _, attributes_str = frame_info.partition(None)

    if not attributes_str:
        return identifier, []

    return identifier, attributes_str.split(ATTRIBUTES_SEP)


def x_parse_frame_info__mutmut_3(frame_info: str) -> Tuple[str, List[str]]:
    """
    Parses a frame_info string, returns a tuple of (identifier, attributes),
    where `identifier` is a unique identifier for this code (e.g. a function
    or method), and `attributes` is a list of invocation-specific attributes
    that were captured at profile-time.
    """

    identifier, _, attributes_str = frame_info.rpartition(ATTRIBUTES_SEP)

    if not attributes_str:
        return identifier, []

    return identifier, attributes_str.split(ATTRIBUTES_SEP)


def x_parse_frame_info__mutmut_4(frame_info: str) -> Tuple[str, List[str]]:
    """
    Parses a frame_info string, returns a tuple of (identifier, attributes),
    where `identifier` is a unique identifier for this code (e.g. a function
    or method), and `attributes` is a list of invocation-specific attributes
    that were captured at profile-time.
    """

    identifier, _, attributes_str = frame_info.partition(ATTRIBUTES_SEP)

    if attributes_str:
        return identifier, []

    return identifier, attributes_str.split(ATTRIBUTES_SEP)


def x_parse_frame_info__mutmut_5(frame_info: str) -> Tuple[str, List[str]]:
    """
    Parses a frame_info string, returns a tuple of (identifier, attributes),
    where `identifier` is a unique identifier for this code (e.g. a function
    or method), and `attributes` is a list of invocation-specific attributes
    that were captured at profile-time.
    """

    identifier, _, attributes_str = frame_info.partition(ATTRIBUTES_SEP)

    if not attributes_str:
        return identifier, []

    return identifier, attributes_str.split(None)

x_parse_frame_info__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_frame_info__mutmut_1': x_parse_frame_info__mutmut_1, 
    'x_parse_frame_info__mutmut_2': x_parse_frame_info__mutmut_2, 
    'x_parse_frame_info__mutmut_3': x_parse_frame_info__mutmut_3, 
    'x_parse_frame_info__mutmut_4': x_parse_frame_info__mutmut_4, 
    'x_parse_frame_info__mutmut_5': x_parse_frame_info__mutmut_5
}

def parse_frame_info(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_frame_info__mutmut_orig, x_parse_frame_info__mutmut_mutants, args, kwargs)
    return result 

parse_frame_info.__signature__ = _mutmut_signature(x_parse_frame_info__mutmut_orig)
x_parse_frame_info__mutmut_orig.__name__ = 'x_parse_frame_info'


def x_frame_info_get_identifier__mutmut_orig(frame_info: str) -> str:
    """
    Equivalent to `parse_frame_info(frame_info)[0]`, but faster.
    """
    index = frame_info.find(ATTRIBUTES_SEP)

    if index == -1:
        # no attributes
        return frame_info

    return frame_info[0:index]


def x_frame_info_get_identifier__mutmut_1(frame_info: str) -> str:
    """
    Equivalent to `parse_frame_info(frame_info)[0]`, but faster.
    """
    index = None

    if index == -1:
        # no attributes
        return frame_info

    return frame_info[0:index]


def x_frame_info_get_identifier__mutmut_2(frame_info: str) -> str:
    """
    Equivalent to `parse_frame_info(frame_info)[0]`, but faster.
    """
    index = frame_info.find(None)

    if index == -1:
        # no attributes
        return frame_info

    return frame_info[0:index]


def x_frame_info_get_identifier__mutmut_3(frame_info: str) -> str:
    """
    Equivalent to `parse_frame_info(frame_info)[0]`, but faster.
    """
    index = frame_info.rfind(ATTRIBUTES_SEP)

    if index == -1:
        # no attributes
        return frame_info

    return frame_info[0:index]


def x_frame_info_get_identifier__mutmut_4(frame_info: str) -> str:
    """
    Equivalent to `parse_frame_info(frame_info)[0]`, but faster.
    """
    index = frame_info.find(ATTRIBUTES_SEP)

    if index != -1:
        # no attributes
        return frame_info

    return frame_info[0:index]


def x_frame_info_get_identifier__mutmut_5(frame_info: str) -> str:
    """
    Equivalent to `parse_frame_info(frame_info)[0]`, but faster.
    """
    index = frame_info.find(ATTRIBUTES_SEP)

    if index == +1:
        # no attributes
        return frame_info

    return frame_info[0:index]


def x_frame_info_get_identifier__mutmut_6(frame_info: str) -> str:
    """
    Equivalent to `parse_frame_info(frame_info)[0]`, but faster.
    """
    index = frame_info.find(ATTRIBUTES_SEP)

    if index == -2:
        # no attributes
        return frame_info

    return frame_info[0:index]


def x_frame_info_get_identifier__mutmut_7(frame_info: str) -> str:
    """
    Equivalent to `parse_frame_info(frame_info)[0]`, but faster.
    """
    index = frame_info.find(ATTRIBUTES_SEP)

    if index == -1:
        # no attributes
        return frame_info

    return frame_info[1:index]

x_frame_info_get_identifier__mutmut_mutants : ClassVar[MutantDict] = {
'x_frame_info_get_identifier__mutmut_1': x_frame_info_get_identifier__mutmut_1, 
    'x_frame_info_get_identifier__mutmut_2': x_frame_info_get_identifier__mutmut_2, 
    'x_frame_info_get_identifier__mutmut_3': x_frame_info_get_identifier__mutmut_3, 
    'x_frame_info_get_identifier__mutmut_4': x_frame_info_get_identifier__mutmut_4, 
    'x_frame_info_get_identifier__mutmut_5': x_frame_info_get_identifier__mutmut_5, 
    'x_frame_info_get_identifier__mutmut_6': x_frame_info_get_identifier__mutmut_6, 
    'x_frame_info_get_identifier__mutmut_7': x_frame_info_get_identifier__mutmut_7
}

def frame_info_get_identifier(*args, **kwargs):
    result = _mutmut_trampoline(x_frame_info_get_identifier__mutmut_orig, x_frame_info_get_identifier__mutmut_mutants, args, kwargs)
    return result 

frame_info_get_identifier.__signature__ = _mutmut_signature(x_frame_info_get_identifier__mutmut_orig)
x_frame_info_get_identifier__mutmut_orig.__name__ = 'x_frame_info_get_identifier'
