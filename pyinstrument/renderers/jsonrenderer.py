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


def encode_bool(a_bool: bool):
    return "true" if a_bool else "false"


class JSONRenderer(FrameRenderer):
    """
    Outputs a tree of JSON, containing processed frames.
    """

    output_file_extension = "json"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def render_frame(self, frame: Frame | None):
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

    def render(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []
        property_decls.append('"start_time": %f' % session.start_time)
        property_decls.append('"duration": %f' % session.duration)
        property_decls.append('"sample_count": %d' % session.sample_count)
        property_decls.append('"target_description": %s' % encode_str(session.target_description))
        property_decls.append('"cpu_time": %f' % session.cpu_time)
        property_decls.append('"root_frame": %s' % self.render_frame(frame))

        return "{%s}\n" % ",".join(property_decls)

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
