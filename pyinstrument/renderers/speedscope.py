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

    def default(self, o: Any) -> Any:
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


class SpeedscopeRenderer(FrameRenderer):
    """
    Outputs a tree of JSON conforming to the speedscope schema documented at

    wiki: https://github.com/jlfwong/speedscope/wiki/Importing-from-custom-sources
    schema: https://www.speedscope.app/file-format-schema.json
    spec: https://github.com/jlfwong/speedscope/blob/main/src/lib/file-format-spec.ts
    example: https://github.com/jlfwong/speedscope/blob/main/sample/profiles/speedscope/0.0.1/simple.speedscope.json

    """

    output_file_extension = "speedscope.json"

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

    def render_frame(self, frame: Frame | None) -> list[SpeedscopeEvent]:
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

    def render(self, session: Session):
        frame = self.preprocess(session.root_frame())

        id_: str = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(session.start_time))
        name: str = f"CPU profile for {session.program} at {id_}"

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
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_irrelevant_nodes,
            processors.remove_first_pyinstrument_frames_processor,
        ]
