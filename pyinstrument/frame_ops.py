from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from pyinstrument.frame import (
    DUMMY_ROOT_FRAME_IDENTIFIER,
    SELF_TIME_FRAME_IDENTIFIER,
    Frame,
    FrameContext,
)
from pyinstrument.frame_info import frame_info_get_identifier
from pyinstrument.typing import LiteralStr, assert_never

# pyright: strict


FrameRecordType = Tuple[List[str], float]


class IdentifierDoesntMatchException(ValueError):
    pass


def build_frame_tree(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Dict[str, Frame | None] | None:
    if len(frame_records) == 0:
        return None

    # put the root frame at the bottom of the stack
    root_frames: Dict[str, Frame] = {}
    frame_stacks: Dict[str, list[Frame]] = {}

    for frame_info_stack, time in frame_records:
        stack_depth = 0

        thread_id = frame_info_get_identifier(frame_info_stack[0])

        if thread_id not in root_frames:
            thread_root = Frame(
                thread_id=thread_id,
                identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)
            root_frames[thread_id] = thread_root
            frame_stacks[thread_id] = [thread_root]

        root_frames[thread_id].record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stacks[thread_id][stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stacks[thread_id][stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stacks[thread_id][stack_depth - 1]
                frame = Frame(thread_id=thread_id, identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stacks[thread_id]) == stack_depth
                frame_stacks[thread_id].append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stacks[thread_id][stack_depth + 1:]

        final_frame = frame_stacks[thread_id][-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(thread_id=thread_id,
                      identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    for thread_id, root_frame in root_frames.items():
        if len(root_frames[thread_id].children) == 1:
            root_frames[thread_id] = root_frame.children[0]
            root_frames[thread_id].remove_from_parent()

    return root_frames


def delete_frame_from_tree(
    frame: Frame, replace_with: LiteralStr["children", "self_time", "nothing"]
):
    """
    Delete a frame from the tree.

    :param frame: the frame to delete
    :param replace_with: what to replace the frame with - `children` replaces
        the frame with its children, `self_time` replaces the frame with a
        self-time frame, and `nothing` deletes the frame, absorbing the time
        into the parent.
    """
    parent = frame.parent
    if parent is None:
        raise ValueError("Cannot delete the root frame")

    if replace_with == "children":
        parent.add_children(frame.children, after=frame)
    elif replace_with == "self_time":
        parent.add_child(
            Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=frame.time),
            after=frame,
        )
    elif replace_with == "nothing":
        parent.absorbed_time += frame.time
    else:
        assert_never(replace_with)

    parent.absorbed_time += frame.absorbed_time

    frame.remove_from_parent()
    # in this call, recursive is true, even when replace_with is 'children'.
    # When replace_with is 'self_time' or 'nothing', that's what we want. But
    # when it's 'children', by now, the children have been removed and added
    # to the parent, so recursive is irrelevant.
    remove_frame_from_groups(frame, recursive=True)


def combine_frames(frame: Frame, into: Frame):
    """
    Combine two frames into one. The frames must have the same parent.

    :param frame: the frame to remove
    :param into: the frame to combine into
    """
    assert frame.parent is into.parent

    into.absorbed_time += frame.absorbed_time
    into.time += frame.time

    for attribute, time in frame.attributes.items():
        try:
            into.attributes[attribute] += time
        except KeyError:
            into.attributes[attribute] = time

    into.add_children(frame.children)
    frame.remove_from_parent()
    remove_frame_from_groups(frame, recursive=False)


def remove_frame_from_groups(frame: Frame, recursive: bool):
    """
    Removes frame from any groups that it is a member of. Should be used when
    removing a frame from a tree, so groups don't keep references to removed
    frames.
    """
    if recursive and frame.children:
        for child in frame.children:
            remove_frame_from_groups(child, recursive=True)

    if frame.group:
        group = frame.group
        group.remove_frame(frame)

        if len(group.frames) == 1:
            # a group with only one frame is meaningless, we'll remove it
            # entirely.
            group.remove_frame(group.frames[0])
