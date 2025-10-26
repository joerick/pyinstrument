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


def x_remove_importlib__mutmut_orig(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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


def x_remove_importlib__mutmut_1(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is not None:
        return None

    for child in frame.children:
        remove_importlib(child, options=options)

        if child.file_path and "<frozen importlib._bootstrap" in child.file_path:
            delete_frame_from_tree(child, replace_with="children")

    return frame


def x_remove_importlib__mutmut_2(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(None, options=options)

        if child.file_path and "<frozen importlib._bootstrap" in child.file_path:
            delete_frame_from_tree(child, replace_with="children")

    return frame


def x_remove_importlib__mutmut_3(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(child, options=None)

        if child.file_path and "<frozen importlib._bootstrap" in child.file_path:
            delete_frame_from_tree(child, replace_with="children")

    return frame


def x_remove_importlib__mutmut_4(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(options=options)

        if child.file_path and "<frozen importlib._bootstrap" in child.file_path:
            delete_frame_from_tree(child, replace_with="children")

    return frame


def x_remove_importlib__mutmut_5(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(child, )

        if child.file_path and "<frozen importlib._bootstrap" in child.file_path:
            delete_frame_from_tree(child, replace_with="children")

    return frame


def x_remove_importlib__mutmut_6(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(child, options=options)

        if child.file_path or "<frozen importlib._bootstrap" in child.file_path:
            delete_frame_from_tree(child, replace_with="children")

    return frame


def x_remove_importlib__mutmut_7(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(child, options=options)

        if child.file_path and "XX<frozen importlib._bootstrapXX" in child.file_path:
            delete_frame_from_tree(child, replace_with="children")

    return frame


def x_remove_importlib__mutmut_8(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(child, options=options)

        if child.file_path and "<FROZEN IMPORTLIB._BOOTSTRAP" in child.file_path:
            delete_frame_from_tree(child, replace_with="children")

    return frame


def x_remove_importlib__mutmut_9(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(child, options=options)

        if child.file_path and "<frozen importlib._bootstrap" not in child.file_path:
            delete_frame_from_tree(child, replace_with="children")

    return frame


def x_remove_importlib__mutmut_10(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(child, options=options)

        if child.file_path and "<frozen importlib._bootstrap" in child.file_path:
            delete_frame_from_tree(None, replace_with="children")

    return frame


def x_remove_importlib__mutmut_11(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(child, options=options)

        if child.file_path and "<frozen importlib._bootstrap" in child.file_path:
            delete_frame_from_tree(child, replace_with=None)

    return frame


def x_remove_importlib__mutmut_12(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(child, options=options)

        if child.file_path and "<frozen importlib._bootstrap" in child.file_path:
            delete_frame_from_tree(replace_with="children")

    return frame


def x_remove_importlib__mutmut_13(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(child, options=options)

        if child.file_path and "<frozen importlib._bootstrap" in child.file_path:
            delete_frame_from_tree(child, )

    return frame


def x_remove_importlib__mutmut_14(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(child, options=options)

        if child.file_path and "<frozen importlib._bootstrap" in child.file_path:
            delete_frame_from_tree(child, replace_with="XXchildrenXX")

    return frame


def x_remove_importlib__mutmut_15(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes ``<frozen importlib._bootstrap`` frames that clutter the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_importlib(child, options=options)

        if child.file_path and "<frozen importlib._bootstrap" in child.file_path:
            delete_frame_from_tree(child, replace_with="CHILDREN")

    return frame

x_remove_importlib__mutmut_mutants : ClassVar[MutantDict] = {
'x_remove_importlib__mutmut_1': x_remove_importlib__mutmut_1, 
    'x_remove_importlib__mutmut_2': x_remove_importlib__mutmut_2, 
    'x_remove_importlib__mutmut_3': x_remove_importlib__mutmut_3, 
    'x_remove_importlib__mutmut_4': x_remove_importlib__mutmut_4, 
    'x_remove_importlib__mutmut_5': x_remove_importlib__mutmut_5, 
    'x_remove_importlib__mutmut_6': x_remove_importlib__mutmut_6, 
    'x_remove_importlib__mutmut_7': x_remove_importlib__mutmut_7, 
    'x_remove_importlib__mutmut_8': x_remove_importlib__mutmut_8, 
    'x_remove_importlib__mutmut_9': x_remove_importlib__mutmut_9, 
    'x_remove_importlib__mutmut_10': x_remove_importlib__mutmut_10, 
    'x_remove_importlib__mutmut_11': x_remove_importlib__mutmut_11, 
    'x_remove_importlib__mutmut_12': x_remove_importlib__mutmut_12, 
    'x_remove_importlib__mutmut_13': x_remove_importlib__mutmut_13, 
    'x_remove_importlib__mutmut_14': x_remove_importlib__mutmut_14, 
    'x_remove_importlib__mutmut_15': x_remove_importlib__mutmut_15
}

def remove_importlib(*args, **kwargs):
    result = _mutmut_trampoline(x_remove_importlib__mutmut_orig, x_remove_importlib__mutmut_mutants, args, kwargs)
    return result 

remove_importlib.__signature__ = _mutmut_signature(x_remove_importlib__mutmut_orig)
x_remove_importlib__mutmut_orig.__name__ = 'x_remove_importlib'


def x_remove_tracebackhide__mutmut_orig(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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


def x_remove_tracebackhide__mutmut_1(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes frames that have set a local `__tracebackhide__` (e.g.
    `__tracebackhide__ = True`), to hide them from the output.
    """
    if frame is not None:
        return None

    for child in frame.children:
        remove_tracebackhide(child, options=options)

        if child.has_tracebackhide:
            # remove this node, moving the self_time and children up to the parent
            delete_frame_from_tree(child, replace_with="children")

    return frame


def x_remove_tracebackhide__mutmut_2(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes frames that have set a local `__tracebackhide__` (e.g.
    `__tracebackhide__ = True`), to hide them from the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_tracebackhide(None, options=options)

        if child.has_tracebackhide:
            # remove this node, moving the self_time and children up to the parent
            delete_frame_from_tree(child, replace_with="children")

    return frame


def x_remove_tracebackhide__mutmut_3(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes frames that have set a local `__tracebackhide__` (e.g.
    `__tracebackhide__ = True`), to hide them from the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_tracebackhide(child, options=None)

        if child.has_tracebackhide:
            # remove this node, moving the self_time and children up to the parent
            delete_frame_from_tree(child, replace_with="children")

    return frame


def x_remove_tracebackhide__mutmut_4(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes frames that have set a local `__tracebackhide__` (e.g.
    `__tracebackhide__ = True`), to hide them from the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_tracebackhide(options=options)

        if child.has_tracebackhide:
            # remove this node, moving the self_time and children up to the parent
            delete_frame_from_tree(child, replace_with="children")

    return frame


def x_remove_tracebackhide__mutmut_5(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Removes frames that have set a local `__tracebackhide__` (e.g.
    `__tracebackhide__ = True`), to hide them from the output.
    """
    if frame is None:
        return None

    for child in frame.children:
        remove_tracebackhide(child, )

        if child.has_tracebackhide:
            # remove this node, moving the self_time and children up to the parent
            delete_frame_from_tree(child, replace_with="children")

    return frame


def x_remove_tracebackhide__mutmut_6(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            delete_frame_from_tree(None, replace_with="children")

    return frame


def x_remove_tracebackhide__mutmut_7(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            delete_frame_from_tree(child, replace_with=None)

    return frame


def x_remove_tracebackhide__mutmut_8(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            delete_frame_from_tree(replace_with="children")

    return frame


def x_remove_tracebackhide__mutmut_9(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            delete_frame_from_tree(child, )

    return frame


def x_remove_tracebackhide__mutmut_10(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            delete_frame_from_tree(child, replace_with="XXchildrenXX")

    return frame


def x_remove_tracebackhide__mutmut_11(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            delete_frame_from_tree(child, replace_with="CHILDREN")

    return frame

x_remove_tracebackhide__mutmut_mutants : ClassVar[MutantDict] = {
'x_remove_tracebackhide__mutmut_1': x_remove_tracebackhide__mutmut_1, 
    'x_remove_tracebackhide__mutmut_2': x_remove_tracebackhide__mutmut_2, 
    'x_remove_tracebackhide__mutmut_3': x_remove_tracebackhide__mutmut_3, 
    'x_remove_tracebackhide__mutmut_4': x_remove_tracebackhide__mutmut_4, 
    'x_remove_tracebackhide__mutmut_5': x_remove_tracebackhide__mutmut_5, 
    'x_remove_tracebackhide__mutmut_6': x_remove_tracebackhide__mutmut_6, 
    'x_remove_tracebackhide__mutmut_7': x_remove_tracebackhide__mutmut_7, 
    'x_remove_tracebackhide__mutmut_8': x_remove_tracebackhide__mutmut_8, 
    'x_remove_tracebackhide__mutmut_9': x_remove_tracebackhide__mutmut_9, 
    'x_remove_tracebackhide__mutmut_10': x_remove_tracebackhide__mutmut_10, 
    'x_remove_tracebackhide__mutmut_11': x_remove_tracebackhide__mutmut_11
}

def remove_tracebackhide(*args, **kwargs):
    result = _mutmut_trampoline(x_remove_tracebackhide__mutmut_orig, x_remove_tracebackhide__mutmut_mutants, args, kwargs)
    return result 

remove_tracebackhide.__signature__ = _mutmut_signature(x_remove_tracebackhide__mutmut_orig)
x_remove_tracebackhide__mutmut_orig.__name__ = 'x_remove_tracebackhide'


def x_aggregate_repeated_calls__mutmut_orig(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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


def x_aggregate_repeated_calls__mutmut_1(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Converts a timeline into a time-aggregate summary.

    Adds together calls along the same call stack, so that repeated calls appear as the same
    frame. Removes time-linearity - frames are sorted according to total time spent.

    Useful for outputs that display a summary of execution (e.g. text and html outputs)
    """
    if frame is not None:
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


def x_aggregate_repeated_calls__mutmut_2(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
    """
    Converts a timeline into a time-aggregate summary.

    Adds together calls along the same call stack, so that repeated calls appear as the same
    frame. Removes time-linearity - frames are sorted according to total time spent.

    Useful for outputs that display a summary of execution (e.g. text and html outputs)
    """
    if frame is None:
        return None

    children_by_identifier: dict[str, Frame] = None

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


def x_aggregate_repeated_calls__mutmut_3(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        if child.identifier not in children_by_identifier:
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


def x_aggregate_repeated_calls__mutmut_4(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            aggregate_frame = None

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


def x_aggregate_repeated_calls__mutmut_5(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            combine_frames(None, into=aggregate_frame)
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


def x_aggregate_repeated_calls__mutmut_6(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            combine_frames(child, into=None)
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


def x_aggregate_repeated_calls__mutmut_7(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            combine_frames(into=aggregate_frame)
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


def x_aggregate_repeated_calls__mutmut_8(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            combine_frames(child, )
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


def x_aggregate_repeated_calls__mutmut_9(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            children_by_identifier[child.identifier] = None

    # recurse into the children
    for child in frame.children:
        aggregate_repeated_calls(child, options=options)

    # sort the children by time
    # we use the internal _children list, because we need to mutate it
    frame._children.sort(key=lambda c: c.time, reverse=True)  # type: ignore # noqa

    return frame


def x_aggregate_repeated_calls__mutmut_10(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        aggregate_repeated_calls(None, options=options)

    # sort the children by time
    # we use the internal _children list, because we need to mutate it
    frame._children.sort(key=lambda c: c.time, reverse=True)  # type: ignore # noqa

    return frame


def x_aggregate_repeated_calls__mutmut_11(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        aggregate_repeated_calls(child, options=None)

    # sort the children by time
    # we use the internal _children list, because we need to mutate it
    frame._children.sort(key=lambda c: c.time, reverse=True)  # type: ignore # noqa

    return frame


def x_aggregate_repeated_calls__mutmut_12(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        aggregate_repeated_calls(options=options)

    # sort the children by time
    # we use the internal _children list, because we need to mutate it
    frame._children.sort(key=lambda c: c.time, reverse=True)  # type: ignore # noqa

    return frame


def x_aggregate_repeated_calls__mutmut_13(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        aggregate_repeated_calls(child, )

    # sort the children by time
    # we use the internal _children list, because we need to mutate it
    frame._children.sort(key=lambda c: c.time, reverse=True)  # type: ignore # noqa

    return frame


def x_aggregate_repeated_calls__mutmut_14(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
    frame._children.sort(key=None, reverse=True)  # type: ignore # noqa

    return frame


def x_aggregate_repeated_calls__mutmut_15(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
    frame._children.sort(key=lambda c: c.time, reverse=None)  # type: ignore # noqa

    return frame


def x_aggregate_repeated_calls__mutmut_16(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
    frame._children.sort(reverse=True)  # type: ignore # noqa

    return frame


def x_aggregate_repeated_calls__mutmut_17(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
    frame._children.sort(key=lambda c: c.time, )  # type: ignore # noqa

    return frame


def x_aggregate_repeated_calls__mutmut_18(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
    frame._children.sort(key=lambda c: None, reverse=True)  # type: ignore # noqa

    return frame


def x_aggregate_repeated_calls__mutmut_19(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
    frame._children.sort(key=lambda c: c.time, reverse=False)  # type: ignore # noqa

    return frame

x_aggregate_repeated_calls__mutmut_mutants : ClassVar[MutantDict] = {
'x_aggregate_repeated_calls__mutmut_1': x_aggregate_repeated_calls__mutmut_1, 
    'x_aggregate_repeated_calls__mutmut_2': x_aggregate_repeated_calls__mutmut_2, 
    'x_aggregate_repeated_calls__mutmut_3': x_aggregate_repeated_calls__mutmut_3, 
    'x_aggregate_repeated_calls__mutmut_4': x_aggregate_repeated_calls__mutmut_4, 
    'x_aggregate_repeated_calls__mutmut_5': x_aggregate_repeated_calls__mutmut_5, 
    'x_aggregate_repeated_calls__mutmut_6': x_aggregate_repeated_calls__mutmut_6, 
    'x_aggregate_repeated_calls__mutmut_7': x_aggregate_repeated_calls__mutmut_7, 
    'x_aggregate_repeated_calls__mutmut_8': x_aggregate_repeated_calls__mutmut_8, 
    'x_aggregate_repeated_calls__mutmut_9': x_aggregate_repeated_calls__mutmut_9, 
    'x_aggregate_repeated_calls__mutmut_10': x_aggregate_repeated_calls__mutmut_10, 
    'x_aggregate_repeated_calls__mutmut_11': x_aggregate_repeated_calls__mutmut_11, 
    'x_aggregate_repeated_calls__mutmut_12': x_aggregate_repeated_calls__mutmut_12, 
    'x_aggregate_repeated_calls__mutmut_13': x_aggregate_repeated_calls__mutmut_13, 
    'x_aggregate_repeated_calls__mutmut_14': x_aggregate_repeated_calls__mutmut_14, 
    'x_aggregate_repeated_calls__mutmut_15': x_aggregate_repeated_calls__mutmut_15, 
    'x_aggregate_repeated_calls__mutmut_16': x_aggregate_repeated_calls__mutmut_16, 
    'x_aggregate_repeated_calls__mutmut_17': x_aggregate_repeated_calls__mutmut_17, 
    'x_aggregate_repeated_calls__mutmut_18': x_aggregate_repeated_calls__mutmut_18, 
    'x_aggregate_repeated_calls__mutmut_19': x_aggregate_repeated_calls__mutmut_19
}

def aggregate_repeated_calls(*args, **kwargs):
    result = _mutmut_trampoline(x_aggregate_repeated_calls__mutmut_orig, x_aggregate_repeated_calls__mutmut_mutants, args, kwargs)
    return result 

aggregate_repeated_calls.__signature__ = _mutmut_signature(x_aggregate_repeated_calls__mutmut_orig)
x_aggregate_repeated_calls__mutmut_orig.__name__ = 'x_aggregate_repeated_calls'


def x_group_library_frames_processor__mutmut_orig(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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


def x_group_library_frames_processor__mutmut_1(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
    if frame is not None:
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


def x_group_library_frames_processor__mutmut_2(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

    hide_regex: str | None = None
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


def x_group_library_frames_processor__mutmut_3(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

    hide_regex: str | None = options.get(None)
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


def x_group_library_frames_processor__mutmut_4(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

    hide_regex: str | None = options.get("XXhide_regexXX")
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


def x_group_library_frames_processor__mutmut_5(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

    hide_regex: str | None = options.get("HIDE_REGEX")
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


def x_group_library_frames_processor__mutmut_6(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
    show_regex: str | None = None

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


def x_group_library_frames_processor__mutmut_7(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
    show_regex: str | None = options.get(None)

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


def x_group_library_frames_processor__mutmut_8(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
    show_regex: str | None = options.get("XXshow_regexXX")

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


def x_group_library_frames_processor__mutmut_9(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
    show_regex: str | None = options.get("SHOW_REGEX")

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


def x_group_library_frames_processor__mutmut_10(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        frame_file_path = None

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


def x_group_library_frames_processor__mutmut_11(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        frame_file_path = frame.file_path and ""

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


def x_group_library_frames_processor__mutmut_12(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        frame_file_path = frame.file_path or "XXXX"

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


def x_group_library_frames_processor__mutmut_13(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

        should_show = None
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


def x_group_library_frames_processor__mutmut_14(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

        should_show = (show_regex is not None) or re.match(show_regex, frame_file_path)
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


def x_group_library_frames_processor__mutmut_15(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

        should_show = (show_regex is None) and re.match(show_regex, frame_file_path)
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


def x_group_library_frames_processor__mutmut_16(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

        should_show = (show_regex is not None) and re.match(None, frame_file_path)
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


def x_group_library_frames_processor__mutmut_17(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

        should_show = (show_regex is not None) and re.match(show_regex, None)
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


def x_group_library_frames_processor__mutmut_18(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

        should_show = (show_regex is not None) and re.match(frame_file_path)
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


def x_group_library_frames_processor__mutmut_19(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

        should_show = (show_regex is not None) and re.match(show_regex, )
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


def x_group_library_frames_processor__mutmut_20(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        should_hide = None

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


def x_group_library_frames_processor__mutmut_21(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        should_hide = (hide_regex is not None) or re.match(hide_regex, frame_file_path)

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


def x_group_library_frames_processor__mutmut_22(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        should_hide = (hide_regex is None) and re.match(hide_regex, frame_file_path)

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


def x_group_library_frames_processor__mutmut_23(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        should_hide = (hide_regex is not None) and re.match(None, frame_file_path)

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


def x_group_library_frames_processor__mutmut_24(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        should_hide = (hide_regex is not None) and re.match(hide_regex, None)

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


def x_group_library_frames_processor__mutmut_25(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        should_hide = (hide_regex is not None) and re.match(frame_file_path)

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


def x_group_library_frames_processor__mutmut_26(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        should_hide = (hide_regex is not None) and re.match(hide_regex, )

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


def x_group_library_frames_processor__mutmut_27(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            return True
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


def x_group_library_frames_processor__mutmut_28(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            return False

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


def x_group_library_frames_processor__mutmut_29(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

        return frame.is_application_code

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


def x_group_library_frames_processor__mutmut_30(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        group.add_frame(None)
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


def x_group_library_frames_processor__mutmut_31(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            if should_be_hidden(None):
                add_frames_to_group(child, group)

    for child in frame.children:
        if not child.group and (
            should_be_hidden(child) and any(should_be_hidden(cc) for cc in child.children)
        ):
            group = FrameGroup(child)
            add_frames_to_group(child, group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_32(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
                add_frames_to_group(None, group)

    for child in frame.children:
        if not child.group and (
            should_be_hidden(child) and any(should_be_hidden(cc) for cc in child.children)
        ):
            group = FrameGroup(child)
            add_frames_to_group(child, group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_33(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
                add_frames_to_group(child, None)

    for child in frame.children:
        if not child.group and (
            should_be_hidden(child) and any(should_be_hidden(cc) for cc in child.children)
        ):
            group = FrameGroup(child)
            add_frames_to_group(child, group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_34(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
                add_frames_to_group(group)

    for child in frame.children:
        if not child.group and (
            should_be_hidden(child) and any(should_be_hidden(cc) for cc in child.children)
        ):
            group = FrameGroup(child)
            add_frames_to_group(child, group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_35(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
                add_frames_to_group(child, )

    for child in frame.children:
        if not child.group and (
            should_be_hidden(child) and any(should_be_hidden(cc) for cc in child.children)
        ):
            group = FrameGroup(child)
            add_frames_to_group(child, group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_36(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        if not child.group or (
            should_be_hidden(child) and any(should_be_hidden(cc) for cc in child.children)
        ):
            group = FrameGroup(child)
            add_frames_to_group(child, group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_37(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
        if child.group and (
            should_be_hidden(child) and any(should_be_hidden(cc) for cc in child.children)
        ):
            group = FrameGroup(child)
            add_frames_to_group(child, group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_38(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            should_be_hidden(child) or any(should_be_hidden(cc) for cc in child.children)
        ):
            group = FrameGroup(child)
            add_frames_to_group(child, group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_39(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            should_be_hidden(None) and any(should_be_hidden(cc) for cc in child.children)
        ):
            group = FrameGroup(child)
            add_frames_to_group(child, group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_40(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            should_be_hidden(child) and any(None)
        ):
            group = FrameGroup(child)
            add_frames_to_group(child, group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_41(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            should_be_hidden(child) and any(should_be_hidden(None) for cc in child.children)
        ):
            group = FrameGroup(child)
            add_frames_to_group(child, group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_42(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            group = None
            add_frames_to_group(child, group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_43(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            group = FrameGroup(None)
            add_frames_to_group(child, group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_44(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            add_frames_to_group(None, group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_45(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            add_frames_to_group(child, None)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_46(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            add_frames_to_group(group)

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_47(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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
            add_frames_to_group(child, )

        group_library_frames_processor(child, options=options)

    return frame


def x_group_library_frames_processor__mutmut_48(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

        group_library_frames_processor(None, options=options)

    return frame


def x_group_library_frames_processor__mutmut_49(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

        group_library_frames_processor(child, options=None)

    return frame


def x_group_library_frames_processor__mutmut_50(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

        group_library_frames_processor(options=options)

    return frame


def x_group_library_frames_processor__mutmut_51(frame: Frame | None, options: ProcessorOptions) -> Frame | None:
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

        group_library_frames_processor(child, )

    return frame

x_group_library_frames_processor__mutmut_mutants : ClassVar[MutantDict] = {
'x_group_library_frames_processor__mutmut_1': x_group_library_frames_processor__mutmut_1, 
    'x_group_library_frames_processor__mutmut_2': x_group_library_frames_processor__mutmut_2, 
    'x_group_library_frames_processor__mutmut_3': x_group_library_frames_processor__mutmut_3, 
    'x_group_library_frames_processor__mutmut_4': x_group_library_frames_processor__mutmut_4, 
    'x_group_library_frames_processor__mutmut_5': x_group_library_frames_processor__mutmut_5, 
    'x_group_library_frames_processor__mutmut_6': x_group_library_frames_processor__mutmut_6, 
    'x_group_library_frames_processor__mutmut_7': x_group_library_frames_processor__mutmut_7, 
    'x_group_library_frames_processor__mutmut_8': x_group_library_frames_processor__mutmut_8, 
    'x_group_library_frames_processor__mutmut_9': x_group_library_frames_processor__mutmut_9, 
    'x_group_library_frames_processor__mutmut_10': x_group_library_frames_processor__mutmut_10, 
    'x_group_library_frames_processor__mutmut_11': x_group_library_frames_processor__mutmut_11, 
    'x_group_library_frames_processor__mutmut_12': x_group_library_frames_processor__mutmut_12, 
    'x_group_library_frames_processor__mutmut_13': x_group_library_frames_processor__mutmut_13, 
    'x_group_library_frames_processor__mutmut_14': x_group_library_frames_processor__mutmut_14, 
    'x_group_library_frames_processor__mutmut_15': x_group_library_frames_processor__mutmut_15, 
    'x_group_library_frames_processor__mutmut_16': x_group_library_frames_processor__mutmut_16, 
    'x_group_library_frames_processor__mutmut_17': x_group_library_frames_processor__mutmut_17, 
    'x_group_library_frames_processor__mutmut_18': x_group_library_frames_processor__mutmut_18, 
    'x_group_library_frames_processor__mutmut_19': x_group_library_frames_processor__mutmut_19, 
    'x_group_library_frames_processor__mutmut_20': x_group_library_frames_processor__mutmut_20, 
    'x_group_library_frames_processor__mutmut_21': x_group_library_frames_processor__mutmut_21, 
    'x_group_library_frames_processor__mutmut_22': x_group_library_frames_processor__mutmut_22, 
    'x_group_library_frames_processor__mutmut_23': x_group_library_frames_processor__mutmut_23, 
    'x_group_library_frames_processor__mutmut_24': x_group_library_frames_processor__mutmut_24, 
    'x_group_library_frames_processor__mutmut_25': x_group_library_frames_processor__mutmut_25, 
    'x_group_library_frames_processor__mutmut_26': x_group_library_frames_processor__mutmut_26, 
    'x_group_library_frames_processor__mutmut_27': x_group_library_frames_processor__mutmut_27, 
    'x_group_library_frames_processor__mutmut_28': x_group_library_frames_processor__mutmut_28, 
    'x_group_library_frames_processor__mutmut_29': x_group_library_frames_processor__mutmut_29, 
    'x_group_library_frames_processor__mutmut_30': x_group_library_frames_processor__mutmut_30, 
    'x_group_library_frames_processor__mutmut_31': x_group_library_frames_processor__mutmut_31, 
    'x_group_library_frames_processor__mutmut_32': x_group_library_frames_processor__mutmut_32, 
    'x_group_library_frames_processor__mutmut_33': x_group_library_frames_processor__mutmut_33, 
    'x_group_library_frames_processor__mutmut_34': x_group_library_frames_processor__mutmut_34, 
    'x_group_library_frames_processor__mutmut_35': x_group_library_frames_processor__mutmut_35, 
    'x_group_library_frames_processor__mutmut_36': x_group_library_frames_processor__mutmut_36, 
    'x_group_library_frames_processor__mutmut_37': x_group_library_frames_processor__mutmut_37, 
    'x_group_library_frames_processor__mutmut_38': x_group_library_frames_processor__mutmut_38, 
    'x_group_library_frames_processor__mutmut_39': x_group_library_frames_processor__mutmut_39, 
    'x_group_library_frames_processor__mutmut_40': x_group_library_frames_processor__mutmut_40, 
    'x_group_library_frames_processor__mutmut_41': x_group_library_frames_processor__mutmut_41, 
    'x_group_library_frames_processor__mutmut_42': x_group_library_frames_processor__mutmut_42, 
    'x_group_library_frames_processor__mutmut_43': x_group_library_frames_processor__mutmut_43, 
    'x_group_library_frames_processor__mutmut_44': x_group_library_frames_processor__mutmut_44, 
    'x_group_library_frames_processor__mutmut_45': x_group_library_frames_processor__mutmut_45, 
    'x_group_library_frames_processor__mutmut_46': x_group_library_frames_processor__mutmut_46, 
    'x_group_library_frames_processor__mutmut_47': x_group_library_frames_processor__mutmut_47, 
    'x_group_library_frames_processor__mutmut_48': x_group_library_frames_processor__mutmut_48, 
    'x_group_library_frames_processor__mutmut_49': x_group_library_frames_processor__mutmut_49, 
    'x_group_library_frames_processor__mutmut_50': x_group_library_frames_processor__mutmut_50, 
    'x_group_library_frames_processor__mutmut_51': x_group_library_frames_processor__mutmut_51
}

def group_library_frames_processor(*args, **kwargs):
    result = _mutmut_trampoline(x_group_library_frames_processor__mutmut_orig, x_group_library_frames_processor__mutmut_mutants, args, kwargs)
    return result 

group_library_frames_processor.__signature__ = _mutmut_signature(x_group_library_frames_processor__mutmut_orig)
x_group_library_frames_processor__mutmut_orig.__name__ = 'x_group_library_frames_processor'


def x_merge_consecutive_self_time__mutmut_orig(
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


def x_merge_consecutive_self_time__mutmut_1(
    frame: Frame | None, options: ProcessorOptions, recursive: bool = False
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


def x_merge_consecutive_self_time__mutmut_2(
    frame: Frame | None, options: ProcessorOptions, recursive: bool = True
) -> Frame | None:
    """
    Combines consecutive 'self time' frames.
    """
    if frame is not None:
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


def x_merge_consecutive_self_time__mutmut_3(
    frame: Frame | None, options: ProcessorOptions, recursive: bool = True
) -> Frame | None:
    """
    Combines consecutive 'self time' frames.
    """
    if frame is None:
        return None

    previous_self_time_frame = ""

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


def x_merge_consecutive_self_time__mutmut_4(
    frame: Frame | None, options: ProcessorOptions, recursive: bool = True
) -> Frame | None:
    """
    Combines consecutive 'self time' frames.
    """
    if frame is None:
        return None

    previous_self_time_frame = None

    for child in frame.children:
        if child.identifier != SELF_TIME_FRAME_IDENTIFIER:
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


def x_merge_consecutive_self_time__mutmut_5(
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
                previous_self_time_frame.time = child.time
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


def x_merge_consecutive_self_time__mutmut_6(
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
                previous_self_time_frame.time -= child.time
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


def x_merge_consecutive_self_time__mutmut_7(
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
                previous_self_time_frame = None
        else:
            previous_self_time_frame = None

    if recursive:
        for child in frame.children:
            merge_consecutive_self_time(child, options=options, recursive=True)

    return frame


def x_merge_consecutive_self_time__mutmut_8(
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
            previous_self_time_frame = ""

    if recursive:
        for child in frame.children:
            merge_consecutive_self_time(child, options=options, recursive=True)

    return frame


def x_merge_consecutive_self_time__mutmut_9(
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
            merge_consecutive_self_time(None, options=options, recursive=True)

    return frame


def x_merge_consecutive_self_time__mutmut_10(
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
            merge_consecutive_self_time(child, options=None, recursive=True)

    return frame


def x_merge_consecutive_self_time__mutmut_11(
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
            merge_consecutive_self_time(child, options=options, recursive=None)

    return frame


def x_merge_consecutive_self_time__mutmut_12(
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
            merge_consecutive_self_time(options=options, recursive=True)

    return frame


def x_merge_consecutive_self_time__mutmut_13(
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
            merge_consecutive_self_time(child, recursive=True)

    return frame


def x_merge_consecutive_self_time__mutmut_14(
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
            merge_consecutive_self_time(child, options=options, )

    return frame


def x_merge_consecutive_self_time__mutmut_15(
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
            merge_consecutive_self_time(child, options=options, recursive=False)

    return frame

x_merge_consecutive_self_time__mutmut_mutants : ClassVar[MutantDict] = {
'x_merge_consecutive_self_time__mutmut_1': x_merge_consecutive_self_time__mutmut_1, 
    'x_merge_consecutive_self_time__mutmut_2': x_merge_consecutive_self_time__mutmut_2, 
    'x_merge_consecutive_self_time__mutmut_3': x_merge_consecutive_self_time__mutmut_3, 
    'x_merge_consecutive_self_time__mutmut_4': x_merge_consecutive_self_time__mutmut_4, 
    'x_merge_consecutive_self_time__mutmut_5': x_merge_consecutive_self_time__mutmut_5, 
    'x_merge_consecutive_self_time__mutmut_6': x_merge_consecutive_self_time__mutmut_6, 
    'x_merge_consecutive_self_time__mutmut_7': x_merge_consecutive_self_time__mutmut_7, 
    'x_merge_consecutive_self_time__mutmut_8': x_merge_consecutive_self_time__mutmut_8, 
    'x_merge_consecutive_self_time__mutmut_9': x_merge_consecutive_self_time__mutmut_9, 
    'x_merge_consecutive_self_time__mutmut_10': x_merge_consecutive_self_time__mutmut_10, 
    'x_merge_consecutive_self_time__mutmut_11': x_merge_consecutive_self_time__mutmut_11, 
    'x_merge_consecutive_self_time__mutmut_12': x_merge_consecutive_self_time__mutmut_12, 
    'x_merge_consecutive_self_time__mutmut_13': x_merge_consecutive_self_time__mutmut_13, 
    'x_merge_consecutive_self_time__mutmut_14': x_merge_consecutive_self_time__mutmut_14, 
    'x_merge_consecutive_self_time__mutmut_15': x_merge_consecutive_self_time__mutmut_15
}

def merge_consecutive_self_time(*args, **kwargs):
    result = _mutmut_trampoline(x_merge_consecutive_self_time__mutmut_orig, x_merge_consecutive_self_time__mutmut_mutants, args, kwargs)
    return result 

merge_consecutive_self_time.__signature__ = _mutmut_signature(x_merge_consecutive_self_time__mutmut_orig)
x_merge_consecutive_self_time__mutmut_orig.__name__ = 'x_merge_consecutive_self_time'


def x_remove_unnecessary_self_time_nodes__mutmut_orig(
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


def x_remove_unnecessary_self_time_nodes__mutmut_1(
    frame: Frame | None, options: ProcessorOptions
) -> Frame | None:
    """
    When a frame has only one child, and that is a self-time frame, remove
    that node and move the time to parent, since it's unnecessary - it
    clutters the output and offers no additional information.
    """
    if frame is not None:
        return None

    if len(frame.children) == 1 and frame.children[0].identifier == SELF_TIME_FRAME_IDENTIFIER:
        delete_frame_from_tree(frame.children[0], replace_with="nothing")

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_2(
    frame: Frame | None, options: ProcessorOptions
) -> Frame | None:
    """
    When a frame has only one child, and that is a self-time frame, remove
    that node and move the time to parent, since it's unnecessary - it
    clutters the output and offers no additional information.
    """
    if frame is None:
        return None

    if len(frame.children) == 1 or frame.children[0].identifier == SELF_TIME_FRAME_IDENTIFIER:
        delete_frame_from_tree(frame.children[0], replace_with="nothing")

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_3(
    frame: Frame | None, options: ProcessorOptions
) -> Frame | None:
    """
    When a frame has only one child, and that is a self-time frame, remove
    that node and move the time to parent, since it's unnecessary - it
    clutters the output and offers no additional information.
    """
    if frame is None:
        return None

    if len(frame.children) != 1 and frame.children[0].identifier == SELF_TIME_FRAME_IDENTIFIER:
        delete_frame_from_tree(frame.children[0], replace_with="nothing")

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_4(
    frame: Frame | None, options: ProcessorOptions
) -> Frame | None:
    """
    When a frame has only one child, and that is a self-time frame, remove
    that node and move the time to parent, since it's unnecessary - it
    clutters the output and offers no additional information.
    """
    if frame is None:
        return None

    if len(frame.children) == 2 and frame.children[0].identifier == SELF_TIME_FRAME_IDENTIFIER:
        delete_frame_from_tree(frame.children[0], replace_with="nothing")

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_5(
    frame: Frame | None, options: ProcessorOptions
) -> Frame | None:
    """
    When a frame has only one child, and that is a self-time frame, remove
    that node and move the time to parent, since it's unnecessary - it
    clutters the output and offers no additional information.
    """
    if frame is None:
        return None

    if len(frame.children) == 1 and frame.children[1].identifier == SELF_TIME_FRAME_IDENTIFIER:
        delete_frame_from_tree(frame.children[0], replace_with="nothing")

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_6(
    frame: Frame | None, options: ProcessorOptions
) -> Frame | None:
    """
    When a frame has only one child, and that is a self-time frame, remove
    that node and move the time to parent, since it's unnecessary - it
    clutters the output and offers no additional information.
    """
    if frame is None:
        return None

    if len(frame.children) == 1 and frame.children[0].identifier != SELF_TIME_FRAME_IDENTIFIER:
        delete_frame_from_tree(frame.children[0], replace_with="nothing")

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_7(
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
        delete_frame_from_tree(None, replace_with="nothing")

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_8(
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
        delete_frame_from_tree(frame.children[0], replace_with=None)

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_9(
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
        delete_frame_from_tree(replace_with="nothing")

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_10(
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
        delete_frame_from_tree(frame.children[0], )

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_11(
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
        delete_frame_from_tree(frame.children[1], replace_with="nothing")

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_12(
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
        delete_frame_from_tree(frame.children[0], replace_with="XXnothingXX")

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_13(
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
        delete_frame_from_tree(frame.children[0], replace_with="NOTHING")

    for child in frame.children:
        remove_unnecessary_self_time_nodes(child, options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_14(
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
        remove_unnecessary_self_time_nodes(None, options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_15(
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
        remove_unnecessary_self_time_nodes(child, options=None)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_16(
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
        remove_unnecessary_self_time_nodes(options=options)

    return frame


def x_remove_unnecessary_self_time_nodes__mutmut_17(
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
        remove_unnecessary_self_time_nodes(child, )

    return frame

x_remove_unnecessary_self_time_nodes__mutmut_mutants : ClassVar[MutantDict] = {
'x_remove_unnecessary_self_time_nodes__mutmut_1': x_remove_unnecessary_self_time_nodes__mutmut_1, 
    'x_remove_unnecessary_self_time_nodes__mutmut_2': x_remove_unnecessary_self_time_nodes__mutmut_2, 
    'x_remove_unnecessary_self_time_nodes__mutmut_3': x_remove_unnecessary_self_time_nodes__mutmut_3, 
    'x_remove_unnecessary_self_time_nodes__mutmut_4': x_remove_unnecessary_self_time_nodes__mutmut_4, 
    'x_remove_unnecessary_self_time_nodes__mutmut_5': x_remove_unnecessary_self_time_nodes__mutmut_5, 
    'x_remove_unnecessary_self_time_nodes__mutmut_6': x_remove_unnecessary_self_time_nodes__mutmut_6, 
    'x_remove_unnecessary_self_time_nodes__mutmut_7': x_remove_unnecessary_self_time_nodes__mutmut_7, 
    'x_remove_unnecessary_self_time_nodes__mutmut_8': x_remove_unnecessary_self_time_nodes__mutmut_8, 
    'x_remove_unnecessary_self_time_nodes__mutmut_9': x_remove_unnecessary_self_time_nodes__mutmut_9, 
    'x_remove_unnecessary_self_time_nodes__mutmut_10': x_remove_unnecessary_self_time_nodes__mutmut_10, 
    'x_remove_unnecessary_self_time_nodes__mutmut_11': x_remove_unnecessary_self_time_nodes__mutmut_11, 
    'x_remove_unnecessary_self_time_nodes__mutmut_12': x_remove_unnecessary_self_time_nodes__mutmut_12, 
    'x_remove_unnecessary_self_time_nodes__mutmut_13': x_remove_unnecessary_self_time_nodes__mutmut_13, 
    'x_remove_unnecessary_self_time_nodes__mutmut_14': x_remove_unnecessary_self_time_nodes__mutmut_14, 
    'x_remove_unnecessary_self_time_nodes__mutmut_15': x_remove_unnecessary_self_time_nodes__mutmut_15, 
    'x_remove_unnecessary_self_time_nodes__mutmut_16': x_remove_unnecessary_self_time_nodes__mutmut_16, 
    'x_remove_unnecessary_self_time_nodes__mutmut_17': x_remove_unnecessary_self_time_nodes__mutmut_17
}

def remove_unnecessary_self_time_nodes(*args, **kwargs):
    result = _mutmut_trampoline(x_remove_unnecessary_self_time_nodes__mutmut_orig, x_remove_unnecessary_self_time_nodes__mutmut_mutants, args, kwargs)
    return result 

remove_unnecessary_self_time_nodes.__signature__ = _mutmut_signature(x_remove_unnecessary_self_time_nodes__mutmut_orig)
x_remove_unnecessary_self_time_nodes__mutmut_orig.__name__ = 'x_remove_unnecessary_self_time_nodes'


def x_remove_irrelevant_nodes__mutmut_orig(
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


def x_remove_irrelevant_nodes__mutmut_1(
    frame: Frame | None, options: ProcessorOptions, total_time: float | None = None
) -> Frame | None:
    """
    Remove nodes that represent less than e.g. 1% of the output. Options:

    ``filter_threshold``
      sets the minimum duration of a frame to be included in the output.
      Default: 0.01.
    """
    if frame is not None:
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


def x_remove_irrelevant_nodes__mutmut_2(
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

    if total_time is not None:
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


def x_remove_irrelevant_nodes__mutmut_3(
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
        total_time = None

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


def x_remove_irrelevant_nodes__mutmut_4(
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
        if total_time < 0:
            total_time = 1e-44

    filter_threshold = options.get("filter_threshold", 0.01)

    for child in frame.children:
        proportion_of_total = child.time / total_time

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_5(
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
        if total_time <= 1:
            total_time = 1e-44

    filter_threshold = options.get("filter_threshold", 0.01)

    for child in frame.children:
        proportion_of_total = child.time / total_time

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_6(
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
            total_time = None

    filter_threshold = options.get("filter_threshold", 0.01)

    for child in frame.children:
        proportion_of_total = child.time / total_time

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_7(
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
            total_time = 1.0

    filter_threshold = options.get("filter_threshold", 0.01)

    for child in frame.children:
        proportion_of_total = child.time / total_time

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_8(
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

    filter_threshold = None

    for child in frame.children:
        proportion_of_total = child.time / total_time

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_9(
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

    filter_threshold = options.get(None, 0.01)

    for child in frame.children:
        proportion_of_total = child.time / total_time

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_10(
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

    filter_threshold = options.get("filter_threshold", None)

    for child in frame.children:
        proportion_of_total = child.time / total_time

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_11(
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

    filter_threshold = options.get(0.01)

    for child in frame.children:
        proportion_of_total = child.time / total_time

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_12(
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

    filter_threshold = options.get("filter_threshold", )

    for child in frame.children:
        proportion_of_total = child.time / total_time

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_13(
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

    filter_threshold = options.get("XXfilter_thresholdXX", 0.01)

    for child in frame.children:
        proportion_of_total = child.time / total_time

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_14(
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

    filter_threshold = options.get("FILTER_THRESHOLD", 0.01)

    for child in frame.children:
        proportion_of_total = child.time / total_time

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_15(
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

    filter_threshold = options.get("filter_threshold", 1.01)

    for child in frame.children:
        proportion_of_total = child.time / total_time

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_16(
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
        proportion_of_total = None

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_17(
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
        proportion_of_total = child.time * total_time

        if proportion_of_total < filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_18(
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

        if proportion_of_total <= filter_threshold:
            delete_frame_from_tree(child, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_19(
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
            delete_frame_from_tree(None, replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_20(
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
            delete_frame_from_tree(child, replace_with=None)

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_21(
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
            delete_frame_from_tree(replace_with="nothing")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_22(
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
            delete_frame_from_tree(child, )

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_23(
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
            delete_frame_from_tree(child, replace_with="XXnothingXX")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_24(
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
            delete_frame_from_tree(child, replace_with="NOTHING")

    for child in frame.children:
        remove_irrelevant_nodes(child, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_25(
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
        remove_irrelevant_nodes(None, options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_26(
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
        remove_irrelevant_nodes(child, options=None, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_27(
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
        remove_irrelevant_nodes(child, options=options, total_time=None)

    return frame


def x_remove_irrelevant_nodes__mutmut_28(
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
        remove_irrelevant_nodes(options=options, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_29(
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
        remove_irrelevant_nodes(child, total_time=total_time)

    return frame


def x_remove_irrelevant_nodes__mutmut_30(
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
        remove_irrelevant_nodes(child, options=options, )

    return frame

x_remove_irrelevant_nodes__mutmut_mutants : ClassVar[MutantDict] = {
'x_remove_irrelevant_nodes__mutmut_1': x_remove_irrelevant_nodes__mutmut_1, 
    'x_remove_irrelevant_nodes__mutmut_2': x_remove_irrelevant_nodes__mutmut_2, 
    'x_remove_irrelevant_nodes__mutmut_3': x_remove_irrelevant_nodes__mutmut_3, 
    'x_remove_irrelevant_nodes__mutmut_4': x_remove_irrelevant_nodes__mutmut_4, 
    'x_remove_irrelevant_nodes__mutmut_5': x_remove_irrelevant_nodes__mutmut_5, 
    'x_remove_irrelevant_nodes__mutmut_6': x_remove_irrelevant_nodes__mutmut_6, 
    'x_remove_irrelevant_nodes__mutmut_7': x_remove_irrelevant_nodes__mutmut_7, 
    'x_remove_irrelevant_nodes__mutmut_8': x_remove_irrelevant_nodes__mutmut_8, 
    'x_remove_irrelevant_nodes__mutmut_9': x_remove_irrelevant_nodes__mutmut_9, 
    'x_remove_irrelevant_nodes__mutmut_10': x_remove_irrelevant_nodes__mutmut_10, 
    'x_remove_irrelevant_nodes__mutmut_11': x_remove_irrelevant_nodes__mutmut_11, 
    'x_remove_irrelevant_nodes__mutmut_12': x_remove_irrelevant_nodes__mutmut_12, 
    'x_remove_irrelevant_nodes__mutmut_13': x_remove_irrelevant_nodes__mutmut_13, 
    'x_remove_irrelevant_nodes__mutmut_14': x_remove_irrelevant_nodes__mutmut_14, 
    'x_remove_irrelevant_nodes__mutmut_15': x_remove_irrelevant_nodes__mutmut_15, 
    'x_remove_irrelevant_nodes__mutmut_16': x_remove_irrelevant_nodes__mutmut_16, 
    'x_remove_irrelevant_nodes__mutmut_17': x_remove_irrelevant_nodes__mutmut_17, 
    'x_remove_irrelevant_nodes__mutmut_18': x_remove_irrelevant_nodes__mutmut_18, 
    'x_remove_irrelevant_nodes__mutmut_19': x_remove_irrelevant_nodes__mutmut_19, 
    'x_remove_irrelevant_nodes__mutmut_20': x_remove_irrelevant_nodes__mutmut_20, 
    'x_remove_irrelevant_nodes__mutmut_21': x_remove_irrelevant_nodes__mutmut_21, 
    'x_remove_irrelevant_nodes__mutmut_22': x_remove_irrelevant_nodes__mutmut_22, 
    'x_remove_irrelevant_nodes__mutmut_23': x_remove_irrelevant_nodes__mutmut_23, 
    'x_remove_irrelevant_nodes__mutmut_24': x_remove_irrelevant_nodes__mutmut_24, 
    'x_remove_irrelevant_nodes__mutmut_25': x_remove_irrelevant_nodes__mutmut_25, 
    'x_remove_irrelevant_nodes__mutmut_26': x_remove_irrelevant_nodes__mutmut_26, 
    'x_remove_irrelevant_nodes__mutmut_27': x_remove_irrelevant_nodes__mutmut_27, 
    'x_remove_irrelevant_nodes__mutmut_28': x_remove_irrelevant_nodes__mutmut_28, 
    'x_remove_irrelevant_nodes__mutmut_29': x_remove_irrelevant_nodes__mutmut_29, 
    'x_remove_irrelevant_nodes__mutmut_30': x_remove_irrelevant_nodes__mutmut_30
}

def remove_irrelevant_nodes(*args, **kwargs):
    result = _mutmut_trampoline(x_remove_irrelevant_nodes__mutmut_orig, x_remove_irrelevant_nodes__mutmut_mutants, args, kwargs)
    return result 

remove_irrelevant_nodes.__signature__ = _mutmut_signature(x_remove_irrelevant_nodes__mutmut_orig)
x_remove_irrelevant_nodes__mutmut_orig.__name__ = 'x_remove_irrelevant_nodes'


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_orig(
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_1(
    frame: Frame | None, options: ProcessorOptions
) -> Frame | None:
    """
    The first few frames when using the command line are the __main__ of
    pyinstrument, the eval, and the 'runpy' module. I want to remove that from
    the output.
    """
    if frame is not None:
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_2(
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
            and re.match(r".*pyinstrument[/\\]__main__.py", frame.file_path) or len(frame.children) > 0
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_3(
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
            frame.file_path is not None or re.match(r".*pyinstrument[/\\]__main__.py", frame.file_path)
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_4(
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
            frame.file_path is None
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_5(
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
            and re.match(None, frame.file_path)
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_6(
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
            and re.match(r".*pyinstrument[/\\]__main__.py", None)
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_7(
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
            and re.match(frame.file_path)
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_8(
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
            and re.match(r".*pyinstrument[/\\]__main__.py", )
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_9(
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
            and re.match(r"XX.*pyinstrument[/\\]__main__.pyXX", frame.file_path)
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_10(
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_11(
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
            and re.match(r".*PYINSTRUMENT[/\\]__MAIN__.PY", frame.file_path)
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_12(
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
            and len(frame.children) >= 0
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_13(
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
            and len(frame.children) > 1
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_14(
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
            and "<string>" in frame.file_path or len(frame.children) > 0
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_15(
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
            and frame.file_path is not None or "<string>" in frame.file_path
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_16(
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
            frame.proportion_of_parent > 0.8 or frame.file_path is not None
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_17(
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
            frame.proportion_of_parent >= 0.8
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_18(
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
            frame.proportion_of_parent > 1.8
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_19(
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
            and frame.file_path is None
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_20(
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
            and "XX<string>XX" in frame.file_path
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_21(
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
            and "<STRING>" in frame.file_path
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_22(
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
            and "<string>" not in frame.file_path
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_23(
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
            and len(frame.children) >= 0
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_24(
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
            and len(frame.children) > 1
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_25(
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
            and (re.match(r".*runpy.py", frame.file_path) or "<frozen runpy>" in frame.file_path) or len(frame.children) > 0
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_26(
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
            and frame.file_path is not None or (re.match(r".*runpy.py", frame.file_path) or "<frozen runpy>" in frame.file_path)
            and len(frame.children) > 0
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_27(
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
            frame.proportion_of_parent > 0.8 or frame.file_path is not None
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_28(
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
            frame.proportion_of_parent >= 0.8
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_29(
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
            frame.proportion_of_parent > 1.8
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_30(
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
            and frame.file_path is None
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_31(
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
            and (re.match(r".*runpy.py", frame.file_path) and "<frozen runpy>" in frame.file_path)
            and len(frame.children) > 0
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_32(
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
            and (re.match(None, frame.file_path) or "<frozen runpy>" in frame.file_path)
            and len(frame.children) > 0
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_33(
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
            and (re.match(r".*runpy.py", None) or "<frozen runpy>" in frame.file_path)
            and len(frame.children) > 0
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_34(
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
            and (re.match(frame.file_path) or "<frozen runpy>" in frame.file_path)
            and len(frame.children) > 0
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_35(
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
            and (re.match(r".*runpy.py", ) or "<frozen runpy>" in frame.file_path)
            and len(frame.children) > 0
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_36(
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
            and (re.match(r"XX.*runpy.pyXX", frame.file_path) or "<frozen runpy>" in frame.file_path)
            and len(frame.children) > 0
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_37(
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_38(
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
            and (re.match(r".*RUNPY.PY", frame.file_path) or "<frozen runpy>" in frame.file_path)
            and len(frame.children) > 0
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_39(
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
            and (re.match(r".*runpy.py", frame.file_path) or "XX<frozen runpy>XX" in frame.file_path)
            and len(frame.children) > 0
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_40(
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
            and (re.match(r".*runpy.py", frame.file_path) or "<FROZEN RUNPY>" in frame.file_path)
            and len(frame.children) > 0
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_41(
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
            and (re.match(r".*runpy.py", frame.file_path) or "<frozen runpy>" not in frame.file_path)
            and len(frame.children) > 0
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_42(
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
            and len(frame.children) >= 0
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_43(
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
            and len(frame.children) > 1
        )

    result = frame

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_44(
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

    result = None

    if not is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_45(
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

    if is_initial_pyinstrument_frame(result):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_46(
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

    if not is_initial_pyinstrument_frame(None):
        return frame

    result = result.children[0]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_47(
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

    result = None

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_48(
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

    result = result.children[1]

    if not is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_49(
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

    if is_exec_frame(result):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_50(
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

    if not is_exec_frame(None):
        return frame

    result = result.children[0]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_51(
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

    result = None

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_52(
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

    result = result.children[1]

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_53(
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(None):
        result = result.children[0]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_54(
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = None

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result


# pylint: disable=W0613
def x_remove_first_pyinstrument_frames_processor__mutmut_55(
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

    # at this point we know we've matched the first few frames of a command
    # line invocation. We'll trim some runpy frames and return.

    while is_runpy_frame(result):
        result = result.children[1]

    # remove this frame from the parent to make it the new root frame
    result.remove_from_parent()

    return result

x_remove_first_pyinstrument_frames_processor__mutmut_mutants : ClassVar[MutantDict] = {
'x_remove_first_pyinstrument_frames_processor__mutmut_1': x_remove_first_pyinstrument_frames_processor__mutmut_1, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_2': x_remove_first_pyinstrument_frames_processor__mutmut_2, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_3': x_remove_first_pyinstrument_frames_processor__mutmut_3, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_4': x_remove_first_pyinstrument_frames_processor__mutmut_4, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_5': x_remove_first_pyinstrument_frames_processor__mutmut_5, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_6': x_remove_first_pyinstrument_frames_processor__mutmut_6, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_7': x_remove_first_pyinstrument_frames_processor__mutmut_7, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_8': x_remove_first_pyinstrument_frames_processor__mutmut_8, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_9': x_remove_first_pyinstrument_frames_processor__mutmut_9, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_10': x_remove_first_pyinstrument_frames_processor__mutmut_10, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_11': x_remove_first_pyinstrument_frames_processor__mutmut_11, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_12': x_remove_first_pyinstrument_frames_processor__mutmut_12, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_13': x_remove_first_pyinstrument_frames_processor__mutmut_13, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_14': x_remove_first_pyinstrument_frames_processor__mutmut_14, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_15': x_remove_first_pyinstrument_frames_processor__mutmut_15, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_16': x_remove_first_pyinstrument_frames_processor__mutmut_16, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_17': x_remove_first_pyinstrument_frames_processor__mutmut_17, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_18': x_remove_first_pyinstrument_frames_processor__mutmut_18, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_19': x_remove_first_pyinstrument_frames_processor__mutmut_19, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_20': x_remove_first_pyinstrument_frames_processor__mutmut_20, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_21': x_remove_first_pyinstrument_frames_processor__mutmut_21, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_22': x_remove_first_pyinstrument_frames_processor__mutmut_22, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_23': x_remove_first_pyinstrument_frames_processor__mutmut_23, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_24': x_remove_first_pyinstrument_frames_processor__mutmut_24, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_25': x_remove_first_pyinstrument_frames_processor__mutmut_25, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_26': x_remove_first_pyinstrument_frames_processor__mutmut_26, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_27': x_remove_first_pyinstrument_frames_processor__mutmut_27, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_28': x_remove_first_pyinstrument_frames_processor__mutmut_28, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_29': x_remove_first_pyinstrument_frames_processor__mutmut_29, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_30': x_remove_first_pyinstrument_frames_processor__mutmut_30, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_31': x_remove_first_pyinstrument_frames_processor__mutmut_31, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_32': x_remove_first_pyinstrument_frames_processor__mutmut_32, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_33': x_remove_first_pyinstrument_frames_processor__mutmut_33, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_34': x_remove_first_pyinstrument_frames_processor__mutmut_34, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_35': x_remove_first_pyinstrument_frames_processor__mutmut_35, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_36': x_remove_first_pyinstrument_frames_processor__mutmut_36, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_37': x_remove_first_pyinstrument_frames_processor__mutmut_37, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_38': x_remove_first_pyinstrument_frames_processor__mutmut_38, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_39': x_remove_first_pyinstrument_frames_processor__mutmut_39, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_40': x_remove_first_pyinstrument_frames_processor__mutmut_40, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_41': x_remove_first_pyinstrument_frames_processor__mutmut_41, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_42': x_remove_first_pyinstrument_frames_processor__mutmut_42, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_43': x_remove_first_pyinstrument_frames_processor__mutmut_43, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_44': x_remove_first_pyinstrument_frames_processor__mutmut_44, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_45': x_remove_first_pyinstrument_frames_processor__mutmut_45, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_46': x_remove_first_pyinstrument_frames_processor__mutmut_46, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_47': x_remove_first_pyinstrument_frames_processor__mutmut_47, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_48': x_remove_first_pyinstrument_frames_processor__mutmut_48, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_49': x_remove_first_pyinstrument_frames_processor__mutmut_49, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_50': x_remove_first_pyinstrument_frames_processor__mutmut_50, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_51': x_remove_first_pyinstrument_frames_processor__mutmut_51, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_52': x_remove_first_pyinstrument_frames_processor__mutmut_52, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_53': x_remove_first_pyinstrument_frames_processor__mutmut_53, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_54': x_remove_first_pyinstrument_frames_processor__mutmut_54, 
    'x_remove_first_pyinstrument_frames_processor__mutmut_55': x_remove_first_pyinstrument_frames_processor__mutmut_55
}

def remove_first_pyinstrument_frames_processor(*args, **kwargs):
    result = _mutmut_trampoline(x_remove_first_pyinstrument_frames_processor__mutmut_orig, x_remove_first_pyinstrument_frames_processor__mutmut_mutants, args, kwargs)
    return result 

remove_first_pyinstrument_frames_processor.__signature__ = _mutmut_signature(x_remove_first_pyinstrument_frames_processor__mutmut_orig)
x_remove_first_pyinstrument_frames_processor__mutmut_orig.__name__ = 'x_remove_first_pyinstrument_frames_processor'
