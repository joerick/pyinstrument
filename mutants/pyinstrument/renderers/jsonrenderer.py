from __future__ import annotations

import json
import typing
from typing import Any, Callable

from pyinstrument import processors
from pyinstrument.frame import Frame
from pyinstrument.renderers.base import FrameRenderer, ProcessorList
from pyinstrument.session import Session

# pyright: strict


# note: this file is called jsonrenderer to avoid hiding built-in module 'json'.

encode_str = typing.cast(Callable[[str], str], json.encoder.encode_basestring)  # type: ignore
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


def x_encode_bool__mutmut_orig(a_bool: bool):
    return "true" if a_bool else "false"


def x_encode_bool__mutmut_1(a_bool: bool):
    return "XXtrueXX" if a_bool else "false"


def x_encode_bool__mutmut_2(a_bool: bool):
    return "TRUE" if a_bool else "false"


def x_encode_bool__mutmut_3(a_bool: bool):
    return "true" if a_bool else "XXfalseXX"


def x_encode_bool__mutmut_4(a_bool: bool):
    return "true" if a_bool else "FALSE"

x_encode_bool__mutmut_mutants : ClassVar[MutantDict] = {
'x_encode_bool__mutmut_1': x_encode_bool__mutmut_1, 
    'x_encode_bool__mutmut_2': x_encode_bool__mutmut_2, 
    'x_encode_bool__mutmut_3': x_encode_bool__mutmut_3, 
    'x_encode_bool__mutmut_4': x_encode_bool__mutmut_4
}

def encode_bool(*args, **kwargs):
    result = _mutmut_trampoline(x_encode_bool__mutmut_orig, x_encode_bool__mutmut_mutants, args, kwargs)
    return result 

encode_bool.__signature__ = _mutmut_signature(x_encode_bool__mutmut_orig)
x_encode_bool__mutmut_orig.__name__ = 'x_encode_bool'


class JSONRenderer(FrameRenderer):
    """
    Outputs a tree of JSON, containing processed frames.
    """

    output_file_extension = "json"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def xǁJSONRendererǁrender_frame__mutmut_orig(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_1(self, frame: Frame | None):
        if frame is not None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_2(self, frame: Frame | None):
        if frame is None:
            return "XXnullXX"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_3(self, frame: Frame | None):
        if frame is None:
            return "NULL"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_4(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = None
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_5(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append(None)
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_6(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' / encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_7(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('XX"function": %sXX' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_8(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"FUNCTION": %S' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_9(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(None))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_10(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append(None)
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_11(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' / encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_12(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('XX"file_path_short": %sXX' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_13(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"FILE_PATH_SHORT": %S' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_14(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(None))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_15(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short and ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_16(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or "XXXX"))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_17(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append(None)
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_18(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' / encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_19(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('XX"file_path": %sXX' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_20(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"FILE_PATH": %S' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_21(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(None))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_22(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path and ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_23(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or "XXXX"))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_24(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append(None)
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_25(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' / (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_26(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('XX"line_no": %dXX' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_27(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"LINE_NO": %D' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_28(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no and 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_29(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 1))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_30(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append(None)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_31(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' / frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_32(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('XX"time": %fXX' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_33(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"TIME": %F' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_34(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append(None)
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_35(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' / frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_36(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('XX"await_time": %fXX' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_37(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"AWAIT_TIME": %F' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_38(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            None
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_39(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' / encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_40(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            'XX"is_application_code": %sXX' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_41(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"IS_APPLICATION_CODE": %S' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_42(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(None)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_43(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code and False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_44(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or True)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_45(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = None
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_46(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(None)
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_47(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(None))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_48(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append(None)

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_49(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' / ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_50(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('XX"children": [%s]XX' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_51(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"CHILDREN": [%S]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_52(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(None))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_53(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % "XX,XX".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_54(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append(None)

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_55(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' / encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_56(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('XX"group_id": %sXX' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_57(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"GROUP_ID": %S' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_58(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(None))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_59(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append(None)

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_60(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' / encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_61(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('XX"class_name": %sXX' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_62(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"CLASS_NAME": %S' % encode_str(frame.class_name))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_63(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(None))

        return "{%s}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_64(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" / ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_65(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "XX{%s}XX" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_66(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%S}" % ",".join(property_decls)

    def xǁJSONRendererǁrender_frame__mutmut_67(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % ",".join(None)

    def xǁJSONRendererǁrender_frame__mutmut_68(self, frame: Frame | None):
        if frame is None:
            return "null"
        # we don't use the json module because it uses 2x stack frames, so
        # crashes on deep but valid call stacks

        property_decls: list[str] = []
        property_decls.append('"function": %s' % encode_str(frame.function))
        property_decls.append('"file_path_short": %s' % encode_str(frame.file_path_short or ""))
        property_decls.append('"file_path": %s' % encode_str(frame.file_path or ""))
        property_decls.append('"line_no": %d' % (frame.line_no or 0))
        property_decls.append('"time": %f' % frame.time)
        property_decls.append('"await_time": %f' % frame.await_time())
        property_decls.append(
            '"is_application_code": %s' % encode_bool(frame.is_application_code or False)
        )

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons: list[str] = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ",".join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode_str(frame.group.id))

        if frame.class_name:
            property_decls.append('"class_name": %s' % encode_str(frame.class_name))

        return "{%s}" % "XX,XX".join(property_decls)
    
    xǁJSONRendererǁrender_frame__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁJSONRendererǁrender_frame__mutmut_1': xǁJSONRendererǁrender_frame__mutmut_1, 
        'xǁJSONRendererǁrender_frame__mutmut_2': xǁJSONRendererǁrender_frame__mutmut_2, 
        'xǁJSONRendererǁrender_frame__mutmut_3': xǁJSONRendererǁrender_frame__mutmut_3, 
        'xǁJSONRendererǁrender_frame__mutmut_4': xǁJSONRendererǁrender_frame__mutmut_4, 
        'xǁJSONRendererǁrender_frame__mutmut_5': xǁJSONRendererǁrender_frame__mutmut_5, 
        'xǁJSONRendererǁrender_frame__mutmut_6': xǁJSONRendererǁrender_frame__mutmut_6, 
        'xǁJSONRendererǁrender_frame__mutmut_7': xǁJSONRendererǁrender_frame__mutmut_7, 
        'xǁJSONRendererǁrender_frame__mutmut_8': xǁJSONRendererǁrender_frame__mutmut_8, 
        'xǁJSONRendererǁrender_frame__mutmut_9': xǁJSONRendererǁrender_frame__mutmut_9, 
        'xǁJSONRendererǁrender_frame__mutmut_10': xǁJSONRendererǁrender_frame__mutmut_10, 
        'xǁJSONRendererǁrender_frame__mutmut_11': xǁJSONRendererǁrender_frame__mutmut_11, 
        'xǁJSONRendererǁrender_frame__mutmut_12': xǁJSONRendererǁrender_frame__mutmut_12, 
        'xǁJSONRendererǁrender_frame__mutmut_13': xǁJSONRendererǁrender_frame__mutmut_13, 
        'xǁJSONRendererǁrender_frame__mutmut_14': xǁJSONRendererǁrender_frame__mutmut_14, 
        'xǁJSONRendererǁrender_frame__mutmut_15': xǁJSONRendererǁrender_frame__mutmut_15, 
        'xǁJSONRendererǁrender_frame__mutmut_16': xǁJSONRendererǁrender_frame__mutmut_16, 
        'xǁJSONRendererǁrender_frame__mutmut_17': xǁJSONRendererǁrender_frame__mutmut_17, 
        'xǁJSONRendererǁrender_frame__mutmut_18': xǁJSONRendererǁrender_frame__mutmut_18, 
        'xǁJSONRendererǁrender_frame__mutmut_19': xǁJSONRendererǁrender_frame__mutmut_19, 
        'xǁJSONRendererǁrender_frame__mutmut_20': xǁJSONRendererǁrender_frame__mutmut_20, 
        'xǁJSONRendererǁrender_frame__mutmut_21': xǁJSONRendererǁrender_frame__mutmut_21, 
        'xǁJSONRendererǁrender_frame__mutmut_22': xǁJSONRendererǁrender_frame__mutmut_22, 
        'xǁJSONRendererǁrender_frame__mutmut_23': xǁJSONRendererǁrender_frame__mutmut_23, 
        'xǁJSONRendererǁrender_frame__mutmut_24': xǁJSONRendererǁrender_frame__mutmut_24, 
        'xǁJSONRendererǁrender_frame__mutmut_25': xǁJSONRendererǁrender_frame__mutmut_25, 
        'xǁJSONRendererǁrender_frame__mutmut_26': xǁJSONRendererǁrender_frame__mutmut_26, 
        'xǁJSONRendererǁrender_frame__mutmut_27': xǁJSONRendererǁrender_frame__mutmut_27, 
        'xǁJSONRendererǁrender_frame__mutmut_28': xǁJSONRendererǁrender_frame__mutmut_28, 
        'xǁJSONRendererǁrender_frame__mutmut_29': xǁJSONRendererǁrender_frame__mutmut_29, 
        'xǁJSONRendererǁrender_frame__mutmut_30': xǁJSONRendererǁrender_frame__mutmut_30, 
        'xǁJSONRendererǁrender_frame__mutmut_31': xǁJSONRendererǁrender_frame__mutmut_31, 
        'xǁJSONRendererǁrender_frame__mutmut_32': xǁJSONRendererǁrender_frame__mutmut_32, 
        'xǁJSONRendererǁrender_frame__mutmut_33': xǁJSONRendererǁrender_frame__mutmut_33, 
        'xǁJSONRendererǁrender_frame__mutmut_34': xǁJSONRendererǁrender_frame__mutmut_34, 
        'xǁJSONRendererǁrender_frame__mutmut_35': xǁJSONRendererǁrender_frame__mutmut_35, 
        'xǁJSONRendererǁrender_frame__mutmut_36': xǁJSONRendererǁrender_frame__mutmut_36, 
        'xǁJSONRendererǁrender_frame__mutmut_37': xǁJSONRendererǁrender_frame__mutmut_37, 
        'xǁJSONRendererǁrender_frame__mutmut_38': xǁJSONRendererǁrender_frame__mutmut_38, 
        'xǁJSONRendererǁrender_frame__mutmut_39': xǁJSONRendererǁrender_frame__mutmut_39, 
        'xǁJSONRendererǁrender_frame__mutmut_40': xǁJSONRendererǁrender_frame__mutmut_40, 
        'xǁJSONRendererǁrender_frame__mutmut_41': xǁJSONRendererǁrender_frame__mutmut_41, 
        'xǁJSONRendererǁrender_frame__mutmut_42': xǁJSONRendererǁrender_frame__mutmut_42, 
        'xǁJSONRendererǁrender_frame__mutmut_43': xǁJSONRendererǁrender_frame__mutmut_43, 
        'xǁJSONRendererǁrender_frame__mutmut_44': xǁJSONRendererǁrender_frame__mutmut_44, 
        'xǁJSONRendererǁrender_frame__mutmut_45': xǁJSONRendererǁrender_frame__mutmut_45, 
        'xǁJSONRendererǁrender_frame__mutmut_46': xǁJSONRendererǁrender_frame__mutmut_46, 
        'xǁJSONRendererǁrender_frame__mutmut_47': xǁJSONRendererǁrender_frame__mutmut_47, 
        'xǁJSONRendererǁrender_frame__mutmut_48': xǁJSONRendererǁrender_frame__mutmut_48, 
        'xǁJSONRendererǁrender_frame__mutmut_49': xǁJSONRendererǁrender_frame__mutmut_49, 
        'xǁJSONRendererǁrender_frame__mutmut_50': xǁJSONRendererǁrender_frame__mutmut_50, 
        'xǁJSONRendererǁrender_frame__mutmut_51': xǁJSONRendererǁrender_frame__mutmut_51, 
        'xǁJSONRendererǁrender_frame__mutmut_52': xǁJSONRendererǁrender_frame__mutmut_52, 
        'xǁJSONRendererǁrender_frame__mutmut_53': xǁJSONRendererǁrender_frame__mutmut_53, 
        'xǁJSONRendererǁrender_frame__mutmut_54': xǁJSONRendererǁrender_frame__mutmut_54, 
        'xǁJSONRendererǁrender_frame__mutmut_55': xǁJSONRendererǁrender_frame__mutmut_55, 
        'xǁJSONRendererǁrender_frame__mutmut_56': xǁJSONRendererǁrender_frame__mutmut_56, 
        'xǁJSONRendererǁrender_frame__mutmut_57': xǁJSONRendererǁrender_frame__mutmut_57, 
        'xǁJSONRendererǁrender_frame__mutmut_58': xǁJSONRendererǁrender_frame__mutmut_58, 
        'xǁJSONRendererǁrender_frame__mutmut_59': xǁJSONRendererǁrender_frame__mutmut_59, 
        'xǁJSONRendererǁrender_frame__mutmut_60': xǁJSONRendererǁrender_frame__mutmut_60, 
        'xǁJSONRendererǁrender_frame__mutmut_61': xǁJSONRendererǁrender_frame__mutmut_61, 
        'xǁJSONRendererǁrender_frame__mutmut_62': xǁJSONRendererǁrender_frame__mutmut_62, 
        'xǁJSONRendererǁrender_frame__mutmut_63': xǁJSONRendererǁrender_frame__mutmut_63, 
        'xǁJSONRendererǁrender_frame__mutmut_64': xǁJSONRendererǁrender_frame__mutmut_64, 
        'xǁJSONRendererǁrender_frame__mutmut_65': xǁJSONRendererǁrender_frame__mutmut_65, 
        'xǁJSONRendererǁrender_frame__mutmut_66': xǁJSONRendererǁrender_frame__mutmut_66, 
        'xǁJSONRendererǁrender_frame__mutmut_67': xǁJSONRendererǁrender_frame__mutmut_67, 
        'xǁJSONRendererǁrender_frame__mutmut_68': xǁJSONRendererǁrender_frame__mutmut_68
    }
    
    def render_frame(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁJSONRendererǁrender_frame__mutmut_orig"), object.__getattribute__(self, "xǁJSONRendererǁrender_frame__mutmut_mutants"), args, kwargs, self)
        return result 
    
    render_frame.__signature__ = _mutmut_signature(xǁJSONRendererǁrender_frame__mutmut_orig)
    xǁJSONRendererǁrender_frame__mutmut_orig.__name__ = 'xǁJSONRendererǁrender_frame'

    def xǁJSONRendererǁrender__mutmut_orig(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_1(self, session: Session):
        frame = None

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_2(self, session: Session):
        frame = self.preprocess(None)

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_3(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = None
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_4(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append(None)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_5(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' / session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_6(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('XX"start_time": %fXX' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_7(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"START_TIME": %F' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_8(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append(None)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_9(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' / session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_10(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('XX"duration": %fXX' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_11(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"DURATION": %F' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_12(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append(None)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_13(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' / session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_14(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('XX"sample_count": %dXX' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_15(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"SAMPLE_COUNT": %D' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_16(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append(None)
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_17(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' / encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_18(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('XX"target_description": %sXX' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_19(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"TARGET_DESCRIPTION": %S' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_20(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(None))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_21(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append(None)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_22(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' / session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_23(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('XX"cpu_time": %fXX' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_24(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"CPU_TIME": %F' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_25(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append(None)

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_26(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' / self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_27(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('XX"root_frame": %sXX' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_28(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"ROOT_FRAME": %S' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_29(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(None))

        return "{%s}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_30(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" / ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_31(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "XX{%s}\nXX" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_32(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%S}\n" % ",".join(property_decls)

    def xǁJSONRendererǁrender__mutmut_33(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(None)

    def xǁJSONRendererǁrender__mutmut_34(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % "XX,XX".join(property_decls)
    
    xǁJSONRendererǁrender__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁJSONRendererǁrender__mutmut_1': xǁJSONRendererǁrender__mutmut_1, 
        'xǁJSONRendererǁrender__mutmut_2': xǁJSONRendererǁrender__mutmut_2, 
        'xǁJSONRendererǁrender__mutmut_3': xǁJSONRendererǁrender__mutmut_3, 
        'xǁJSONRendererǁrender__mutmut_4': xǁJSONRendererǁrender__mutmut_4, 
        'xǁJSONRendererǁrender__mutmut_5': xǁJSONRendererǁrender__mutmut_5, 
        'xǁJSONRendererǁrender__mutmut_6': xǁJSONRendererǁrender__mutmut_6, 
        'xǁJSONRendererǁrender__mutmut_7': xǁJSONRendererǁrender__mutmut_7, 
        'xǁJSONRendererǁrender__mutmut_8': xǁJSONRendererǁrender__mutmut_8, 
        'xǁJSONRendererǁrender__mutmut_9': xǁJSONRendererǁrender__mutmut_9, 
        'xǁJSONRendererǁrender__mutmut_10': xǁJSONRendererǁrender__mutmut_10, 
        'xǁJSONRendererǁrender__mutmut_11': xǁJSONRendererǁrender__mutmut_11, 
        'xǁJSONRendererǁrender__mutmut_12': xǁJSONRendererǁrender__mutmut_12, 
        'xǁJSONRendererǁrender__mutmut_13': xǁJSONRendererǁrender__mutmut_13, 
        'xǁJSONRendererǁrender__mutmut_14': xǁJSONRendererǁrender__mutmut_14, 
        'xǁJSONRendererǁrender__mutmut_15': xǁJSONRendererǁrender__mutmut_15, 
        'xǁJSONRendererǁrender__mutmut_16': xǁJSONRendererǁrender__mutmut_16, 
        'xǁJSONRendererǁrender__mutmut_17': xǁJSONRendererǁrender__mutmut_17, 
        'xǁJSONRendererǁrender__mutmut_18': xǁJSONRendererǁrender__mutmut_18, 
        'xǁJSONRendererǁrender__mutmut_19': xǁJSONRendererǁrender__mutmut_19, 
        'xǁJSONRendererǁrender__mutmut_20': xǁJSONRendererǁrender__mutmut_20, 
        'xǁJSONRendererǁrender__mutmut_21': xǁJSONRendererǁrender__mutmut_21, 
        'xǁJSONRendererǁrender__mutmut_22': xǁJSONRendererǁrender__mutmut_22, 
        'xǁJSONRendererǁrender__mutmut_23': xǁJSONRendererǁrender__mutmut_23, 
        'xǁJSONRendererǁrender__mutmut_24': xǁJSONRendererǁrender__mutmut_24, 
        'xǁJSONRendererǁrender__mutmut_25': xǁJSONRendererǁrender__mutmut_25, 
        'xǁJSONRendererǁrender__mutmut_26': xǁJSONRendererǁrender__mutmut_26, 
        'xǁJSONRendererǁrender__mutmut_27': xǁJSONRendererǁrender__mutmut_27, 
        'xǁJSONRendererǁrender__mutmut_28': xǁJSONRendererǁrender__mutmut_28, 
        'xǁJSONRendererǁrender__mutmut_29': xǁJSONRendererǁrender__mutmut_29, 
        'xǁJSONRendererǁrender__mutmut_30': xǁJSONRendererǁrender__mutmut_30, 
        'xǁJSONRendererǁrender__mutmut_31': xǁJSONRendererǁrender__mutmut_31, 
        'xǁJSONRendererǁrender__mutmut_32': xǁJSONRendererǁrender__mutmut_32, 
        'xǁJSONRendererǁrender__mutmut_33': xǁJSONRendererǁrender__mutmut_33, 
        'xǁJSONRendererǁrender__mutmut_34': xǁJSONRendererǁrender__mutmut_34
    }
    
    def render(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁJSONRendererǁrender__mutmut_orig"), object.__getattribute__(self, "xǁJSONRendererǁrender__mutmut_mutants"), args, kwargs, self)
        return result 
    
    render.__signature__ = _mutmut_signature(xǁJSONRendererǁrender__mutmut_orig)
    xǁJSONRendererǁrender__mutmut_orig.__name__ = 'xǁJSONRendererǁrender'

    def default_processors(self) -> ProcessorList:
        return [
            processors.remove_importlib,
            processors.remove_tracebackhide,
            processors.merge_consecutive_self_time,
            processors.aggregate_repeated_calls,
            processors.remove_irrelevant_nodes,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_first_pyinstrument_frames_processor,
            processors.group_library_frames_processor,
        ]
