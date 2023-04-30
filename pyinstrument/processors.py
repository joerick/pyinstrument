"""
Processors are functions that take a Frame object, and mutate the tree to perform some task.

They can mutate the tree in-place, but also can change the root frame, they should always be
called like::

    frame = processor(frame, options=...)
"""

from __future__ import annotations

import re
from typing import Any, Callable, Dict, Union

from pyinstrument.frame import SELF_TIME_FRAME_IDENTIFIER, Frame, FrameGroup
from pyinstrument.frame_ops import combine_frames, delete_frame_from_tree

# pyright: strict


ProcessorType = Callable[..., Union[Frame, None]]
ProcessorOptions = Dict[str, Any]


def remove_importlib(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(child, options=options)

        if child.file_path and "<frozen importlib._bootstrap" in child.file_path:
            delete_frame_from_tree(child, replace_with="children")

    return frame


def remove_tracebackhide(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes frames that have set a local `__tracebackhide__` (e.g.
    `__tracebackhide__ = True`), to hide them from the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_tracebackhide(child, options=options)

        if child.has_tracebackhide:
            # remove this node, moving the self_time and children up to the parent
            delete_frame_from_tree(child, replace_with="children")

    return frame


def aggregate_repeated_calls(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Converts a timeline into a time-aggregate summary.

    Adds together calls along the same call stack, so that repeated calls appear as the same
    frame. Removes time-linearity - frames are sorted according to total time spent.

    Useful for outputs that display a summary of execution (e.g. text and html outputs)
    """
    if frame is None:
        return None

    children_by_identifier: dict[str, Frame] = {}

    # iterate over a copy of the children since it's going to mutate while we're iterating
    for child in frame.children:
        if child.identifier in children_by_identifier:
            aggregate_frame = children_by_identifier[child.identifier]

            # combine child into aggregate frame, removing it from the tree
            combine_frames(child, into=aggregate_frame)
        else:
            # never seen this identifier before. It becomes the aggregate frame.
            children_by_identifier[child.identifier] = child

    # recurse into the children
    for child in frame.children:
        aggregate_repeated_calls(child, options=options)

    # sort the children by time
    # we use the internal _children list, because we need to mutate it
    frame._children.sort(key=lambda c: c.time, reverse=True)  # type: ignore # noqa

    return frame


def group_library_frames_processor(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Groups frames that should be hidden into :class:`FrameGroup` objects,
    according to ``hide_regex`` and ``show_regex`` in the options dict, as
    applied to the file path of the source code of the frame. If both match,
    'show' has precedence.
    Options:

    ``hide_regex``
      regular expression, which if matches the file path, hides the frame in a
      frame group.

    ``show_regex``
      regular expression, which if matches the file path, ensures the frame is
      not hidden

    Single frames are not grouped, there must be at least two frames in a
    group.
    """
    if frame is None:
        return None

    hide_regex: str | None = options.get("hide_regex")
    show_regex: str | None = options.get("show_regex")

    def should_be_hidden(frame: Frame):
        frame_file_path = frame.file_path or ""

        should_show = (show_regex is not None) and re.match(show_regex, frame_file_path)
        should_hide = (hide_regex is not None) and re.match(hide_regex, frame_file_path)

        # check for explicit user show/hide rules. 'show' has precedence.
        if should_show:
            return False
        if should_hide:
            return True

        return not frame.is_application_code

    def add_frames_to_group(frame: Frame, group: FrameGroup):
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
    frame: Frame | None, options: ProcessorOptions, recursive: bool = True
) -> Frame | None:
    """
    Combines consecutive 'self time' frames.
    """
    if frame is None:
        return None

    previous_self_time_frame = None

    for child in frame.children:
        if child.identifier == SELF_TIME_FRAME_IDENTIFIER:
            if previous_self_time_frame:
                # merge
                previous_self_time_frame.time += child.time
                child.remove_from_parent()
            else:
                # keep a reference, maybe it'll be added to on the next loop
                previous_self_time_frame = child
        else:
            previous_self_time_frame = None

    if recursive:
        for child in frame.children:
            merge_consecutive_self_time(child, options=options, recursive=True)

    return frame


def remove_unnecessary_self_time_nodes(
    frame: Frame | None, options: ProcessorOptions
) -> Frame | None:
    """
    When a frame has only one child, and that is a self-time frame, remove
    that node and move the time to parent, since it's unnecessary - it
    clutters the output and offers no additional information.
    """
    if frame is None:
        return None

    if len(frame.children) == 1 and frame.children[0].identifier == SELF_TIME_FRAME_IDENTIFIER:
        delete_frame_from_tree(frame.children[0], replace_with="nothing")

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def remove_irrelevant_nodes(
    frame: Frame | None, options: ProcessorOptions, total_time: float | None = None
) -> Frame | None:
    """
    Remove nodes that represent less than e.g. 1% of the output. Options:

    ``filter_threshold``
      sets the minimum duration of a frame to be included in the output.
      Default: 0.01.
    """
    if frame is None:
        return None

    if total_time is None:
        total_time = frame.time

        # prevent divide by zero
        if total_time <= 0:
            total_time = 1e-44

    filter_threshold = options.get("filter_threshold", 0.01)

    for child in frame.children:
        proportion_of_total = child.time / total_time

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


# pylint: disable=W0613
def remove_first_pyinstrument_frames_processor(
    frame: Frame | None, options: ProcessorOptions
) -> Frame | None:
    """
    The first few frames when using the command line are the __main__ of
    pyinstrument, the eval, and the 'runpy' module. I want to remove that from
    the output.
    """
    if frame is None:
        return None

    # the initial pyinstrument frame
    def is_initial_pyinstrument_frame(frame: Frame):
        return (
            frame.file_path is not None
            and re.match(r".*pyinstrument[/\\]__main__.py", frame.file_path)
            and len(frame.children) > 0
        )

    def is_exec_frame(frame: Frame):
        return (
            frame.proportion_of_parent > 0.8
            and frame.file_path is not None
            and "<string>" in frame.file_path
            and len(frame.children) > 0
        )

    def is_runpy_frame(frame: Frame):
        return (
            frame.proportion_of_parent > 0.8
            and frame.file_path is not None
            and (re.match(r".*runpy.py", frame.file_path) or "<frozen runpy>" in frame.file_path)
            and len(frame.children) > 0
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    if not is_runpy_frame(result):
        return frame

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result
