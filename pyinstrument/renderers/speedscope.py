from __future__ import annotations

import json
import time
from typing import Any, Callable, NamedTuple
from enum import Enum

from pyinstrument import processors
from pyinstrument.frame import BaseFrame
from pyinstrument.renderers.base import ProcessorList, Renderer
from pyinstrument.session import Session

# pyright: strict


encode_str: Callable[[str], str] = json.encoder.encode_basestring  # type: ignore


def encode_bool(a_bool: bool):
    return "true" if a_bool else "false"


class SpeedscopeFrame(NamedTuple):
    """
    Named tuple to store data needed for speedscope's concept of a
    frame, hereafter referred to as a "speedscope frame", as opposed to
    a "pyinstrument frame". This type must be hashable in order to use
    it as a dictionary key; a dictionary will be used to track unique
    speedscope frames.
    """
    name: str | None
    file: str | None
    line: int | None


class SpeedscopeFrameEncoder(json.JSONEncoder):
    """
    Encoder used by json.dumps method on SpeedscopeFrame objects to serialize
    SpeedscopeEvent objects in JSON format.
    """
    def default(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeFrame):
            return {"name": o.name, "file": o.file, "line": o.line}
        return json.JSONEncoder.default(self, o)


class SpeedscopeEventType(Enum):
    """Enum representing the only two types of speedscope frame events"""
    OPEN = "O"
    CLOSE = "C"


class SpeedscopeEvent(NamedTuple):
    """
    Named tuple to store speedscope's concept of an "event", which
    corresponds to opening or closing stack frames as functions or
    methods are entered or exited.
    """
    type: SpeedscopeEventType
    at: float
    frame: int


class SpeedscopeEventEncoder(json.JSONEncoder):
    """
    Encoder used by json.dumps method on SpeedscopeEvent objects to
    serialize SpeedscopeEvent objects in JSON format.
    """
    def default(self, o: Any) -> Any:
        if isinstance(o, SpeedscopeEvent):
            return {"type": o.type, "at": o.at, "frame": o.frame}
        if isinstance(o, SpeedscopeEventType):
            return o.value
        return json.JSONEncoder.default(self, o)


# Dictionaries in Python 3.7+ track insertion order, and
# dict.popitem() returns (key, value) pair in reverse insertion order
# (LIFO)

class SpeedscopeRenderer(Renderer):
    """
    Outputs a tree of JSON conforming to the speedscope schema documented at

    wiki: https://github.com/jlfwong/speedscope/wiki/Importing-from-custom-sources
    schema: https://www.speedscope.app/file-format-schema.json
    spec: https://github.com/jlfwong/speedscope/blob/main/src/lib/file-format-spec.ts
    example: https://github.com/jlfwong/speedscope/blob/main/sample/profiles/speedscope/0.0.1/simple.speedscope.json

    """

    def __init__(self, **kwargs: Any):
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


    def render_frame(self, frame: BaseFrame | None):
        """Renders frame as string by representing it JSON array-formatted
        string containing the speedscope open frame event, opend and
        close frame events of all children, and close event, in order,
        except for the outer enclosing square brackets. This
        information is used to build up the "events" array in
        speedscope-formatted JSON.

        This method has two notable side effects:

        * it populates the self._frame_to_index dictionary that matches
          speedscope frames with their positions in the "shared" array of
          speedscope output; this dictionary will be used to write this
          "shared" array in the render method

        * it accumulates a running total of time elapsed by
          accumulating the self_time spent in each pyinstrument frame;
          this running total is used by speedscope events to construct
          a flame chart

        This method avoids using the json module because it uses twice
        as many stack frames, which will crash by exceeding the stack
        limit on deep-but-valid call stacks. List comprehensions are
        avoided for similar reasons.
        """

        # if frame is None, recursion bottoms out; no event frames
        # need to be added
        if frame is None:
            return ""

        sframe = SpeedscopeFrame(frame.function, frame.file_path, frame.line_no)
        if sframe not in self._frame_to_index:
            self._frame_to_index[sframe] = len(self._frame_to_index)

        sframe_index = self._frame_to_index[sframe]
        open_event = SpeedscopeEvent(
            SpeedscopeEventType.OPEN,
            self._event_time,
            sframe_index
        )

        event_array: list[str] = [json.dumps(open_event, cls=SpeedscopeEventEncoder)]

        for child in frame.children:
            child_events = self.render_frame(child)
            if child_events:
                event_array.append(child_events)


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
        self._event_time += frame.self_time

        close_event = SpeedscopeEvent(
            SpeedscopeEventType.CLOSE,
            self._event_time,
            sframe_index
        )
        event_array.append(json.dumps(close_event, cls=SpeedscopeEventEncoder))

        # Omit enclosing square brackets here; these brackets are applied in
        # the render method
        return "%s" % ",".join(event_array)

    def render(self, session: Session):
        frame = self.preprocess(session.root_frame())

        property_decls: list[str] = []

        # Fields for file
        schema_url: str = "https://www.speedscope.app/file-format-schema.json"
        property_decls.append('"$schema": %s' % encode_str(schema_url))

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = "CPU profile for {} at {}".format(session.program, id_)
        property_decls.append('"name": %s' % encode_str(name))

        property_decls.append('"activeProfileIndex": null')

        # TODO(goxberry@gmail.com): figure out how to get version from
        # pyinstrument and add it here as something like
        # pyinstrument@4.0.4 ; can't use from pyinstrument import
        # __version__
        exporter: str = "pyinstrument"
        property_decls.append('"exporter": %s' % encode_str(exporter))

        # Fields for profile
        profile_decls: list[str] = []
        profile_type: str = "evented"
        profile_decls.append('"type": %s' % encode_str(profile_type))

        profile_name: str = session.program
        profile_decls.append('"name": %s' % encode_str(profile_name))

        unit: str = "seconds"
        profile_decls.append('"unit": %s' % encode_str(unit))

        start_value: float = 0.0
        profile_decls.append('"startValue": %f' % start_value)

        end_value: float = session.duration
        profile_decls.append('"endValue": %f' % end_value)

        # use render_frame to build up dictionary of frames for 'shared' field
        # via the self._frame_to_index field; have it output the string
        # representation of the events array
        profile_decls.append('"events": [%s]' % self.render_frame(frame))
        profile_string = "{%s}" % ",".join(profile_decls)

        property_decls.append('"profiles": [%s]' % profile_string)

        # exploits Python 3.7+ dictionary property of iterating over
        # keys in insertion order
        shared_decls: list[str] = []
        for sframe in iter(self._frame_to_index):
            shared_decls.append(json.dumps(sframe, cls=SpeedscopeFrameEncoder))
        property_decls.append('"shared": {"frames": [%s]}' % ",".join(shared_decls))

        return "{%s}\n" % ",".join(property_decls)

    def default_processors(self) -> ProcessorList:
        return [
            processors.remove_importlib,
            processors.merge_consecutive_self_time,
            processors.aggregate_repeated_calls,
            processors.group_library_frames_processor,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_irrelevant_nodes,
        ]
