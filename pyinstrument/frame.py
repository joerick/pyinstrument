from __future__ import annotations

import math
import os
import sys
import uuid
from typing import Sequence

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


class Frame:
    """
    Object that represents a stack frame in the parsed tree
    """

    parent: Frame | None
    group: FrameGroup | None
    time: float

    # tracks the time from frames that were deleted during processing
    absorbed_time: float

    attributes: dict[str, float]

    def __init__(
        self,
        identifier_or_frame_info: str = "",
        children: Sequence[Frame] | None = None,
        time: float = 0,
    ):
        identifier = frame_info_get_identifier(identifier_or_frame_info)
        self.identifier = identifier
        self.parent = None
        self.time = 0.0
        self.group = None
        self.absorbed_time = 0.0

        self._identifier_parts = identifier.split("\x00")
        self.attributes = {}
        self._children = []

        self.record_time_from_frame_info(frame_info=identifier_or_frame_info, time=time)

        if children:
            for child in children:
                self.add_child(child)

    def record_time_from_frame_info(self, frame_info: str, time: float):
        self.time += time

        _, attributes_list = parse_frame_info(frame_info)

        for attribute in attributes_list:
            try:
                self.attributes[attribute] += time
            except KeyError:
                self.attributes[attribute] = time

    def remove_from_parent(self):
        """
        Removes this frame from its parent, and nulls the parent link
        """
        if self.parent:
            self.parent._children.remove(self)
            self.parent = None

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

        if not hasattr(self, "_file_path_short"):
            result = None

            if self.file_path:
                if len(self.file_path.split(os.sep)) == 1:
                    # probably not a file path at all, more likely <built-in>
                    # or similar
                    result = self.file_path
                else:
                    for path in sys.path:
                        # On Windows, if self.file_path and path are on
                        # different drives, relpath will result in exception,
                        # because it cannot compute a relpath in this case.
                        # The root cause is that on Windows, there is no root
                        # dir like '/' on Linux.
                        try:
                            candidate = os.path.relpath(self.file_path, path)
                        except ValueError:
                            continue

                        if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                            result = candidate

            self._file_path_short = result

        return self._file_path_short

    @property
    def is_application_code(self) -> bool:
        if self.is_synthetic:
            return False

        file_path = self.file_path

        if not file_path:
            return False

        if "/lib/" in file_path:
            return False

        if os.sep != "/":
            # windows uses back-slash too, so let's look for that too.
            if (f"{os.sep}lib{os.sep}") in file_path:
                return False

        if file_path.startswith("<"):
            if file_path.startswith("<ipython-input-"):
                # lines typed at a console or in a notebook are app code
                return True
            else:
                # otherwise, this is probably some library-internal code gen
                return False

        return True

    @property
    def code_position_short(self) -> str | None:
        if self.file_path_short and self.line_no:
            return "%s:%i" % (self.file_path_short, self.line_no)
        return self.file_path_short

    _children: list[Frame]
    attributes: dict[str, float]

    def add_child(self, frame: Frame, after: Frame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """

        if self.identifier in SYNTHETIC_LEAF_IDENTIFIERS:
            raise ValueError("Cannot add children to a leaf-only frame")

        frame.remove_from_parent()
        frame.parent = self
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, frame)

    def add_children(self, frames: Sequence[Frame], after: Frame | None = None):
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

    def await_time(self) -> float:
        # i'd rather this was a property, but properties use twice as many stack frames
        await_time = 0

        if self.identifier == AWAIT_FRAME_IDENTIFIER:
            await_time += self.time

        for child in self.children:
            await_time += child.await_time()

        return await_time

    def get_attribute_value(self, attribute_marker: str) -> str | None:
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

    @property
    def class_name(self) -> str | None:
        return self.get_attribute_value(ATTRIBUTE_MARKER_CLASS_NAME)

    @property
    def has_tracebackhide(self) -> bool:
        """
        Returns whether this frame has a `__tracebackhide__` variable.
        """
        return self.get_attribute_value(ATTRIBUTE_MARKER_TRACEBACKHIDE) == "1"

    def self_check(self, recursive: bool = True) -> None:
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

    def __repr__(self):
        return "Frame(identifier=%s, time=%f, len(children)=%d), group=%r" % (
            self.identifier,
            self.time,
            len(self.children),
            self.group,
        )


class FrameGroup:
    _libraries: list[str] | None
    _frames: list[Frame]
    _exit_frames: list[Frame] | None

    def __init__(self, root: Frame):
        self.root = root
        self.id = str(uuid.uuid4())
        self._frames = []
        self._exit_frames = None
        self._libraries = None

        self.add_frame(root)

    @property
    def libraries(self) -> list[str]:
        if self._libraries is None:
            libraries: list[str] = []

            for frame in self.frames:
                if frame.file_path_short:
                    library = frame.file_path_short.split(os.sep)[0]
                    library, _ = os.path.splitext(library)
                    if library and library not in libraries:
                        libraries.append(library)
            self._libraries = libraries

        return self._libraries

    @property
    def frames(self) -> Sequence[Frame]:
        return tuple(self._frames)

    def add_frame(self, frame: Frame):
        if frame.group:
            frame.group.remove_frame(frame)

        self._frames.append(frame)
        frame.group = self

    def remove_frame(self, frame: Frame):
        assert frame.group is self
        self._frames.remove(frame)
        frame.group = None

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

    def __repr__(self):
        return "FrameGroup(len(frames)=%d)" % len(self.frames)
