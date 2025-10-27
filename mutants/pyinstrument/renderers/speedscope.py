from __future__ import annotations

import json
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Union

from pyinstrument import processors
from pyinstrument.frame import Frame
from pyinstrument.renderers.base import FrameRenderer, ProcessorList
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

# pyright: strict


@dataclass(frozen=True, eq=True)
class SpeedscopeFrame:
    """
    Data class to store data needed for speedscope's concept of a
    frame, hereafter referred to as a "speedscope frame", as opposed to
    a "pyinstrument frame". This type must be hashable in order to use
    it as a dictionary key; a dictionary will be used to track unique
    speedscope frames.
    """

    name: str | None
    file: str | None
    line: int | None


class SpeedscopeEventType(Enum):
    """Enum representing the only two types of speedscope frame events"""

    OPEN = "O"
    CLOSE = "C"


@dataclass
class SpeedscopeEvent:
    """
    Data class to store speedscope's concept of an "event", which
    corresponds to opening or closing stack frames as functions or
    methods are entered or exited.
    """

    type: SpeedscopeEventType
    at: float
    frame: int


@dataclass
class SpeedscopeProfile:
    """
    Data class to store speedscope's concept of a "profile".
    """

    name: str
    events: list[SpeedscopeEvent]
    end_value: float
    start_value: float = 0.0
    type: str = "evented"
    unit: str = "seconds"


@dataclass
class SpeedscopeFile:
    """
    Data class encoding fields in speedscope's JSON file schema
    """

    name: str
    profiles: list[SpeedscopeProfile]
    shared: dict[str, list[SpeedscopeFrame]]
    schema: str = "https://www.speedscope.app/file-format-schema.json"
    active_profile_index: None = None
    exporter: str = "pyinstrument"


SpeedscopeFrameDictType = Dict[str, Union[str, int, None]]
SpeedscopeEventDictType = Dict[str, Union[SpeedscopeEventType, float, int]]


class SpeedscopeEncoder(json.JSONEncoder):
    """
    Encoder class used by json.dumps to serialize the various
    speedscope data classes.
    """

    def xǁSpeedscopeEncoderǁdefault__mutmut_orig(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_1(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "XX$schemaXX": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_2(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$SCHEMA": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_3(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "XXnameXX": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_4(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "NAME": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_5(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "XXactiveProfileIndexXX": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_6(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeprofileindex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_7(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "ACTIVEPROFILEINDEX": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_8(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "XXexporterXX": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_9(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "EXPORTER": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_10(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "XXprofilesXX": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_11(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "PROFILES": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_12(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "XXsharedXX": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_13(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "SHARED": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_14(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "XXtypeXX": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_15(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "TYPE": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_16(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "XXnameXX": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_17(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "NAME": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_18(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "XXunitXX": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_19(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "UNIT": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_20(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "XXstartValueXX": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_21(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startvalue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_22(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "STARTVALUE": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_23(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "XXendValueXX": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_24(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endvalue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_25(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "ENDVALUE": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_26(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "XXeventsXX": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_27(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "EVENTS": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_28(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = None
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_29(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(None, o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_30(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, None)

    def xǁSpeedscopeEncoderǁdefault__mutmut_31(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(o)

    def xǁSpeedscopeEncoderǁdefault__mutmut_32(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFile):
            return {
                "$schema": o.schema,
                "name": o.name,
                "activeProfileIndex": o.active_profile_index,
                "exporter": o.exporter,
                "profiles": o.profiles,
                "shared": o.shared,
            }
        if isinstance(o, SpeedscopeProfile):
            return {
                "type": o.type,
                "name": o.name,
                "unit": o.unit,
                "startValue": o.start_value,
                "endValue": o.end_value,
                "events": o.events,
            }
        if isinstance(o, (SpeedscopeFrame, SpeedscopeEvent)):
            d: SpeedscopeFrameDictType | SpeedscopeEventDictType = o.__dict__
            return d
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, )
    
    xǁSpeedscopeEncoderǁdefault__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSpeedscopeEncoderǁdefault__mutmut_1': xǁSpeedscopeEncoderǁdefault__mutmut_1, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_2': xǁSpeedscopeEncoderǁdefault__mutmut_2, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_3': xǁSpeedscopeEncoderǁdefault__mutmut_3, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_4': xǁSpeedscopeEncoderǁdefault__mutmut_4, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_5': xǁSpeedscopeEncoderǁdefault__mutmut_5, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_6': xǁSpeedscopeEncoderǁdefault__mutmut_6, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_7': xǁSpeedscopeEncoderǁdefault__mutmut_7, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_8': xǁSpeedscopeEncoderǁdefault__mutmut_8, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_9': xǁSpeedscopeEncoderǁdefault__mutmut_9, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_10': xǁSpeedscopeEncoderǁdefault__mutmut_10, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_11': xǁSpeedscopeEncoderǁdefault__mutmut_11, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_12': xǁSpeedscopeEncoderǁdefault__mutmut_12, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_13': xǁSpeedscopeEncoderǁdefault__mutmut_13, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_14': xǁSpeedscopeEncoderǁdefault__mutmut_14, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_15': xǁSpeedscopeEncoderǁdefault__mutmut_15, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_16': xǁSpeedscopeEncoderǁdefault__mutmut_16, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_17': xǁSpeedscopeEncoderǁdefault__mutmut_17, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_18': xǁSpeedscopeEncoderǁdefault__mutmut_18, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_19': xǁSpeedscopeEncoderǁdefault__mutmut_19, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_20': xǁSpeedscopeEncoderǁdefault__mutmut_20, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_21': xǁSpeedscopeEncoderǁdefault__mutmut_21, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_22': xǁSpeedscopeEncoderǁdefault__mutmut_22, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_23': xǁSpeedscopeEncoderǁdefault__mutmut_23, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_24': xǁSpeedscopeEncoderǁdefault__mutmut_24, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_25': xǁSpeedscopeEncoderǁdefault__mutmut_25, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_26': xǁSpeedscopeEncoderǁdefault__mutmut_26, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_27': xǁSpeedscopeEncoderǁdefault__mutmut_27, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_28': xǁSpeedscopeEncoderǁdefault__mutmut_28, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_29': xǁSpeedscopeEncoderǁdefault__mutmut_29, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_30': xǁSpeedscopeEncoderǁdefault__mutmut_30, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_31': xǁSpeedscopeEncoderǁdefault__mutmut_31, 
        'xǁSpeedscopeEncoderǁdefault__mutmut_32': xǁSpeedscopeEncoderǁdefault__mutmut_32
    }
    
    def default(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSpeedscopeEncoderǁdefault__mutmut_orig"), object.__getattribute__(self, "xǁSpeedscopeEncoderǁdefault__mutmut_mutants"), args, kwargs, self)
        return result 
    
    default.__signature__ = _mutmut_signature(xǁSpeedscopeEncoderǁdefault__mutmut_orig)
    xǁSpeedscopeEncoderǁdefault__mutmut_orig.__name__ = 'xǁSpeedscopeEncoderǁdefault'


class SpeedscopeRenderer(FrameRenderer):
    """
    Outputs a tree of JSON conforming to the speedscope schema documented at

    wiki: https://github.com/jlfwong/speedscope/wiki/Importing-from-custom-sources
    schema: https://www.speedscope.app/file-format-schema.json
    spec: https://github.com/jlfwong/speedscope/blob/main/src/lib/file-format-spec.ts
    example: https://github.com/jlfwong/speedscope/blob/main/sample/profiles/speedscope/0.0.1/simple.speedscope.json

    """

    output_file_extension = "speedscope.json"

    def xǁSpeedscopeRendererǁ__init____mutmut_orig(self, **kwargs: Any):
        super().__init__(**kwargs)

        # Member holding a running total of wall clock time needed to
        # compute the times at which events occur
        self._event_time: float = 0.0

        # Map of speedscope frames to speedscope frame indices, needed
        # to construct evented speedscope profiles; exploits LIFO
        # property of popinfo method in Python 3.7+ dictionaries. This
        # dictionary is used to build up the "shared" JSON array in
        # speedscope's schema.
        self._frame_to_index: dict[SpeedscopeFrame, int] = {}

    def xǁSpeedscopeRendererǁ__init____mutmut_1(self, **kwargs: Any):
        super().__init__(**kwargs)

        # Member holding a running total of wall clock time needed to
        # compute the times at which events occur
        self._event_time: float = None

        # Map of speedscope frames to speedscope frame indices, needed
        # to construct evented speedscope profiles; exploits LIFO
        # property of popinfo method in Python 3.7+ dictionaries. This
        # dictionary is used to build up the "shared" JSON array in
        # speedscope's schema.
        self._frame_to_index: dict[SpeedscopeFrame, int] = {}

    def xǁSpeedscopeRendererǁ__init____mutmut_2(self, **kwargs: Any):
        super().__init__(**kwargs)

        # Member holding a running total of wall clock time needed to
        # compute the times at which events occur
        self._event_time: float = 1.0

        # Map of speedscope frames to speedscope frame indices, needed
        # to construct evented speedscope profiles; exploits LIFO
        # property of popinfo method in Python 3.7+ dictionaries. This
        # dictionary is used to build up the "shared" JSON array in
        # speedscope's schema.
        self._frame_to_index: dict[SpeedscopeFrame, int] = {}

    def xǁSpeedscopeRendererǁ__init____mutmut_3(self, **kwargs: Any):
        super().__init__(**kwargs)

        # Member holding a running total of wall clock time needed to
        # compute the times at which events occur
        self._event_time: float = 0.0

        # Map of speedscope frames to speedscope frame indices, needed
        # to construct evented speedscope profiles; exploits LIFO
        # property of popinfo method in Python 3.7+ dictionaries. This
        # dictionary is used to build up the "shared" JSON array in
        # speedscope's schema.
        self._frame_to_index: dict[SpeedscopeFrame, int] = None
    
    xǁSpeedscopeRendererǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSpeedscopeRendererǁ__init____mutmut_1': xǁSpeedscopeRendererǁ__init____mutmut_1, 
        'xǁSpeedscopeRendererǁ__init____mutmut_2': xǁSpeedscopeRendererǁ__init____mutmut_2, 
        'xǁSpeedscopeRendererǁ__init____mutmut_3': xǁSpeedscopeRendererǁ__init____mutmut_3
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSpeedscopeRendererǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSpeedscopeRendererǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSpeedscopeRendererǁ__init____mutmut_orig)
    xǁSpeedscopeRendererǁ__init____mutmut_orig.__name__ = 'xǁSpeedscopeRendererǁ__init__'

    def xǁSpeedscopeRendererǁrender_frame__mutmut_orig(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_1(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is not None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_2(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = None
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_3(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(None, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_4(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, None, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_5(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, None)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_6(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_7(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_8(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, )
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_9(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_10(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = None

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_11(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = None
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_12(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = None
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_13(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(None, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_14(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, None, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_15(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, None)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_16(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_17(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_18(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, )
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_19(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = None

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_20(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(None)

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_21(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(None))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_22(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time = frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_23(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time -= frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_24(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time = frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_25(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time -= frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_26(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = None
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_27(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(None, self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_28(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, None, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_29(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, None)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_30(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(self._event_time, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_31(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, sframe_index)
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_32(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, )
        events_array.append(close_event)

        return events_array

    def xǁSpeedscopeRendererǁrender_frame__mutmut_33(self, frame: Frame | None) -> list[SpeedscopeEvent]:
        """
        Builds up a list of speedscope events that are used to populate the
        "events" array in speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return []

        # Otherwise, form a speedscope frame and add it to the frame
        # to index map if the frame is not already a key in that map.
        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        # Get the frame index and add a speedscope event corresponding
        # to opening a stack frame.
        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(SpeedscopeEventType.OPEN, self._event_time, sframe_index)
        events_array: list[SpeedscopeEvent] = [open_event]

        # Add stack frame open and close events for all child frames
        # of this frame.
        for child in frame.children:
            events_array.extend(self.render_frame(child))

        # Update event time for closing this stack frame.
        #
        # If number of frames approaches 1e16 * desired accuracy
        # level, consider using Neumaier-Kahan summation; improves
        # worst-case relative accuracy of sum from O(num_summands *
        # eps) to (2 * eps + O(num_summands * eps * eps)), where eps
        # is IEEE-754 double precision unit roundoff, approximately
        # 1e-16. Average case relative accuracy expressions replace
        # num_summands with sqrt(num_summands). However, Kahan
        # summation quadruples operation count of sum, and Neumaier
        # variant also adds a branch & swap for each summand. Pairwise
        # summation isn't an option here because a running total is
        # needed.

        self._event_time += frame.absorbed_time
        if frame.is_synthetic_leaf:
            # only time contained within leaf nodes is real time i.e. not the sum of children
            self._event_time += frame.time

        # Add event closing this stack frame.
        close_event = SpeedscopeEvent(SpeedscopeEventType.CLOSE, self._event_time, sframe_index)
        events_array.append(None)

        return events_array
    
    xǁSpeedscopeRendererǁrender_frame__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSpeedscopeRendererǁrender_frame__mutmut_1': xǁSpeedscopeRendererǁrender_frame__mutmut_1, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_2': xǁSpeedscopeRendererǁrender_frame__mutmut_2, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_3': xǁSpeedscopeRendererǁrender_frame__mutmut_3, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_4': xǁSpeedscopeRendererǁrender_frame__mutmut_4, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_5': xǁSpeedscopeRendererǁrender_frame__mutmut_5, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_6': xǁSpeedscopeRendererǁrender_frame__mutmut_6, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_7': xǁSpeedscopeRendererǁrender_frame__mutmut_7, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_8': xǁSpeedscopeRendererǁrender_frame__mutmut_8, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_9': xǁSpeedscopeRendererǁrender_frame__mutmut_9, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_10': xǁSpeedscopeRendererǁrender_frame__mutmut_10, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_11': xǁSpeedscopeRendererǁrender_frame__mutmut_11, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_12': xǁSpeedscopeRendererǁrender_frame__mutmut_12, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_13': xǁSpeedscopeRendererǁrender_frame__mutmut_13, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_14': xǁSpeedscopeRendererǁrender_frame__mutmut_14, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_15': xǁSpeedscopeRendererǁrender_frame__mutmut_15, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_16': xǁSpeedscopeRendererǁrender_frame__mutmut_16, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_17': xǁSpeedscopeRendererǁrender_frame__mutmut_17, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_18': xǁSpeedscopeRendererǁrender_frame__mutmut_18, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_19': xǁSpeedscopeRendererǁrender_frame__mutmut_19, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_20': xǁSpeedscopeRendererǁrender_frame__mutmut_20, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_21': xǁSpeedscopeRendererǁrender_frame__mutmut_21, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_22': xǁSpeedscopeRendererǁrender_frame__mutmut_22, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_23': xǁSpeedscopeRendererǁrender_frame__mutmut_23, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_24': xǁSpeedscopeRendererǁrender_frame__mutmut_24, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_25': xǁSpeedscopeRendererǁrender_frame__mutmut_25, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_26': xǁSpeedscopeRendererǁrender_frame__mutmut_26, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_27': xǁSpeedscopeRendererǁrender_frame__mutmut_27, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_28': xǁSpeedscopeRendererǁrender_frame__mutmut_28, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_29': xǁSpeedscopeRendererǁrender_frame__mutmut_29, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_30': xǁSpeedscopeRendererǁrender_frame__mutmut_30, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_31': xǁSpeedscopeRendererǁrender_frame__mutmut_31, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_32': xǁSpeedscopeRendererǁrender_frame__mutmut_32, 
        'xǁSpeedscopeRendererǁrender_frame__mutmut_33': xǁSpeedscopeRendererǁrender_frame__mutmut_33
    }
    
    def render_frame(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSpeedscopeRendererǁrender_frame__mutmut_orig"), object.__getattribute__(self, "xǁSpeedscopeRendererǁrender_frame__mutmut_mutants"), args, kwargs, self)
        return result 
    
    render_frame.__signature__ = _mutmut_signature(xǁSpeedscopeRendererǁrender_frame__mutmut_orig)
    xǁSpeedscopeRendererǁrender_frame__mutmut_orig.__name__ = 'xǁSpeedscopeRendererǁrender_frame'

    def xǁSpeedscopeRendererǁrender__mutmut_orig(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_1(self, session: Session):
        frame = None

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_2(self, session: Session):
        frame = self.preprocess(None)

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_3(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = None
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_4(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime(None, time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_5(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", None)
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_6(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime(time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_7(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", )
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_8(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("XX%Y-%m-%dT%H-%M-%SXX", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_9(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%y-%m-%dt%h-%m-%s", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_10(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%M-%DT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_11(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(None))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_12(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = None

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_13(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = None

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_14(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(None, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_15(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, None, session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_16(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), None)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_17(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_18(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_19(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), )
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_20(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(None), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_21(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = None

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_22(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(None)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_23(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = None
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_24(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"XXframesXX": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_25(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"FRAMES": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_26(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = None

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_27(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(None, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_28(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, None, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_29(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, None)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_30(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_31(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_32(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, )

        return "%s\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_33(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" / json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_34(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "XX%s\nXX" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_35(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%S\n" % json.dumps(speedscope_file, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_36(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(None, cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_37(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, cls=None)

    def xǁSpeedscopeRendererǁrender__mutmut_38(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(cls=SpeedscopeEncoder)

    def xǁSpeedscopeRendererǁrender__mutmut_39(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for '{session.target_description}' at {id_}"

        sprofile_list: list[SpeedscopeProfile] = [
            SpeedscopeProfile(name, self.render_frame(frame), session.duration)
        ]

        # Exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order to build the list of speedscope
        # frames.
        sframe_list: list[SpeedscopeFrame] = [sframe for sframe in iter(self._frame_to_index)]

        shared_dict = {"frames": sframe_list}
        speedscope_file = SpeedscopeFile(name, sprofile_list, shared_dict)

        return "%s\n" % json.dumps(speedscope_file, )
    
    xǁSpeedscopeRendererǁrender__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSpeedscopeRendererǁrender__mutmut_1': xǁSpeedscopeRendererǁrender__mutmut_1, 
        'xǁSpeedscopeRendererǁrender__mutmut_2': xǁSpeedscopeRendererǁrender__mutmut_2, 
        'xǁSpeedscopeRendererǁrender__mutmut_3': xǁSpeedscopeRendererǁrender__mutmut_3, 
        'xǁSpeedscopeRendererǁrender__mutmut_4': xǁSpeedscopeRendererǁrender__mutmut_4, 
        'xǁSpeedscopeRendererǁrender__mutmut_5': xǁSpeedscopeRendererǁrender__mutmut_5, 
        'xǁSpeedscopeRendererǁrender__mutmut_6': xǁSpeedscopeRendererǁrender__mutmut_6, 
        'xǁSpeedscopeRendererǁrender__mutmut_7': xǁSpeedscopeRendererǁrender__mutmut_7, 
        'xǁSpeedscopeRendererǁrender__mutmut_8': xǁSpeedscopeRendererǁrender__mutmut_8, 
        'xǁSpeedscopeRendererǁrender__mutmut_9': xǁSpeedscopeRendererǁrender__mutmut_9, 
        'xǁSpeedscopeRendererǁrender__mutmut_10': xǁSpeedscopeRendererǁrender__mutmut_10, 
        'xǁSpeedscopeRendererǁrender__mutmut_11': xǁSpeedscopeRendererǁrender__mutmut_11, 
        'xǁSpeedscopeRendererǁrender__mutmut_12': xǁSpeedscopeRendererǁrender__mutmut_12, 
        'xǁSpeedscopeRendererǁrender__mutmut_13': xǁSpeedscopeRendererǁrender__mutmut_13, 
        'xǁSpeedscopeRendererǁrender__mutmut_14': xǁSpeedscopeRendererǁrender__mutmut_14, 
        'xǁSpeedscopeRendererǁrender__mutmut_15': xǁSpeedscopeRendererǁrender__mutmut_15, 
        'xǁSpeedscopeRendererǁrender__mutmut_16': xǁSpeedscopeRendererǁrender__mutmut_16, 
        'xǁSpeedscopeRendererǁrender__mutmut_17': xǁSpeedscopeRendererǁrender__mutmut_17, 
        'xǁSpeedscopeRendererǁrender__mutmut_18': xǁSpeedscopeRendererǁrender__mutmut_18, 
        'xǁSpeedscopeRendererǁrender__mutmut_19': xǁSpeedscopeRendererǁrender__mutmut_19, 
        'xǁSpeedscopeRendererǁrender__mutmut_20': xǁSpeedscopeRendererǁrender__mutmut_20, 
        'xǁSpeedscopeRendererǁrender__mutmut_21': xǁSpeedscopeRendererǁrender__mutmut_21, 
        'xǁSpeedscopeRendererǁrender__mutmut_22': xǁSpeedscopeRendererǁrender__mutmut_22, 
        'xǁSpeedscopeRendererǁrender__mutmut_23': xǁSpeedscopeRendererǁrender__mutmut_23, 
        'xǁSpeedscopeRendererǁrender__mutmut_24': xǁSpeedscopeRendererǁrender__mutmut_24, 
        'xǁSpeedscopeRendererǁrender__mutmut_25': xǁSpeedscopeRendererǁrender__mutmut_25, 
        'xǁSpeedscopeRendererǁrender__mutmut_26': xǁSpeedscopeRendererǁrender__mutmut_26, 
        'xǁSpeedscopeRendererǁrender__mutmut_27': xǁSpeedscopeRendererǁrender__mutmut_27, 
        'xǁSpeedscopeRendererǁrender__mutmut_28': xǁSpeedscopeRendererǁrender__mutmut_28, 
        'xǁSpeedscopeRendererǁrender__mutmut_29': xǁSpeedscopeRendererǁrender__mutmut_29, 
        'xǁSpeedscopeRendererǁrender__mutmut_30': xǁSpeedscopeRendererǁrender__mutmut_30, 
        'xǁSpeedscopeRendererǁrender__mutmut_31': xǁSpeedscopeRendererǁrender__mutmut_31, 
        'xǁSpeedscopeRendererǁrender__mutmut_32': xǁSpeedscopeRendererǁrender__mutmut_32, 
        'xǁSpeedscopeRendererǁrender__mutmut_33': xǁSpeedscopeRendererǁrender__mutmut_33, 
        'xǁSpeedscopeRendererǁrender__mutmut_34': xǁSpeedscopeRendererǁrender__mutmut_34, 
        'xǁSpeedscopeRendererǁrender__mutmut_35': xǁSpeedscopeRendererǁrender__mutmut_35, 
        'xǁSpeedscopeRendererǁrender__mutmut_36': xǁSpeedscopeRendererǁrender__mutmut_36, 
        'xǁSpeedscopeRendererǁrender__mutmut_37': xǁSpeedscopeRendererǁrender__mutmut_37, 
        'xǁSpeedscopeRendererǁrender__mutmut_38': xǁSpeedscopeRendererǁrender__mutmut_38, 
        'xǁSpeedscopeRendererǁrender__mutmut_39': xǁSpeedscopeRendererǁrender__mutmut_39
    }
    
    def render(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSpeedscopeRendererǁrender__mutmut_orig"), object.__getattribute__(self, "xǁSpeedscopeRendererǁrender__mutmut_mutants"), args, kwargs, self)
        return result 
    
    render.__signature__ = _mutmut_signature(xǁSpeedscopeRendererǁrender__mutmut_orig)
    xǁSpeedscopeRendererǁrender__mutmut_orig.__name__ = 'xǁSpeedscopeRendererǁrender'

    def default_processors(self) -> ProcessorList:
        """
        Default Processors for speedscope renderer; note that
        processors.aggregate_repeated_calls is removed because
        speedscope is a timeline-based format.
        """
        return [
            processors.remove_importlib,
            processors.remove_tracebackhide,
            processors.merge_consecutive_self_time,
            processors.remove_irrelevant_nodes,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_first_pyinstrument_frames_processor,
        ]
