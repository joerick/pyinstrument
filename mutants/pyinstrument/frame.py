from __future__ import annotations

import json
import math
import typing
import uuid
from typing import Callable, Sequence

from pyinstrument.frame_info import (
    ATTRIBUTE_MARKER_CLASS_NAME,
    ATTRIBUTE_MARKER_TRACEBACKHIDE,
    frame_info_get_identifier,
    parse_frame_info,
)

# pyright: strict


# the 'synthetic' frames these identifiers represent don't reflect real Python
# frames
AWAIT_FRAME_IDENTIFIER = "[await]"
SELF_TIME_FRAME_IDENTIFIER = "[self]"
OUT_OF_CONTEXT_FRAME_IDENTIFIER = "[out-of-context]"
DUMMY_ROOT_FRAME_IDENTIFIER = "[root]"

SYNTHETIC_FRAME_IDENTIFIERS = frozenset(
    [
        AWAIT_FRAME_IDENTIFIER,
        SELF_TIME_FRAME_IDENTIFIER,
        OUT_OF_CONTEXT_FRAME_IDENTIFIER,
        DUMMY_ROOT_FRAME_IDENTIFIER,
    ]
)

# these identifiers can have no children - correspondingly, they can have time
# that is not the sum of their children's time
SYNTHETIC_LEAF_IDENTIFIERS = frozenset(
    [
        AWAIT_FRAME_IDENTIFIER,
        SELF_TIME_FRAME_IDENTIFIER,
        OUT_OF_CONTEXT_FRAME_IDENTIFIER,
    ]
)
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


class FrameContext(typing.Protocol):
    def shorten_path(self, path: str) -> str: ...
    @property
    def sys_prefixes(self) -> Sequence[str]: ...


class Frame:
    """
    Object that represents a stack frame in the parsed tree
    """

    parent: Frame | None
    group: FrameGroup | None
    time: float

    # the session this frame belongs to
    _context: FrameContext | None

    # tracks the time from frames that were deleted during processing
    absorbed_time: float

    attributes: dict[str, float]

    def xǁFrameǁ__init____mutmut_orig(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_1(
        self,
        identifier_or_frame_info: str = "XXXX",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_2(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 1,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_3(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = None
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_4(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(None)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_5(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = None
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_6(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = ""
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_7(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = None
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_8(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 1.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_9(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = ""
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_10(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = None
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_11(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 1.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_12(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = None

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_13(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = None
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_14(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split(None)
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_15(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("XX\x00XX")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_16(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = None
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_17(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = None

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_18(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=None, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_19(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=None)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_20(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(time=time)

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_21(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, )

        if children:
            for child in children:
                self.add_child(child)

    def xǁFrameǁ__init____mutmut_22(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
        context: FrameContext | None = None,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0
        self._context = context

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(None)
    
    xǁFrameǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameǁ__init____mutmut_1': xǁFrameǁ__init____mutmut_1, 
        'xǁFrameǁ__init____mutmut_2': xǁFrameǁ__init____mutmut_2, 
        'xǁFrameǁ__init____mutmut_3': xǁFrameǁ__init____mutmut_3, 
        'xǁFrameǁ__init____mutmut_4': xǁFrameǁ__init____mutmut_4, 
        'xǁFrameǁ__init____mutmut_5': xǁFrameǁ__init____mutmut_5, 
        'xǁFrameǁ__init____mutmut_6': xǁFrameǁ__init____mutmut_6, 
        'xǁFrameǁ__init____mutmut_7': xǁFrameǁ__init____mutmut_7, 
        'xǁFrameǁ__init____mutmut_8': xǁFrameǁ__init____mutmut_8, 
        'xǁFrameǁ__init____mutmut_9': xǁFrameǁ__init____mutmut_9, 
        'xǁFrameǁ__init____mutmut_10': xǁFrameǁ__init____mutmut_10, 
        'xǁFrameǁ__init____mutmut_11': xǁFrameǁ__init____mutmut_11, 
        'xǁFrameǁ__init____mutmut_12': xǁFrameǁ__init____mutmut_12, 
        'xǁFrameǁ__init____mutmut_13': xǁFrameǁ__init____mutmut_13, 
        'xǁFrameǁ__init____mutmut_14': xǁFrameǁ__init____mutmut_14, 
        'xǁFrameǁ__init____mutmut_15': xǁFrameǁ__init____mutmut_15, 
        'xǁFrameǁ__init____mutmut_16': xǁFrameǁ__init____mutmut_16, 
        'xǁFrameǁ__init____mutmut_17': xǁFrameǁ__init____mutmut_17, 
        'xǁFrameǁ__init____mutmut_18': xǁFrameǁ__init____mutmut_18, 
        'xǁFrameǁ__init____mutmut_19': xǁFrameǁ__init____mutmut_19, 
        'xǁFrameǁ__init____mutmut_20': xǁFrameǁ__init____mutmut_20, 
        'xǁFrameǁ__init____mutmut_21': xǁFrameǁ__init____mutmut_21, 
        'xǁFrameǁ__init____mutmut_22': xǁFrameǁ__init____mutmut_22
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFrameǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁFrameǁ__init____mutmut_orig)
    xǁFrameǁ__init____mutmut_orig.__name__ = 'xǁFrameǁ__init__'

    def xǁFrameǁrecord_time_from_frame_info__mutmut_orig(self, frame_info: str, time: float):
        self.time += time

        _, attributes_list = parse_frame_info(frame_info)

        for attribute in attributes_list:
            try:
                self.attributes[attribute] += time
            except KeyError:
                self.attributes[attribute] = time

    def xǁFrameǁrecord_time_from_frame_info__mutmut_1(self, frame_info: str, time: float):
        self.time = time

        _, attributes_list = parse_frame_info(frame_info)

        for attribute in attributes_list:
            try:
                self.attributes[attribute] += time
            except KeyError:
                self.attributes[attribute] = time

    def xǁFrameǁrecord_time_from_frame_info__mutmut_2(self, frame_info: str, time: float):
        self.time -= time

        _, attributes_list = parse_frame_info(frame_info)

        for attribute in attributes_list:
            try:
                self.attributes[attribute] += time
            except KeyError:
                self.attributes[attribute] = time

    def xǁFrameǁrecord_time_from_frame_info__mutmut_3(self, frame_info: str, time: float):
        self.time += time

        _, attributes_list = None

        for attribute in attributes_list:
            try:
                self.attributes[attribute] += time
            except KeyError:
                self.attributes[attribute] = time

    def xǁFrameǁrecord_time_from_frame_info__mutmut_4(self, frame_info: str, time: float):
        self.time += time

        _, attributes_list = parse_frame_info(None)

        for attribute in attributes_list:
            try:
                self.attributes[attribute] += time
            except KeyError:
                self.attributes[attribute] = time

    def xǁFrameǁrecord_time_from_frame_info__mutmut_5(self, frame_info: str, time: float):
        self.time += time

        _, attributes_list = parse_frame_info(frame_info)

        for attribute in attributes_list:
            try:
                self.attributes[attribute] = time
            except KeyError:
                self.attributes[attribute] = time

    def xǁFrameǁrecord_time_from_frame_info__mutmut_6(self, frame_info: str, time: float):
        self.time += time

        _, attributes_list = parse_frame_info(frame_info)

        for attribute in attributes_list:
            try:
                self.attributes[attribute] -= time
            except KeyError:
                self.attributes[attribute] = time

    def xǁFrameǁrecord_time_from_frame_info__mutmut_7(self, frame_info: str, time: float):
        self.time += time

        _, attributes_list = parse_frame_info(frame_info)

        for attribute in attributes_list:
            try:
                self.attributes[attribute] += time
            except KeyError:
                self.attributes[attribute] = None
    
    xǁFrameǁrecord_time_from_frame_info__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameǁrecord_time_from_frame_info__mutmut_1': xǁFrameǁrecord_time_from_frame_info__mutmut_1, 
        'xǁFrameǁrecord_time_from_frame_info__mutmut_2': xǁFrameǁrecord_time_from_frame_info__mutmut_2, 
        'xǁFrameǁrecord_time_from_frame_info__mutmut_3': xǁFrameǁrecord_time_from_frame_info__mutmut_3, 
        'xǁFrameǁrecord_time_from_frame_info__mutmut_4': xǁFrameǁrecord_time_from_frame_info__mutmut_4, 
        'xǁFrameǁrecord_time_from_frame_info__mutmut_5': xǁFrameǁrecord_time_from_frame_info__mutmut_5, 
        'xǁFrameǁrecord_time_from_frame_info__mutmut_6': xǁFrameǁrecord_time_from_frame_info__mutmut_6, 
        'xǁFrameǁrecord_time_from_frame_info__mutmut_7': xǁFrameǁrecord_time_from_frame_info__mutmut_7
    }
    
    def record_time_from_frame_info(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameǁrecord_time_from_frame_info__mutmut_orig"), object.__getattribute__(self, "xǁFrameǁrecord_time_from_frame_info__mutmut_mutants"), args, kwargs, self)
        return result 
    
    record_time_from_frame_info.__signature__ = _mutmut_signature(xǁFrameǁrecord_time_from_frame_info__mutmut_orig)
    xǁFrameǁrecord_time_from_frame_info__mutmut_orig.__name__ = 'xǁFrameǁrecord_time_from_frame_info'

    def xǁFrameǁremove_from_parent__mutmut_orig(self):
        """
        Removes this frame from its parent, and nulls the parent link
        """
        if self.parent:
            self.parent._children.remove(self)
            self.parent = None

    def xǁFrameǁremove_from_parent__mutmut_1(self):
        """
        Removes this frame from its parent, and nulls the parent link
        """
        if self.parent:
            self.parent._children.remove(None)
            self.parent = None

    def xǁFrameǁremove_from_parent__mutmut_2(self):
        """
        Removes this frame from its parent, and nulls the parent link
        """
        if self.parent:
            self.parent._children.remove(self)
            self.parent = ""
    
    xǁFrameǁremove_from_parent__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameǁremove_from_parent__mutmut_1': xǁFrameǁremove_from_parent__mutmut_1, 
        'xǁFrameǁremove_from_parent__mutmut_2': xǁFrameǁremove_from_parent__mutmut_2
    }
    
    def remove_from_parent(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameǁremove_from_parent__mutmut_orig"), object.__getattribute__(self, "xǁFrameǁremove_from_parent__mutmut_mutants"), args, kwargs, self)
        return result 
    
    remove_from_parent.__signature__ = _mutmut_signature(xǁFrameǁremove_from_parent__mutmut_orig)
    xǁFrameǁremove_from_parent__mutmut_orig.__name__ = 'xǁFrameǁremove_from_parent'

    @property
    def context(self):
        if not self._context:
            raise RuntimeError("Frame has no context")
        return self._context

    def xǁFrameǁset_context__mutmut_orig(self, context: FrameContext | None):
        self._context = context
        for child in self._children:
            child.set_context(context)

    def xǁFrameǁset_context__mutmut_1(self, context: FrameContext | None):
        self._context = None
        for child in self._children:
            child.set_context(context)

    def xǁFrameǁset_context__mutmut_2(self, context: FrameContext | None):
        self._context = context
        for child in self._children:
            child.set_context(None)
    
    xǁFrameǁset_context__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameǁset_context__mutmut_1': xǁFrameǁset_context__mutmut_1, 
        'xǁFrameǁset_context__mutmut_2': xǁFrameǁset_context__mutmut_2
    }
    
    def set_context(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameǁset_context__mutmut_orig"), object.__getattribute__(self, "xǁFrameǁset_context__mutmut_mutants"), args, kwargs, self)
        return result 
    
    set_context.__signature__ = _mutmut_signature(xǁFrameǁset_context__mutmut_orig)
    xǁFrameǁset_context__mutmut_orig.__name__ = 'xǁFrameǁset_context'

    @staticmethod
    def new_subclass_with_frame_info(frame_info: str) -> Frame:
        # TODO remove me
        return Frame(identifier_or_frame_info=frame_info)

    @property
    def proportion_of_parent(self) -> float:
        if self.parent:
            try:
                return self.time / self.parent.time
            except ZeroDivisionError:
                return float("nan")
        else:
            return 1.0

    @property
    def total_self_time(self) -> float:
        """
        The total amount of self time in this frame (including self time recorded by SelfTimeFrame
        children, and await time from AwaitTimeFrame children)
        """

        # self time is time in this frame, minus time in children
        self_time = self.time
        real_children = [c for c in self.children if not c.is_synthetic]

        for child in real_children:
            self_time -= child.time

        return self_time

    @property
    def function(self) -> str:
        return self._identifier_parts[0]

    @property
    def file_path(self) -> str | None:
        if len(self._identifier_parts) > 1:
            return self._identifier_parts[1]

    @property
    def line_no(self) -> int | None:
        if len(self._identifier_parts) > 2:
            return int(self._identifier_parts[2])

    @property
    def file_path_short(self) -> str | None:
        """Return the path resolved against the closest entry in sys.path"""
        if self.is_synthetic and self.parent:
            return self.parent.file_path_short

        if not self.file_path:
            return None

        return self.context.shorten_path(self.file_path)

    @property
    def is_application_code(self) -> bool:
        if self.is_synthetic:
            return False

        file_path = self.file_path

        if not file_path:
            return False

        if any(file_path.startswith(p) for p in self.context.sys_prefixes):
            # lives in python install dir or virtualenv
            return False

        if file_path.startswith("<"):
            if file_path.startswith("<ipython-input-"):
                # lines typed at a console or in a notebook are app code
                return True
            elif file_path == "<string>" or file_path == "<stdin>":
                # eval/exec is app code if started by a parent frame that is
                # app code
                if self.parent:
                    return self.parent.is_application_code
                else:
                    # if this is the root frame, it must have been started
                    # with -c, so it's app code
                    return True
            else:
                # otherwise, this is probably some library-internal code gen
                return False

        return True

    def xǁFrameǁcode_position_short__mutmut_orig(self) -> str | None:
        file_path_short = self.file_path_short
        if file_path_short and self.line_no:
            return "%s:%i" % (file_path_short, self.line_no)
        return file_path_short

    def xǁFrameǁcode_position_short__mutmut_1(self) -> str | None:
        file_path_short = None
        if file_path_short and self.line_no:
            return "%s:%i" % (file_path_short, self.line_no)
        return file_path_short

    def xǁFrameǁcode_position_short__mutmut_2(self) -> str | None:
        file_path_short = self.file_path_short
        if file_path_short or self.line_no:
            return "%s:%i" % (file_path_short, self.line_no)
        return file_path_short

    def xǁFrameǁcode_position_short__mutmut_3(self) -> str | None:
        file_path_short = self.file_path_short
        if file_path_short and self.line_no:
            return "%s:%i" / (file_path_short, self.line_no)
        return file_path_short

    def xǁFrameǁcode_position_short__mutmut_4(self) -> str | None:
        file_path_short = self.file_path_short
        if file_path_short and self.line_no:
            return "XX%s:%iXX" % (file_path_short, self.line_no)
        return file_path_short

    def xǁFrameǁcode_position_short__mutmut_5(self) -> str | None:
        file_path_short = self.file_path_short
        if file_path_short and self.line_no:
            return "%S:%I" % (file_path_short, self.line_no)
        return file_path_short
    
    xǁFrameǁcode_position_short__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameǁcode_position_short__mutmut_1': xǁFrameǁcode_position_short__mutmut_1, 
        'xǁFrameǁcode_position_short__mutmut_2': xǁFrameǁcode_position_short__mutmut_2, 
        'xǁFrameǁcode_position_short__mutmut_3': xǁFrameǁcode_position_short__mutmut_3, 
        'xǁFrameǁcode_position_short__mutmut_4': xǁFrameǁcode_position_short__mutmut_4, 
        'xǁFrameǁcode_position_short__mutmut_5': xǁFrameǁcode_position_short__mutmut_5
    }
    
    def code_position_short(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameǁcode_position_short__mutmut_orig"), object.__getattribute__(self, "xǁFrameǁcode_position_short__mutmut_mutants"), args, kwargs, self)
        return result 
    
    code_position_short.__signature__ = _mutmut_signature(xǁFrameǁcode_position_short__mutmut_orig)
    xǁFrameǁcode_position_short__mutmut_orig.__name__ = 'xǁFrameǁcode_position_short'

    _children: list[Frame]
    attributes: dict[str, float]

    def xǁFrameǁadd_child__mutmut_orig(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_1(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier not in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_2(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError(None)

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_3(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("XXCannot add children to a leaf-only frameXX")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_4(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_5(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("CANNOT ADD CHILDREN TO A LEAF-ONLY FRAME")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_6(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = None
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_7(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(None)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_8(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is not None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_9(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(None)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_10(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = None
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_11(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) - 1
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_12(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(None) + 1
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_13(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.rindex(after) + 1
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_14(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 2
            self._children.insert(index, frame)

    def xǁFrameǁadd_child__mutmut_15(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(None, frame)

    def xǁFrameǁadd_child__mutmut_16(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, None)

    def xǁFrameǁadd_child__mutmut_17(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(frame)

    def xǁFrameǁadd_child__mutmut_18(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        frame.set_context(self._context)
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, )
    
    xǁFrameǁadd_child__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameǁadd_child__mutmut_1': xǁFrameǁadd_child__mutmut_1, 
        'xǁFrameǁadd_child__mutmut_2': xǁFrameǁadd_child__mutmut_2, 
        'xǁFrameǁadd_child__mutmut_3': xǁFrameǁadd_child__mutmut_3, 
        'xǁFrameǁadd_child__mutmut_4': xǁFrameǁadd_child__mutmut_4, 
        'xǁFrameǁadd_child__mutmut_5': xǁFrameǁadd_child__mutmut_5, 
        'xǁFrameǁadd_child__mutmut_6': xǁFrameǁadd_child__mutmut_6, 
        'xǁFrameǁadd_child__mutmut_7': xǁFrameǁadd_child__mutmut_7, 
        'xǁFrameǁadd_child__mutmut_8': xǁFrameǁadd_child__mutmut_8, 
        'xǁFrameǁadd_child__mutmut_9': xǁFrameǁadd_child__mutmut_9, 
        'xǁFrameǁadd_child__mutmut_10': xǁFrameǁadd_child__mutmut_10, 
        'xǁFrameǁadd_child__mutmut_11': xǁFrameǁadd_child__mutmut_11, 
        'xǁFrameǁadd_child__mutmut_12': xǁFrameǁadd_child__mutmut_12, 
        'xǁFrameǁadd_child__mutmut_13': xǁFrameǁadd_child__mutmut_13, 
        'xǁFrameǁadd_child__mutmut_14': xǁFrameǁadd_child__mutmut_14, 
        'xǁFrameǁadd_child__mutmut_15': xǁFrameǁadd_child__mutmut_15, 
        'xǁFrameǁadd_child__mutmut_16': xǁFrameǁadd_child__mutmut_16, 
        'xǁFrameǁadd_child__mutmut_17': xǁFrameǁadd_child__mutmut_17, 
        'xǁFrameǁadd_child__mutmut_18': xǁFrameǁadd_child__mutmut_18
    }
    
    def add_child(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameǁadd_child__mutmut_orig"), object.__getattribute__(self, "xǁFrameǁadd_child__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_child.__signature__ = _mutmut_signature(xǁFrameǁadd_child__mutmut_orig)
    xǁFrameǁadd_child__mutmut_orig.__name__ = 'xǁFrameǁadd_child'

    def xǁFrameǁadd_children__mutmut_orig(self, frames: Sequence[Frame], after: Frame | None = None):
        """
        Convenience method to add multiple frames at once.
        """
        if after is not None:
            # if there's an 'after' parameter, add the frames in reverse so the order is
            # preserved.
            for frame in reversed(frames):
                self.add_child(frame, after=after)
        else:
            for frame in frames:
                self.add_child(frame)

    def xǁFrameǁadd_children__mutmut_1(self, frames: Sequence[Frame], after: Frame | None = None):
        """
        Convenience method to add multiple frames at once.
        """
        if after is None:
            # if there's an 'after' parameter, add the frames in reverse so the order is
            # preserved.
            for frame in reversed(frames):
                self.add_child(frame, after=after)
        else:
            for frame in frames:
                self.add_child(frame)

    def xǁFrameǁadd_children__mutmut_2(self, frames: Sequence[Frame], after: Frame | None = None):
        """
        Convenience method to add multiple frames at once.
        """
        if after is not None:
            # if there's an 'after' parameter, add the frames in reverse so the order is
            # preserved.
            for frame in reversed(None):
                self.add_child(frame, after=after)
        else:
            for frame in frames:
                self.add_child(frame)

    def xǁFrameǁadd_children__mutmut_3(self, frames: Sequence[Frame], after: Frame | None = None):
        """
        Convenience method to add multiple frames at once.
        """
        if after is not None:
            # if there's an 'after' parameter, add the frames in reverse so the order is
            # preserved.
            for frame in reversed(frames):
                self.add_child(None, after=after)
        else:
            for frame in frames:
                self.add_child(frame)

    def xǁFrameǁadd_children__mutmut_4(self, frames: Sequence[Frame], after: Frame | None = None):
        """
        Convenience method to add multiple frames at once.
        """
        if after is not None:
            # if there's an 'after' parameter, add the frames in reverse so the order is
            # preserved.
            for frame in reversed(frames):
                self.add_child(frame, after=None)
        else:
            for frame in frames:
                self.add_child(frame)

    def xǁFrameǁadd_children__mutmut_5(self, frames: Sequence[Frame], after: Frame | None = None):
        """
        Convenience method to add multiple frames at once.
        """
        if after is not None:
            # if there's an 'after' parameter, add the frames in reverse so the order is
            # preserved.
            for frame in reversed(frames):
                self.add_child(after=after)
        else:
            for frame in frames:
                self.add_child(frame)

    def xǁFrameǁadd_children__mutmut_6(self, frames: Sequence[Frame], after: Frame | None = None):
        """
        Convenience method to add multiple frames at once.
        """
        if after is not None:
            # if there's an 'after' parameter, add the frames in reverse so the order is
            # preserved.
            for frame in reversed(frames):
                self.add_child(frame, )
        else:
            for frame in frames:
                self.add_child(frame)

    def xǁFrameǁadd_children__mutmut_7(self, frames: Sequence[Frame], after: Frame | None = None):
        """
        Convenience method to add multiple frames at once.
        """
        if after is not None:
            # if there's an 'after' parameter, add the frames in reverse so the order is
            # preserved.
            for frame in reversed(frames):
                self.add_child(frame, after=after)
        else:
            for frame in frames:
                self.add_child(None)
    
    xǁFrameǁadd_children__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameǁadd_children__mutmut_1': xǁFrameǁadd_children__mutmut_1, 
        'xǁFrameǁadd_children__mutmut_2': xǁFrameǁadd_children__mutmut_2, 
        'xǁFrameǁadd_children__mutmut_3': xǁFrameǁadd_children__mutmut_3, 
        'xǁFrameǁadd_children__mutmut_4': xǁFrameǁadd_children__mutmut_4, 
        'xǁFrameǁadd_children__mutmut_5': xǁFrameǁadd_children__mutmut_5, 
        'xǁFrameǁadd_children__mutmut_6': xǁFrameǁadd_children__mutmut_6, 
        'xǁFrameǁadd_children__mutmut_7': xǁFrameǁadd_children__mutmut_7
    }
    
    def add_children(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameǁadd_children__mutmut_orig"), object.__getattribute__(self, "xǁFrameǁadd_children__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_children.__signature__ = _mutmut_signature(xǁFrameǁadd_children__mutmut_orig)
    xǁFrameǁadd_children__mutmut_orig.__name__ = 'xǁFrameǁadd_children'

    @property
    def is_synthetic(self) -> bool:
        return self.identifier in SYNTHETIC_FRAME_IDENTIFIERS

    @property
    def is_synthetic_leaf(self) -> bool:
        return self.identifier in SYNTHETIC_LEAF_IDENTIFIERS

    @property
    def children(self) -> Sequence[Frame]:
        # Return an immutable copy (this property should only be mutated using methods)
        # Also, returning a copy avoid problems when mutating while iterating, which happens a lot
        # in processors!
        return tuple(self._children)

    def xǁFrameǁawait_time__mutmut_orig(self) -> float:
        # i'd rather this was a property, but properties use twice as many stack frames
        await_time = 0

        if self.identifier == AWAIT_FRAME_IDENTIFIER:
            await_time += self.time

        for child in self.children:
            await_time += child.await_time()

        return await_time

    def xǁFrameǁawait_time__mutmut_1(self) -> float:
        # i'd rather this was a property, but properties use twice as many stack frames
        await_time = None

        if self.identifier == AWAIT_FRAME_IDENTIFIER:
            await_time += self.time

        for child in self.children:
            await_time += child.await_time()

        return await_time

    def xǁFrameǁawait_time__mutmut_2(self) -> float:
        # i'd rather this was a property, but properties use twice as many stack frames
        await_time = 1

        if self.identifier == AWAIT_FRAME_IDENTIFIER:
            await_time += self.time

        for child in self.children:
            await_time += child.await_time()

        return await_time

    def xǁFrameǁawait_time__mutmut_3(self) -> float:
        # i'd rather this was a property, but properties use twice as many stack frames
        await_time = 0

        if self.identifier != AWAIT_FRAME_IDENTIFIER:
            await_time += self.time

        for child in self.children:
            await_time += child.await_time()

        return await_time

    def xǁFrameǁawait_time__mutmut_4(self) -> float:
        # i'd rather this was a property, but properties use twice as many stack frames
        await_time = 0

        if self.identifier == AWAIT_FRAME_IDENTIFIER:
            await_time = self.time

        for child in self.children:
            await_time += child.await_time()

        return await_time

    def xǁFrameǁawait_time__mutmut_5(self) -> float:
        # i'd rather this was a property, but properties use twice as many stack frames
        await_time = 0

        if self.identifier == AWAIT_FRAME_IDENTIFIER:
            await_time -= self.time

        for child in self.children:
            await_time += child.await_time()

        return await_time

    def xǁFrameǁawait_time__mutmut_6(self) -> float:
        # i'd rather this was a property, but properties use twice as many stack frames
        await_time = 0

        if self.identifier == AWAIT_FRAME_IDENTIFIER:
            await_time += self.time

        for child in self.children:
            await_time = child.await_time()

        return await_time

    def xǁFrameǁawait_time__mutmut_7(self) -> float:
        # i'd rather this was a property, but properties use twice as many stack frames
        await_time = 0

        if self.identifier == AWAIT_FRAME_IDENTIFIER:
            await_time += self.time

        for child in self.children:
            await_time -= child.await_time()

        return await_time
    
    xǁFrameǁawait_time__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameǁawait_time__mutmut_1': xǁFrameǁawait_time__mutmut_1, 
        'xǁFrameǁawait_time__mutmut_2': xǁFrameǁawait_time__mutmut_2, 
        'xǁFrameǁawait_time__mutmut_3': xǁFrameǁawait_time__mutmut_3, 
        'xǁFrameǁawait_time__mutmut_4': xǁFrameǁawait_time__mutmut_4, 
        'xǁFrameǁawait_time__mutmut_5': xǁFrameǁawait_time__mutmut_5, 
        'xǁFrameǁawait_time__mutmut_6': xǁFrameǁawait_time__mutmut_6, 
        'xǁFrameǁawait_time__mutmut_7': xǁFrameǁawait_time__mutmut_7
    }
    
    def await_time(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameǁawait_time__mutmut_orig"), object.__getattribute__(self, "xǁFrameǁawait_time__mutmut_mutants"), args, kwargs, self)
        return result 
    
    await_time.__signature__ = _mutmut_signature(xǁFrameǁawait_time__mutmut_orig)
    xǁFrameǁawait_time__mutmut_orig.__name__ = 'xǁFrameǁawait_time'

    def xǁFrameǁget_attribute_value__mutmut_orig(self, attribute_marker: str) -> str | None:
        """
        Returns the value of the attribute. If multiple values are present,
        the most commonly observed one is returned.
        """
        # Attributes are recorded as a dict, with the key representing an
        # observation, and the value representing the duration that it was
        # observed. the first character of the observation is the 'marker' -
        # the type of the attribute, the rest is data.
        matching_attributes = [
            a_tuple
            for a_tuple in self.attributes.items()
            if a_tuple[0].startswith(attribute_marker)
        ]

        if len(matching_attributes) == 0:
            return None

        top_attribute, _ = max(matching_attributes, key=lambda a: a[1])

        # strip off the marker, return the data
        return top_attribute[1:]

    def xǁFrameǁget_attribute_value__mutmut_1(self, attribute_marker: str) -> str | None:
        """
        Returns the value of the attribute. If multiple values are present,
        the most commonly observed one is returned.
        """
        # Attributes are recorded as a dict, with the key representing an
        # observation, and the value representing the duration that it was
        # observed. the first character of the observation is the 'marker' -
        # the type of the attribute, the rest is data.
        matching_attributes = None

        if len(matching_attributes) == 0:
            return None

        top_attribute, _ = max(matching_attributes, key=lambda a: a[1])

        # strip off the marker, return the data
        return top_attribute[1:]

    def xǁFrameǁget_attribute_value__mutmut_2(self, attribute_marker: str) -> str | None:
        """
        Returns the value of the attribute. If multiple values are present,
        the most commonly observed one is returned.
        """
        # Attributes are recorded as a dict, with the key representing an
        # observation, and the value representing the duration that it was
        # observed. the first character of the observation is the 'marker' -
        # the type of the attribute, the rest is data.
        matching_attributes = [
            a_tuple
            for a_tuple in self.attributes.items()
            if a_tuple[0].startswith(None)
        ]

        if len(matching_attributes) == 0:
            return None

        top_attribute, _ = max(matching_attributes, key=lambda a: a[1])

        # strip off the marker, return the data
        return top_attribute[1:]

    def xǁFrameǁget_attribute_value__mutmut_3(self, attribute_marker: str) -> str | None:
        """
        Returns the value of the attribute. If multiple values are present,
        the most commonly observed one is returned.
        """
        # Attributes are recorded as a dict, with the key representing an
        # observation, and the value representing the duration that it was
        # observed. the first character of the observation is the 'marker' -
        # the type of the attribute, the rest is data.
        matching_attributes = [
            a_tuple
            for a_tuple in self.attributes.items()
            if a_tuple[1].startswith(attribute_marker)
        ]

        if len(matching_attributes) == 0:
            return None

        top_attribute, _ = max(matching_attributes, key=lambda a: a[1])

        # strip off the marker, return the data
        return top_attribute[1:]

    def xǁFrameǁget_attribute_value__mutmut_4(self, attribute_marker: str) -> str | None:
        """
        Returns the value of the attribute. If multiple values are present,
        the most commonly observed one is returned.
        """
        # Attributes are recorded as a dict, with the key representing an
        # observation, and the value representing the duration that it was
        # observed. the first character of the observation is the 'marker' -
        # the type of the attribute, the rest is data.
        matching_attributes = [
            a_tuple
            for a_tuple in self.attributes.items()
            if a_tuple[0].startswith(attribute_marker)
        ]

        if len(matching_attributes) != 0:
            return None

        top_attribute, _ = max(matching_attributes, key=lambda a: a[1])

        # strip off the marker, return the data
        return top_attribute[1:]

    def xǁFrameǁget_attribute_value__mutmut_5(self, attribute_marker: str) -> str | None:
        """
        Returns the value of the attribute. If multiple values are present,
        the most commonly observed one is returned.
        """
        # Attributes are recorded as a dict, with the key representing an
        # observation, and the value representing the duration that it was
        # observed. the first character of the observation is the 'marker' -
        # the type of the attribute, the rest is data.
        matching_attributes = [
            a_tuple
            for a_tuple in self.attributes.items()
            if a_tuple[0].startswith(attribute_marker)
        ]

        if len(matching_attributes) == 1:
            return None

        top_attribute, _ = max(matching_attributes, key=lambda a: a[1])

        # strip off the marker, return the data
        return top_attribute[1:]

    def xǁFrameǁget_attribute_value__mutmut_6(self, attribute_marker: str) -> str | None:
        """
        Returns the value of the attribute. If multiple values are present,
        the most commonly observed one is returned.
        """
        # Attributes are recorded as a dict, with the key representing an
        # observation, and the value representing the duration that it was
        # observed. the first character of the observation is the 'marker' -
        # the type of the attribute, the rest is data.
        matching_attributes = [
            a_tuple
            for a_tuple in self.attributes.items()
            if a_tuple[0].startswith(attribute_marker)
        ]

        if len(matching_attributes) == 0:
            return None

        top_attribute, _ = None

        # strip off the marker, return the data
        return top_attribute[1:]

    def xǁFrameǁget_attribute_value__mutmut_7(self, attribute_marker: str) -> str | None:
        """
        Returns the value of the attribute. If multiple values are present,
        the most commonly observed one is returned.
        """
        # Attributes are recorded as a dict, with the key representing an
        # observation, and the value representing the duration that it was
        # observed. the first character of the observation is the 'marker' -
        # the type of the attribute, the rest is data.
        matching_attributes = [
            a_tuple
            for a_tuple in self.attributes.items()
            if a_tuple[0].startswith(attribute_marker)
        ]

        if len(matching_attributes) == 0:
            return None

        top_attribute, _ = max(None, key=lambda a: a[1])

        # strip off the marker, return the data
        return top_attribute[1:]

    def xǁFrameǁget_attribute_value__mutmut_8(self, attribute_marker: str) -> str | None:
        """
        Returns the value of the attribute. If multiple values are present,
        the most commonly observed one is returned.
        """
        # Attributes are recorded as a dict, with the key representing an
        # observation, and the value representing the duration that it was
        # observed. the first character of the observation is the 'marker' -
        # the type of the attribute, the rest is data.
        matching_attributes = [
            a_tuple
            for a_tuple in self.attributes.items()
            if a_tuple[0].startswith(attribute_marker)
        ]

        if len(matching_attributes) == 0:
            return None

        top_attribute, _ = max(matching_attributes, key=None)

        # strip off the marker, return the data
        return top_attribute[1:]

    def xǁFrameǁget_attribute_value__mutmut_9(self, attribute_marker: str) -> str | None:
        """
        Returns the value of the attribute. If multiple values are present,
        the most commonly observed one is returned.
        """
        # Attributes are recorded as a dict, with the key representing an
        # observation, and the value representing the duration that it was
        # observed. the first character of the observation is the 'marker' -
        # the type of the attribute, the rest is data.
        matching_attributes = [
            a_tuple
            for a_tuple in self.attributes.items()
            if a_tuple[0].startswith(attribute_marker)
        ]

        if len(matching_attributes) == 0:
            return None

        top_attribute, _ = max(key=lambda a: a[1])

        # strip off the marker, return the data
        return top_attribute[1:]

    def xǁFrameǁget_attribute_value__mutmut_10(self, attribute_marker: str) -> str | None:
        """
        Returns the value of the attribute. If multiple values are present,
        the most commonly observed one is returned.
        """
        # Attributes are recorded as a dict, with the key representing an
        # observation, and the value representing the duration that it was
        # observed. the first character of the observation is the 'marker' -
        # the type of the attribute, the rest is data.
        matching_attributes = [
            a_tuple
            for a_tuple in self.attributes.items()
            if a_tuple[0].startswith(attribute_marker)
        ]

        if len(matching_attributes) == 0:
            return None

        top_attribute, _ = max(matching_attributes, )

        # strip off the marker, return the data
        return top_attribute[1:]

    def xǁFrameǁget_attribute_value__mutmut_11(self, attribute_marker: str) -> str | None:
        """
        Returns the value of the attribute. If multiple values are present,
        the most commonly observed one is returned.
        """
        # Attributes are recorded as a dict, with the key representing an
        # observation, and the value representing the duration that it was
        # observed. the first character of the observation is the 'marker' -
        # the type of the attribute, the rest is data.
        matching_attributes = [
            a_tuple
            for a_tuple in self.attributes.items()
            if a_tuple[0].startswith(attribute_marker)
        ]

        if len(matching_attributes) == 0:
            return None

        top_attribute, _ = max(matching_attributes, key=lambda a: None)

        # strip off the marker, return the data
        return top_attribute[1:]

    def xǁFrameǁget_attribute_value__mutmut_12(self, attribute_marker: str) -> str | None:
        """
        Returns the value of the attribute. If multiple values are present,
        the most commonly observed one is returned.
        """
        # Attributes are recorded as a dict, with the key representing an
        # observation, and the value representing the duration that it was
        # observed. the first character of the observation is the 'marker' -
        # the type of the attribute, the rest is data.
        matching_attributes = [
            a_tuple
            for a_tuple in self.attributes.items()
            if a_tuple[0].startswith(attribute_marker)
        ]

        if len(matching_attributes) == 0:
            return None

        top_attribute, _ = max(matching_attributes, key=lambda a: a[2])

        # strip off the marker, return the data
        return top_attribute[1:]

    def xǁFrameǁget_attribute_value__mutmut_13(self, attribute_marker: str) -> str | None:
        """
        Returns the value of the attribute. If multiple values are present,
        the most commonly observed one is returned.
        """
        # Attributes are recorded as a dict, with the key representing an
        # observation, and the value representing the duration that it was
        # observed. the first character of the observation is the 'marker' -
        # the type of the attribute, the rest is data.
        matching_attributes = [
            a_tuple
            for a_tuple in self.attributes.items()
            if a_tuple[0].startswith(attribute_marker)
        ]

        if len(matching_attributes) == 0:
            return None

        top_attribute, _ = max(matching_attributes, key=lambda a: a[1])

        # strip off the marker, return the data
        return top_attribute[2:]
    
    xǁFrameǁget_attribute_value__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameǁget_attribute_value__mutmut_1': xǁFrameǁget_attribute_value__mutmut_1, 
        'xǁFrameǁget_attribute_value__mutmut_2': xǁFrameǁget_attribute_value__mutmut_2, 
        'xǁFrameǁget_attribute_value__mutmut_3': xǁFrameǁget_attribute_value__mutmut_3, 
        'xǁFrameǁget_attribute_value__mutmut_4': xǁFrameǁget_attribute_value__mutmut_4, 
        'xǁFrameǁget_attribute_value__mutmut_5': xǁFrameǁget_attribute_value__mutmut_5, 
        'xǁFrameǁget_attribute_value__mutmut_6': xǁFrameǁget_attribute_value__mutmut_6, 
        'xǁFrameǁget_attribute_value__mutmut_7': xǁFrameǁget_attribute_value__mutmut_7, 
        'xǁFrameǁget_attribute_value__mutmut_8': xǁFrameǁget_attribute_value__mutmut_8, 
        'xǁFrameǁget_attribute_value__mutmut_9': xǁFrameǁget_attribute_value__mutmut_9, 
        'xǁFrameǁget_attribute_value__mutmut_10': xǁFrameǁget_attribute_value__mutmut_10, 
        'xǁFrameǁget_attribute_value__mutmut_11': xǁFrameǁget_attribute_value__mutmut_11, 
        'xǁFrameǁget_attribute_value__mutmut_12': xǁFrameǁget_attribute_value__mutmut_12, 
        'xǁFrameǁget_attribute_value__mutmut_13': xǁFrameǁget_attribute_value__mutmut_13
    }
    
    def get_attribute_value(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameǁget_attribute_value__mutmut_orig"), object.__getattribute__(self, "xǁFrameǁget_attribute_value__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_attribute_value.__signature__ = _mutmut_signature(xǁFrameǁget_attribute_value__mutmut_orig)
    xǁFrameǁget_attribute_value__mutmut_orig.__name__ = 'xǁFrameǁget_attribute_value'

    @property
    def class_name(self) -> str | None:
        return self.get_attribute_value(ATTRIBUTE_MARKER_CLASS_NAME)

    @property
    def has_tracebackhide(self) -> bool:
        """
        Returns whether this frame has a `__tracebackhide__` variable.
        """
        return self.get_attribute_value(ATTRIBUTE_MARKER_TRACEBACKHIDE) == "1"

    def xǁFrameǁself_check__mutmut_orig(self, recursive: bool = True) -> None:
        """
        Checks that the frame is valid.
        """
        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            assert len(self._children) == 0
            # leaf frames have time that isn't attributable to their
            # children, so we don't check that.
            return

        calculated_time = sum(child.time for child in self.children) + self.absorbed_time
        assert math.isclose(
            calculated_time, self.time
        ), f"Frame time mismatch, should be {calculated_time}, was {self.time}, {self.children}"

        if recursive:
            for child in self.children:
                child.self_check(recursive=True)

    def xǁFrameǁself_check__mutmut_1(self, recursive: bool = False) -> None:
        """
        Checks that the frame is valid.
        """
        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            assert len(self._children) == 0
            # leaf frames have time that isn't attributable to their
            # children, so we don't check that.
            return

        calculated_time = sum(child.time for child in self.children) + self.absorbed_time
        assert math.isclose(
            calculated_time, self.time
        ), f"Frame time mismatch, should be {calculated_time}, was {self.time}, {self.children}"

        if recursive:
            for child in self.children:
                child.self_check(recursive=True)

    def xǁFrameǁself_check__mutmut_2(self, recursive: bool = True) -> None:
        """
        Checks that the frame is valid.
        """
        if self.identifier not in SYNTHETIC_LEAF_IDENTIFIERS:
            assert len(self._children) == 0
            # leaf frames have time that isn't attributable to their
            # children, so we don't check that.
            return

        calculated_time = sum(child.time for child in self.children) + self.absorbed_time
        assert math.isclose(
            calculated_time, self.time
        ), f"Frame time mismatch, should be {calculated_time}, was {self.time}, {self.children}"

        if recursive:
            for child in self.children:
                child.self_check(recursive=True)

    def xǁFrameǁself_check__mutmut_3(self, recursive: bool = True) -> None:
        """
        Checks that the frame is valid.
        """
        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            assert len(self._children) != 0
            # leaf frames have time that isn't attributable to their
            # children, so we don't check that.
            return

        calculated_time = sum(child.time for child in self.children) + self.absorbed_time
        assert math.isclose(
            calculated_time, self.time
        ), f"Frame time mismatch, should be {calculated_time}, was {self.time}, {self.children}"

        if recursive:
            for child in self.children:
                child.self_check(recursive=True)

    def xǁFrameǁself_check__mutmut_4(self, recursive: bool = True) -> None:
        """
        Checks that the frame is valid.
        """
        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            assert len(self._children) == 1
            # leaf frames have time that isn't attributable to their
            # children, so we don't check that.
            return

        calculated_time = sum(child.time for child in self.children) + self.absorbed_time
        assert math.isclose(
            calculated_time, self.time
        ), f"Frame time mismatch, should be {calculated_time}, was {self.time}, {self.children}"

        if recursive:
            for child in self.children:
                child.self_check(recursive=True)

    def xǁFrameǁself_check__mutmut_5(self, recursive: bool = True) -> None:
        """
        Checks that the frame is valid.
        """
        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            assert len(self._children) == 0
            # leaf frames have time that isn't attributable to their
            # children, so we don't check that.
            return

        calculated_time = None
        assert math.isclose(
            calculated_time, self.time
        ), f"Frame time mismatch, should be {calculated_time}, was {self.time}, {self.children}"

        if recursive:
            for child in self.children:
                child.self_check(recursive=True)

    def xǁFrameǁself_check__mutmut_6(self, recursive: bool = True) -> None:
        """
        Checks that the frame is valid.
        """
        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            assert len(self._children) == 0
            # leaf frames have time that isn't attributable to their
            # children, so we don't check that.
            return

        calculated_time = sum(child.time for child in self.children) - self.absorbed_time
        assert math.isclose(
            calculated_time, self.time
        ), f"Frame time mismatch, should be {calculated_time}, was {self.time}, {self.children}"

        if recursive:
            for child in self.children:
                child.self_check(recursive=True)

    def xǁFrameǁself_check__mutmut_7(self, recursive: bool = True) -> None:
        """
        Checks that the frame is valid.
        """
        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            assert len(self._children) == 0
            # leaf frames have time that isn't attributable to their
            # children, so we don't check that.
            return

        calculated_time = sum(None) + self.absorbed_time
        assert math.isclose(
            calculated_time, self.time
        ), f"Frame time mismatch, should be {calculated_time}, was {self.time}, {self.children}"

        if recursive:
            for child in self.children:
                child.self_check(recursive=True)

    def xǁFrameǁself_check__mutmut_8(self, recursive: bool = True) -> None:
        """
        Checks that the frame is valid.
        """
        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            assert len(self._children) == 0
            # leaf frames have time that isn't attributable to their
            # children, so we don't check that.
            return

        calculated_time = sum(child.time for child in self.children) + self.absorbed_time
        assert math.isclose(
            None, self.time
        ), f"Frame time mismatch, should be {calculated_time}, was {self.time}, {self.children}"

        if recursive:
            for child in self.children:
                child.self_check(recursive=True)

    def xǁFrameǁself_check__mutmut_9(self, recursive: bool = True) -> None:
        """
        Checks that the frame is valid.
        """
        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            assert len(self._children) == 0
            # leaf frames have time that isn't attributable to their
            # children, so we don't check that.
            return

        calculated_time = sum(child.time for child in self.children) + self.absorbed_time
        assert math.isclose(
            calculated_time, None
        ), f"Frame time mismatch, should be {calculated_time}, was {self.time}, {self.children}"

        if recursive:
            for child in self.children:
                child.self_check(recursive=True)

    def xǁFrameǁself_check__mutmut_10(self, recursive: bool = True) -> None:
        """
        Checks that the frame is valid.
        """
        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            assert len(self._children) == 0
            # leaf frames have time that isn't attributable to their
            # children, so we don't check that.
            return

        calculated_time = sum(child.time for child in self.children) + self.absorbed_time
        assert math.isclose(
            self.time
        ), f"Frame time mismatch, should be {calculated_time}, was {self.time}, {self.children}"

        if recursive:
            for child in self.children:
                child.self_check(recursive=True)

    def xǁFrameǁself_check__mutmut_11(self, recursive: bool = True) -> None:
        """
        Checks that the frame is valid.
        """
        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            assert len(self._children) == 0
            # leaf frames have time that isn't attributable to their
            # children, so we don't check that.
            return

        calculated_time = sum(child.time for child in self.children) + self.absorbed_time
        assert math.isclose(
            calculated_time, ), f"Frame time mismatch, should be {calculated_time}, was {self.time}, {self.children}"

        if recursive:
            for child in self.children:
                child.self_check(recursive=True)

    def xǁFrameǁself_check__mutmut_12(self, recursive: bool = True) -> None:
        """
        Checks that the frame is valid.
        """
        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            assert len(self._children) == 0
            # leaf frames have time that isn't attributable to their
            # children, so we don't check that.
            return

        calculated_time = sum(child.time for child in self.children) + self.absorbed_time
        assert math.isclose(
            calculated_time, self.time
        ), f"Frame time mismatch, should be {calculated_time}, was {self.time}, {self.children}"

        if recursive:
            for child in self.children:
                child.self_check(recursive=None)

    def xǁFrameǁself_check__mutmut_13(self, recursive: bool = True) -> None:
        """
        Checks that the frame is valid.
        """
        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            assert len(self._children) == 0
            # leaf frames have time that isn't attributable to their
            # children, so we don't check that.
            return

        calculated_time = sum(child.time for child in self.children) + self.absorbed_time
        assert math.isclose(
            calculated_time, self.time
        ), f"Frame time mismatch, should be {calculated_time}, was {self.time}, {self.children}"

        if recursive:
            for child in self.children:
                child.self_check(recursive=False)
    
    xǁFrameǁself_check__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameǁself_check__mutmut_1': xǁFrameǁself_check__mutmut_1, 
        'xǁFrameǁself_check__mutmut_2': xǁFrameǁself_check__mutmut_2, 
        'xǁFrameǁself_check__mutmut_3': xǁFrameǁself_check__mutmut_3, 
        'xǁFrameǁself_check__mutmut_4': xǁFrameǁself_check__mutmut_4, 
        'xǁFrameǁself_check__mutmut_5': xǁFrameǁself_check__mutmut_5, 
        'xǁFrameǁself_check__mutmut_6': xǁFrameǁself_check__mutmut_6, 
        'xǁFrameǁself_check__mutmut_7': xǁFrameǁself_check__mutmut_7, 
        'xǁFrameǁself_check__mutmut_8': xǁFrameǁself_check__mutmut_8, 
        'xǁFrameǁself_check__mutmut_9': xǁFrameǁself_check__mutmut_9, 
        'xǁFrameǁself_check__mutmut_10': xǁFrameǁself_check__mutmut_10, 
        'xǁFrameǁself_check__mutmut_11': xǁFrameǁself_check__mutmut_11, 
        'xǁFrameǁself_check__mutmut_12': xǁFrameǁself_check__mutmut_12, 
        'xǁFrameǁself_check__mutmut_13': xǁFrameǁself_check__mutmut_13
    }
    
    def self_check(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameǁself_check__mutmut_orig"), object.__getattribute__(self, "xǁFrameǁself_check__mutmut_mutants"), args, kwargs, self)
        return result 
    
    self_check.__signature__ = _mutmut_signature(xǁFrameǁself_check__mutmut_orig)
    xǁFrameǁself_check__mutmut_orig.__name__ = 'xǁFrameǁself_check'

    def xǁFrameǁ__repr____mutmut_orig(self):
        return "Frame(identifier=%s, time=%f, len(children)=%d), group=%r" % (
            self.identifier,
            self.time,
            len(self.children),
            self.group,
        )

    def xǁFrameǁ__repr____mutmut_1(self):
        return "Frame(identifier=%s, time=%f, len(children)=%d), group=%r" / (
            self.identifier,
            self.time,
            len(self.children),
            self.group,
        )

    def xǁFrameǁ__repr____mutmut_2(self):
        return "XXFrame(identifier=%s, time=%f, len(children)=%d), group=%rXX" % (
            self.identifier,
            self.time,
            len(self.children),
            self.group,
        )

    def xǁFrameǁ__repr____mutmut_3(self):
        return "frame(identifier=%s, time=%f, len(children)=%d), group=%r" % (
            self.identifier,
            self.time,
            len(self.children),
            self.group,
        )

    def xǁFrameǁ__repr____mutmut_4(self):
        return "FRAME(IDENTIFIER=%S, TIME=%F, LEN(CHILDREN)=%D), GROUP=%R" % (
            self.identifier,
            self.time,
            len(self.children),
            self.group,
        )
    
    xǁFrameǁ__repr____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameǁ__repr____mutmut_1': xǁFrameǁ__repr____mutmut_1, 
        'xǁFrameǁ__repr____mutmut_2': xǁFrameǁ__repr____mutmut_2, 
        'xǁFrameǁ__repr____mutmut_3': xǁFrameǁ__repr____mutmut_3, 
        'xǁFrameǁ__repr____mutmut_4': xǁFrameǁ__repr____mutmut_4
    }
    
    def __repr__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameǁ__repr____mutmut_orig"), object.__getattribute__(self, "xǁFrameǁ__repr____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __repr__.__signature__ = _mutmut_signature(xǁFrameǁ__repr____mutmut_orig)
    xǁFrameǁ__repr____mutmut_orig.__name__ = 'xǁFrameǁ__repr__'

    def xǁFrameǁto_json_str__mutmut_orig(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_1(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = None  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_2(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(None, json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_3(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], None)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_4(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_5(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], )  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_6(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = None
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_7(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append(None)
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_8(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' / encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_9(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('XX"identifier": %sXX' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_10(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"IDENTIFIER": %S' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_11(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(None))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_12(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append(None)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_13(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' / self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_14(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('XX"time": %fXX' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_15(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"TIME": %F' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_16(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append(None)
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_17(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' / json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_18(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('XX"attributes": %sXX' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_19(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"ATTRIBUTES": %S' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_20(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(None))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_21(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = None
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_22(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(None)
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_23(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append(None)

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_24(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' / ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_25(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('XX"children": [%s]XX' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_26(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"CHILDREN": [%S]' % ",".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_27(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(None))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_28(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % "XX,XX".join(child_jsons))

        return "{%s}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_29(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" / ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_30(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "XX{%s}XX" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_31(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%S}" % ",".join(property_decls)

    def xǁFrameǁto_json_str__mutmut_32(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % ",".join(None)

    def xǁFrameǁto_json_str__mutmut_33(self):
        # method that converts this object into a JSON string. Uses an inline
        # technique because the json module uses 2x stack frames, so we'd get
        # a RecursionError on deep stacks.
        encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore

        property_decls: list[str] = []
        property_decls.append('"identifier": %s' % encode_str(self.identifier))
        property_decls.append('"time": %f' % self.time)
        property_decls.append('"attributes": %s' % json.dumps(self.attributes))
        child_jsons: list[str] = []
        for child in self.children:
            child_jsons.append(child.to_json_str())
        property_decls.append('"children": [%s]' % ",".join(child_jsons))

        return "{%s}" % "XX,XX".join(property_decls)
    
    xǁFrameǁto_json_str__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameǁto_json_str__mutmut_1': xǁFrameǁto_json_str__mutmut_1, 
        'xǁFrameǁto_json_str__mutmut_2': xǁFrameǁto_json_str__mutmut_2, 
        'xǁFrameǁto_json_str__mutmut_3': xǁFrameǁto_json_str__mutmut_3, 
        'xǁFrameǁto_json_str__mutmut_4': xǁFrameǁto_json_str__mutmut_4, 
        'xǁFrameǁto_json_str__mutmut_5': xǁFrameǁto_json_str__mutmut_5, 
        'xǁFrameǁto_json_str__mutmut_6': xǁFrameǁto_json_str__mutmut_6, 
        'xǁFrameǁto_json_str__mutmut_7': xǁFrameǁto_json_str__mutmut_7, 
        'xǁFrameǁto_json_str__mutmut_8': xǁFrameǁto_json_str__mutmut_8, 
        'xǁFrameǁto_json_str__mutmut_9': xǁFrameǁto_json_str__mutmut_9, 
        'xǁFrameǁto_json_str__mutmut_10': xǁFrameǁto_json_str__mutmut_10, 
        'xǁFrameǁto_json_str__mutmut_11': xǁFrameǁto_json_str__mutmut_11, 
        'xǁFrameǁto_json_str__mutmut_12': xǁFrameǁto_json_str__mutmut_12, 
        'xǁFrameǁto_json_str__mutmut_13': xǁFrameǁto_json_str__mutmut_13, 
        'xǁFrameǁto_json_str__mutmut_14': xǁFrameǁto_json_str__mutmut_14, 
        'xǁFrameǁto_json_str__mutmut_15': xǁFrameǁto_json_str__mutmut_15, 
        'xǁFrameǁto_json_str__mutmut_16': xǁFrameǁto_json_str__mutmut_16, 
        'xǁFrameǁto_json_str__mutmut_17': xǁFrameǁto_json_str__mutmut_17, 
        'xǁFrameǁto_json_str__mutmut_18': xǁFrameǁto_json_str__mutmut_18, 
        'xǁFrameǁto_json_str__mutmut_19': xǁFrameǁto_json_str__mutmut_19, 
        'xǁFrameǁto_json_str__mutmut_20': xǁFrameǁto_json_str__mutmut_20, 
        'xǁFrameǁto_json_str__mutmut_21': xǁFrameǁto_json_str__mutmut_21, 
        'xǁFrameǁto_json_str__mutmut_22': xǁFrameǁto_json_str__mutmut_22, 
        'xǁFrameǁto_json_str__mutmut_23': xǁFrameǁto_json_str__mutmut_23, 
        'xǁFrameǁto_json_str__mutmut_24': xǁFrameǁto_json_str__mutmut_24, 
        'xǁFrameǁto_json_str__mutmut_25': xǁFrameǁto_json_str__mutmut_25, 
        'xǁFrameǁto_json_str__mutmut_26': xǁFrameǁto_json_str__mutmut_26, 
        'xǁFrameǁto_json_str__mutmut_27': xǁFrameǁto_json_str__mutmut_27, 
        'xǁFrameǁto_json_str__mutmut_28': xǁFrameǁto_json_str__mutmut_28, 
        'xǁFrameǁto_json_str__mutmut_29': xǁFrameǁto_json_str__mutmut_29, 
        'xǁFrameǁto_json_str__mutmut_30': xǁFrameǁto_json_str__mutmut_30, 
        'xǁFrameǁto_json_str__mutmut_31': xǁFrameǁto_json_str__mutmut_31, 
        'xǁFrameǁto_json_str__mutmut_32': xǁFrameǁto_json_str__mutmut_32, 
        'xǁFrameǁto_json_str__mutmut_33': xǁFrameǁto_json_str__mutmut_33
    }
    
    def to_json_str(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameǁto_json_str__mutmut_orig"), object.__getattribute__(self, "xǁFrameǁto_json_str__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_json_str.__signature__ = _mutmut_signature(xǁFrameǁto_json_str__mutmut_orig)
    xǁFrameǁto_json_str__mutmut_orig.__name__ = 'xǁFrameǁto_json_str'


class FrameGroup:
    _frames: list[Frame]
    _exit_frames: list[Frame] | None

    def xǁFrameGroupǁ__init____mutmut_orig(self, root: Frame):
        self.root = root
        self.id = str(uuid.uuid4())
        self._frames = []
        self._exit_frames = None

        self.add_frame(root)

    def xǁFrameGroupǁ__init____mutmut_1(self, root: Frame):
        self.root = None
        self.id = str(uuid.uuid4())
        self._frames = []
        self._exit_frames = None

        self.add_frame(root)

    def xǁFrameGroupǁ__init____mutmut_2(self, root: Frame):
        self.root = root
        self.id = None
        self._frames = []
        self._exit_frames = None

        self.add_frame(root)

    def xǁFrameGroupǁ__init____mutmut_3(self, root: Frame):
        self.root = root
        self.id = str(None)
        self._frames = []
        self._exit_frames = None

        self.add_frame(root)

    def xǁFrameGroupǁ__init____mutmut_4(self, root: Frame):
        self.root = root
        self.id = str(uuid.uuid4())
        self._frames = None
        self._exit_frames = None

        self.add_frame(root)

    def xǁFrameGroupǁ__init____mutmut_5(self, root: Frame):
        self.root = root
        self.id = str(uuid.uuid4())
        self._frames = []
        self._exit_frames = ""

        self.add_frame(root)

    def xǁFrameGroupǁ__init____mutmut_6(self, root: Frame):
        self.root = root
        self.id = str(uuid.uuid4())
        self._frames = []
        self._exit_frames = None

        self.add_frame(None)
    
    xǁFrameGroupǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameGroupǁ__init____mutmut_1': xǁFrameGroupǁ__init____mutmut_1, 
        'xǁFrameGroupǁ__init____mutmut_2': xǁFrameGroupǁ__init____mutmut_2, 
        'xǁFrameGroupǁ__init____mutmut_3': xǁFrameGroupǁ__init____mutmut_3, 
        'xǁFrameGroupǁ__init____mutmut_4': xǁFrameGroupǁ__init____mutmut_4, 
        'xǁFrameGroupǁ__init____mutmut_5': xǁFrameGroupǁ__init____mutmut_5, 
        'xǁFrameGroupǁ__init____mutmut_6': xǁFrameGroupǁ__init____mutmut_6
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameGroupǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFrameGroupǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁFrameGroupǁ__init____mutmut_orig)
    xǁFrameGroupǁ__init____mutmut_orig.__name__ = 'xǁFrameGroupǁ__init__'

    @property
    def frames(self) -> Sequence[Frame]:
        return tuple(self._frames)

    def xǁFrameGroupǁadd_frame__mutmut_orig(self, frame: Frame):
        if frame.group:
            frame.group.remove_frame(frame)

        self._frames.append(frame)
        frame.group = self

    def xǁFrameGroupǁadd_frame__mutmut_1(self, frame: Frame):
        if frame.group:
            frame.group.remove_frame(None)

        self._frames.append(frame)
        frame.group = self

    def xǁFrameGroupǁadd_frame__mutmut_2(self, frame: Frame):
        if frame.group:
            frame.group.remove_frame(frame)

        self._frames.append(None)
        frame.group = self

    def xǁFrameGroupǁadd_frame__mutmut_3(self, frame: Frame):
        if frame.group:
            frame.group.remove_frame(frame)

        self._frames.append(frame)
        frame.group = None
    
    xǁFrameGroupǁadd_frame__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameGroupǁadd_frame__mutmut_1': xǁFrameGroupǁadd_frame__mutmut_1, 
        'xǁFrameGroupǁadd_frame__mutmut_2': xǁFrameGroupǁadd_frame__mutmut_2, 
        'xǁFrameGroupǁadd_frame__mutmut_3': xǁFrameGroupǁadd_frame__mutmut_3
    }
    
    def add_frame(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameGroupǁadd_frame__mutmut_orig"), object.__getattribute__(self, "xǁFrameGroupǁadd_frame__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_frame.__signature__ = _mutmut_signature(xǁFrameGroupǁadd_frame__mutmut_orig)
    xǁFrameGroupǁadd_frame__mutmut_orig.__name__ = 'xǁFrameGroupǁadd_frame'

    def xǁFrameGroupǁremove_frame__mutmut_orig(self, frame: Frame):
        assert frame.group is self
        self._frames.remove(frame)
        frame.group = None

    def xǁFrameGroupǁremove_frame__mutmut_1(self, frame: Frame):
        assert frame.group is not self
        self._frames.remove(frame)
        frame.group = None

    def xǁFrameGroupǁremove_frame__mutmut_2(self, frame: Frame):
        assert frame.group is self
        self._frames.remove(None)
        frame.group = None

    def xǁFrameGroupǁremove_frame__mutmut_3(self, frame: Frame):
        assert frame.group is self
        self._frames.remove(frame)
        frame.group = ""
    
    xǁFrameGroupǁremove_frame__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameGroupǁremove_frame__mutmut_1': xǁFrameGroupǁremove_frame__mutmut_1, 
        'xǁFrameGroupǁremove_frame__mutmut_2': xǁFrameGroupǁremove_frame__mutmut_2, 
        'xǁFrameGroupǁremove_frame__mutmut_3': xǁFrameGroupǁremove_frame__mutmut_3
    }
    
    def remove_frame(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameGroupǁremove_frame__mutmut_orig"), object.__getattribute__(self, "xǁFrameGroupǁremove_frame__mutmut_mutants"), args, kwargs, self)
        return result 
    
    remove_frame.__signature__ = _mutmut_signature(xǁFrameGroupǁremove_frame__mutmut_orig)
    xǁFrameGroupǁremove_frame__mutmut_orig.__name__ = 'xǁFrameGroupǁremove_frame'

    @property
    def exit_frames(self):
        """
        Returns a list of frames whose children include a frame outside of the group
        """
        if self._exit_frames is None:
            exit_frames: list[Frame] = []
            for frame in self.frames:
                if any(c.group != self for c in frame.children):
                    exit_frames.append(frame)
            self._exit_frames = exit_frames

        return self._exit_frames

    def xǁFrameGroupǁ__repr____mutmut_orig(self):
        return "FrameGroup(len(frames)=%d)" % len(self.frames)

    def xǁFrameGroupǁ__repr____mutmut_1(self):
        return "FrameGroup(len(frames)=%d)" / len(self.frames)

    def xǁFrameGroupǁ__repr____mutmut_2(self):
        return "XXFrameGroup(len(frames)=%d)XX" % len(self.frames)

    def xǁFrameGroupǁ__repr____mutmut_3(self):
        return "framegroup(len(frames)=%d)" % len(self.frames)

    def xǁFrameGroupǁ__repr____mutmut_4(self):
        return "FRAMEGROUP(LEN(FRAMES)=%D)" % len(self.frames)
    
    xǁFrameGroupǁ__repr____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameGroupǁ__repr____mutmut_1': xǁFrameGroupǁ__repr____mutmut_1, 
        'xǁFrameGroupǁ__repr____mutmut_2': xǁFrameGroupǁ__repr____mutmut_2, 
        'xǁFrameGroupǁ__repr____mutmut_3': xǁFrameGroupǁ__repr____mutmut_3, 
        'xǁFrameGroupǁ__repr____mutmut_4': xǁFrameGroupǁ__repr____mutmut_4
    }
    
    def __repr__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameGroupǁ__repr____mutmut_orig"), object.__getattribute__(self, "xǁFrameGroupǁ__repr____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __repr__.__signature__ = _mutmut_signature(xǁFrameGroupǁ__repr____mutmut_orig)
    xǁFrameGroupǁ__repr____mutmut_orig.__name__ = 'xǁFrameGroupǁ__repr__'
