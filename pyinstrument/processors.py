"""
Processors are functions that take a Frame object, and mutate the tree to perform some task.

They can mutate the tree in-place, but also can change the root frame, they should always be
called like::

    frame = processor(frame, options=...)
"""

from __future__ import annotations

import re
from operator import methodcaller
from typing import Any, Callable, Dict, Union

from pyinstrument.frame import BaseFrame, Frame, FrameGroup, SelfTimeFrame

# pyright: strict


ProcessorType = Callable[..., Union[BaseFrame, None]]
ProcessorOptions = Dict[str, Any]


def remove_importlib(frame: BaseFrame | None, options: ProcessorOptions) -> BaseFrame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    if not isinstance(frame, Frame):
        return frame

    for child in frame.children:
        remove_importlib(child, options=options)

        if child.file_path and "<frozen importlib._bootstrap" in child.file_path:
            # remove this node, moving the self_time and children up to the parent
            frame.self_time += child.self_time
            frame.add_children(child.children, after=child)
            child.remove_from_parent()

    return frame


def aggregate_repeated_calls(
    frame: BaseFrame | None, options: ProcessorOptions
) -> BaseFrame | None:
    """
    Converts a timeline into a time-aggregate summary.

    Adds together calls along the same call stack, so that repeated calls appear as the same
    frame. Removes time-linearity - frames are sorted according to total time spent.

    Useful for outputs that display a summary of execution (e.g. text and html outputs)
    """
    if frame is None:
        return None

    children_by_identifier: dict[str, BaseFrame] = {}

    # iterate over a copy of the children since it's going to mutate while we're iterating
    for child in frame.children:
        if child.identifier in children_by_identifier:
            aggregate_frame = children_by_identifier[child.identifier]

            # combine the two frames, putting the children and self_time into the aggregate frame.
            aggregate_frame.self_time += child.self_time
            if child.children:
                if not isinstance(aggregate_frame, Frame):
                    raise Exception("cannot aggregate children into a DummyFrame")
                aggregate_frame.add_children(child.children)

            # remove this frame, it's been incorporated into aggregate_frame
            child.remove_from_parent()
        else:
            # never seen this identifier before. It becomes the aggregate frame.
            children_by_identifier[child.identifier] = child

    # recurse into the children
    for child in frame.children:
        aggregate_repeated_calls(child, options=options)

    # sort the children by time
    # it's okay to use the internal _children list, sinde we're not changing the tree
    # structure.
    frame._children.sort(key=methodcaller("time"), reverse=True)  # type: ignore # noqa

    return frame


def group_library_frames_processor(
    frame: BaseFrame | None, options: ProcessorOptions
) -> BaseFrame | None:
    """
    Groups frames that should be hidden into :class:`FrameGroup` objects,
    according to ``hide_regex`` and ``show_regex`` in the options dict. If
    both match, 'show' has precedence.

    Single frames are not grouped, there must be at least two frames in a
    group.
    """
    if frame is None:
        return None

    hide_regex: str | None = options.get("hide_regex")
    show_regex: str | None = options.get("show_regex")

    def should_be_hidden(frame: BaseFrame):
        frame_file_path = frame.file_path or ""

        should_show = (show_regex is not None) and re.match(show_regex, frame_file_path)
        should_hide = (hide_regex is not None) and re.match(hide_regex, frame_file_path)

        # check for explicit user show/hide rules. 'show' has precedence.
        if should_show:
            return False
        if should_hide:
            return True

        return not frame.is_application_code

    def add_frames_to_group(frame: BaseFrame, group: FrameGroup):
        group.add_frame(frame)
        for child in frame.children:
            if should_be_hidden(child):
                add_frames_to_group(child, group)

    for child in frame.children:
        if not child.group and (
            should_be_hidden(child) and any(should_be_hidden(cc) for cc in child.children)
        ):
            group = FrameGroup(child)
            add_frames_to_group(child, group)

        group_library_frames_processor(child, options=options)

    return frame


def merge_consecutive_self_time(
    frame: BaseFrame | None, options: ProcessorOptions
) -> BaseFrame | None:
    """
    Combines consecutive 'self time' frames.
    """
    if frame is None:
        return None

    previous_self_time_frame = None

    for child in frame.children:
        if isinstance(child, SelfTimeFrame):
            if previous_self_time_frame:
                # merge
                previous_self_time_frame.self_time += child.self_time
                child.remove_from_parent()
            else:
                # keep a reference, maybe it'll be added to on the next loop
                previous_self_time_frame = child
        else:
            previous_self_time_frame = None

    for child in frame.children:
        merge_consecutive_self_time(child, options=options)

    return frame


def remove_unnecessary_self_time_nodes(
    frame: BaseFrame | None, options: ProcessorOptions
) -> BaseFrame | None:
    """
    When a frame has only one child, and that is a self-time frame, remove
    that node and move the time to parent, since it's unnecessary - it
    clutters the output and offers no additional information.
    """
    if frame is None:
        return None

    if len(frame.children) == 1 and isinstance(frame.children[0], SelfTimeFrame):
        child = frame.children[0]
        frame.self_time += child.self_time
        child.remove_from_parent()

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def remove_irrelevant_nodes(
    frame: BaseFrame | None, options: ProcessorOptions, total_time: float | None = None
) -> BaseFrame | None:
    """
    Remove nodes that represent less than e.g. 1% of the output.
    """
    if frame is None:
        return None

    if total_time is None:
        total_time = frame.time()

    filter_threshold = options.get("filter_threshold", 0.01)

    for child in frame.children:
        proportion_of_total = child.time() / total_time

        if proportion_of_total < filter_threshold:
            frame.self_time += child.time()
            child.remove_from_parent()

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame
