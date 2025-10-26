from __future__ import annotations

from typing import List, Sequence, Tuple

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


class IdentifierDoesntMatchException(ValueError):
    pass


def x_build_frame_tree__mutmut_orig(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_1(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) != 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_2(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 1:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_3(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = None

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_4(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=None, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_5(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=None)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_6(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_7(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, )

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_8(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = None

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_9(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = None
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_10(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 1
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_11(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(None, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_12(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, None)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_13(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_14(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, )

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_15(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(None, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_16(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=None):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_17(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_18(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, ):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_19(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=2):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_20(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = None
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_21(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(None)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_22(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = None
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_23(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier == frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_24(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = None
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_25(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth + 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_26(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 2]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_27(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = None
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_28(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=None)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_29(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(None)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_30(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) != stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_31(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(None)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_32(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=None, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_33(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=None)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_34(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_35(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, )

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_36(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth - 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_37(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 2 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_38(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = None

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_39(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[+1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_40(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-2]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_41(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_42(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                None
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_43(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=None, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_44(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=None)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_45(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_46(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, )
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_47(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) != 1:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_48(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 2:
        root_frame = root_frame.children[0]
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_49(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = None
        root_frame.remove_from_parent()

    return root_frame


def x_build_frame_tree__mutmut_50(
    frame_records: Sequence[FrameRecordType], context: FrameContext
) -> Frame | None:
    if len(frame_records) == 0:
        return None

    root_frame = Frame(identifier_or_frame_info=DUMMY_ROOT_FRAME_IDENTIFIER, context=context)

    # put the root frame at the bottom of the stack
    frame_stack: list[Frame] = [root_frame]

    for frame_info_stack, time in frame_records:
        stack_depth = 0
        root_frame.record_time_from_frame_info(DUMMY_ROOT_FRAME_IDENTIFIER, time)

        for stack_depth, frame_info in enumerate(frame_info_stack, start=1):
            frame_identifier = frame_info_get_identifier(frame_info)
            try:
                frame = frame_stack[stack_depth]
                if frame.identifier != frame_identifier:
                    # trim any frames after and including this one, and make a new frame
                    del frame_stack[stack_depth:]
                    raise IdentifierDoesntMatchException()
            except (IndexError, IdentifierDoesntMatchException):
                # create a new frame
                parent = frame_stack[stack_depth - 1]
                frame = Frame(identifier_or_frame_info=frame_info)
                parent.add_child(frame)

                assert len(frame_stack) == stack_depth
                frame_stack.append(frame)

            frame.record_time_from_frame_info(frame_info=frame_info, time=time)

        # trim any extra frames
        del frame_stack[stack_depth + 1 :]

        final_frame = frame_stack[-1]

        if not final_frame.is_synthetic_leaf:
            # record the self-time
            final_frame.add_child(
                Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=time)
            )

    if len(root_frame.children) == 1:
        root_frame = root_frame.children[1]
        root_frame.remove_from_parent()

    return root_frame

x_build_frame_tree__mutmut_mutants : ClassVar[MutantDict] = {
'x_build_frame_tree__mutmut_1': x_build_frame_tree__mutmut_1, 
    'x_build_frame_tree__mutmut_2': x_build_frame_tree__mutmut_2, 
    'x_build_frame_tree__mutmut_3': x_build_frame_tree__mutmut_3, 
    'x_build_frame_tree__mutmut_4': x_build_frame_tree__mutmut_4, 
    'x_build_frame_tree__mutmut_5': x_build_frame_tree__mutmut_5, 
    'x_build_frame_tree__mutmut_6': x_build_frame_tree__mutmut_6, 
    'x_build_frame_tree__mutmut_7': x_build_frame_tree__mutmut_7, 
    'x_build_frame_tree__mutmut_8': x_build_frame_tree__mutmut_8, 
    'x_build_frame_tree__mutmut_9': x_build_frame_tree__mutmut_9, 
    'x_build_frame_tree__mutmut_10': x_build_frame_tree__mutmut_10, 
    'x_build_frame_tree__mutmut_11': x_build_frame_tree__mutmut_11, 
    'x_build_frame_tree__mutmut_12': x_build_frame_tree__mutmut_12, 
    'x_build_frame_tree__mutmut_13': x_build_frame_tree__mutmut_13, 
    'x_build_frame_tree__mutmut_14': x_build_frame_tree__mutmut_14, 
    'x_build_frame_tree__mutmut_15': x_build_frame_tree__mutmut_15, 
    'x_build_frame_tree__mutmut_16': x_build_frame_tree__mutmut_16, 
    'x_build_frame_tree__mutmut_17': x_build_frame_tree__mutmut_17, 
    'x_build_frame_tree__mutmut_18': x_build_frame_tree__mutmut_18, 
    'x_build_frame_tree__mutmut_19': x_build_frame_tree__mutmut_19, 
    'x_build_frame_tree__mutmut_20': x_build_frame_tree__mutmut_20, 
    'x_build_frame_tree__mutmut_21': x_build_frame_tree__mutmut_21, 
    'x_build_frame_tree__mutmut_22': x_build_frame_tree__mutmut_22, 
    'x_build_frame_tree__mutmut_23': x_build_frame_tree__mutmut_23, 
    'x_build_frame_tree__mutmut_24': x_build_frame_tree__mutmut_24, 
    'x_build_frame_tree__mutmut_25': x_build_frame_tree__mutmut_25, 
    'x_build_frame_tree__mutmut_26': x_build_frame_tree__mutmut_26, 
    'x_build_frame_tree__mutmut_27': x_build_frame_tree__mutmut_27, 
    'x_build_frame_tree__mutmut_28': x_build_frame_tree__mutmut_28, 
    'x_build_frame_tree__mutmut_29': x_build_frame_tree__mutmut_29, 
    'x_build_frame_tree__mutmut_30': x_build_frame_tree__mutmut_30, 
    'x_build_frame_tree__mutmut_31': x_build_frame_tree__mutmut_31, 
    'x_build_frame_tree__mutmut_32': x_build_frame_tree__mutmut_32, 
    'x_build_frame_tree__mutmut_33': x_build_frame_tree__mutmut_33, 
    'x_build_frame_tree__mutmut_34': x_build_frame_tree__mutmut_34, 
    'x_build_frame_tree__mutmut_35': x_build_frame_tree__mutmut_35, 
    'x_build_frame_tree__mutmut_36': x_build_frame_tree__mutmut_36, 
    'x_build_frame_tree__mutmut_37': x_build_frame_tree__mutmut_37, 
    'x_build_frame_tree__mutmut_38': x_build_frame_tree__mutmut_38, 
    'x_build_frame_tree__mutmut_39': x_build_frame_tree__mutmut_39, 
    'x_build_frame_tree__mutmut_40': x_build_frame_tree__mutmut_40, 
    'x_build_frame_tree__mutmut_41': x_build_frame_tree__mutmut_41, 
    'x_build_frame_tree__mutmut_42': x_build_frame_tree__mutmut_42, 
    'x_build_frame_tree__mutmut_43': x_build_frame_tree__mutmut_43, 
    'x_build_frame_tree__mutmut_44': x_build_frame_tree__mutmut_44, 
    'x_build_frame_tree__mutmut_45': x_build_frame_tree__mutmut_45, 
    'x_build_frame_tree__mutmut_46': x_build_frame_tree__mutmut_46, 
    'x_build_frame_tree__mutmut_47': x_build_frame_tree__mutmut_47, 
    'x_build_frame_tree__mutmut_48': x_build_frame_tree__mutmut_48, 
    'x_build_frame_tree__mutmut_49': x_build_frame_tree__mutmut_49, 
    'x_build_frame_tree__mutmut_50': x_build_frame_tree__mutmut_50
}

def build_frame_tree(*args, **kwargs):
    result = _mutmut_trampoline(x_build_frame_tree__mutmut_orig, x_build_frame_tree__mutmut_mutants, args, kwargs)
    return result 

build_frame_tree.__signature__ = _mutmut_signature(x_build_frame_tree__mutmut_orig)
x_build_frame_tree__mutmut_orig.__name__ = 'x_build_frame_tree'


def x_delete_frame_from_tree__mutmut_orig(
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


def x_delete_frame_from_tree__mutmut_1(
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
    parent = None
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


def x_delete_frame_from_tree__mutmut_2(
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
    if parent is not None:
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


def x_delete_frame_from_tree__mutmut_3(
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
        raise ValueError(None)

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


def x_delete_frame_from_tree__mutmut_4(
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
        raise ValueError("XXCannot delete the root frameXX")

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


def x_delete_frame_from_tree__mutmut_5(
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
        raise ValueError("cannot delete the root frame")

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


def x_delete_frame_from_tree__mutmut_6(
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
        raise ValueError("CANNOT DELETE THE ROOT FRAME")

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


def x_delete_frame_from_tree__mutmut_7(
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

    if replace_with != "children":
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


def x_delete_frame_from_tree__mutmut_8(
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

    if replace_with == "XXchildrenXX":
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


def x_delete_frame_from_tree__mutmut_9(
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

    if replace_with == "CHILDREN":
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


def x_delete_frame_from_tree__mutmut_10(
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
        parent.add_children(None, after=frame)
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


def x_delete_frame_from_tree__mutmut_11(
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
        parent.add_children(frame.children, after=None)
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


def x_delete_frame_from_tree__mutmut_12(
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
        parent.add_children(after=frame)
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


def x_delete_frame_from_tree__mutmut_13(
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
        parent.add_children(frame.children, )
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


def x_delete_frame_from_tree__mutmut_14(
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
    elif replace_with != "self_time":
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


def x_delete_frame_from_tree__mutmut_15(
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
    elif replace_with == "XXself_timeXX":
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


def x_delete_frame_from_tree__mutmut_16(
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
    elif replace_with == "SELF_TIME":
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


def x_delete_frame_from_tree__mutmut_17(
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
            None,
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


def x_delete_frame_from_tree__mutmut_18(
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
            after=None,
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


def x_delete_frame_from_tree__mutmut_19(
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


def x_delete_frame_from_tree__mutmut_20(
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


def x_delete_frame_from_tree__mutmut_21(
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
            Frame(identifier_or_frame_info=None, time=frame.time),
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


def x_delete_frame_from_tree__mutmut_22(
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
            Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, time=None),
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


def x_delete_frame_from_tree__mutmut_23(
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
            Frame(time=frame.time),
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


def x_delete_frame_from_tree__mutmut_24(
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
            Frame(identifier_or_frame_info=SELF_TIME_FRAME_IDENTIFIER, ),
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


def x_delete_frame_from_tree__mutmut_25(
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
    elif replace_with != "nothing":
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


def x_delete_frame_from_tree__mutmut_26(
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
    elif replace_with == "XXnothingXX":
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


def x_delete_frame_from_tree__mutmut_27(
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
    elif replace_with == "NOTHING":
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


def x_delete_frame_from_tree__mutmut_28(
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
        parent.absorbed_time = frame.time
    else:
        assert_never(replace_with)

    parent.absorbed_time += frame.absorbed_time

    frame.remove_from_parent()
    # in this call, recursive is true, even when replace_with is 'children'.
    # When replace_with is 'self_time' or 'nothing', that's what we want. But
    # when it's 'children', by now, the children have been removed and added
    # to the parent, so recursive is irrelevant.
    remove_frame_from_groups(frame, recursive=True)


def x_delete_frame_from_tree__mutmut_29(
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
        parent.absorbed_time -= frame.time
    else:
        assert_never(replace_with)

    parent.absorbed_time += frame.absorbed_time

    frame.remove_from_parent()
    # in this call, recursive is true, even when replace_with is 'children'.
    # When replace_with is 'self_time' or 'nothing', that's what we want. But
    # when it's 'children', by now, the children have been removed and added
    # to the parent, so recursive is irrelevant.
    remove_frame_from_groups(frame, recursive=True)


def x_delete_frame_from_tree__mutmut_30(
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
        assert_never(None)

    parent.absorbed_time += frame.absorbed_time

    frame.remove_from_parent()
    # in this call, recursive is true, even when replace_with is 'children'.
    # When replace_with is 'self_time' or 'nothing', that's what we want. But
    # when it's 'children', by now, the children have been removed and added
    # to the parent, so recursive is irrelevant.
    remove_frame_from_groups(frame, recursive=True)


def x_delete_frame_from_tree__mutmut_31(
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

    parent.absorbed_time = frame.absorbed_time

    frame.remove_from_parent()
    # in this call, recursive is true, even when replace_with is 'children'.
    # When replace_with is 'self_time' or 'nothing', that's what we want. But
    # when it's 'children', by now, the children have been removed and added
    # to the parent, so recursive is irrelevant.
    remove_frame_from_groups(frame, recursive=True)


def x_delete_frame_from_tree__mutmut_32(
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

    parent.absorbed_time -= frame.absorbed_time

    frame.remove_from_parent()
    # in this call, recursive is true, even when replace_with is 'children'.
    # When replace_with is 'self_time' or 'nothing', that's what we want. But
    # when it's 'children', by now, the children have been removed and added
    # to the parent, so recursive is irrelevant.
    remove_frame_from_groups(frame, recursive=True)


def x_delete_frame_from_tree__mutmut_33(
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
    remove_frame_from_groups(None, recursive=True)


def x_delete_frame_from_tree__mutmut_34(
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
    remove_frame_from_groups(frame, recursive=None)


def x_delete_frame_from_tree__mutmut_35(
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
    remove_frame_from_groups(recursive=True)


def x_delete_frame_from_tree__mutmut_36(
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
    remove_frame_from_groups(frame, )


def x_delete_frame_from_tree__mutmut_37(
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
    remove_frame_from_groups(frame, recursive=False)

x_delete_frame_from_tree__mutmut_mutants : ClassVar[MutantDict] = {
'x_delete_frame_from_tree__mutmut_1': x_delete_frame_from_tree__mutmut_1, 
    'x_delete_frame_from_tree__mutmut_2': x_delete_frame_from_tree__mutmut_2, 
    'x_delete_frame_from_tree__mutmut_3': x_delete_frame_from_tree__mutmut_3, 
    'x_delete_frame_from_tree__mutmut_4': x_delete_frame_from_tree__mutmut_4, 
    'x_delete_frame_from_tree__mutmut_5': x_delete_frame_from_tree__mutmut_5, 
    'x_delete_frame_from_tree__mutmut_6': x_delete_frame_from_tree__mutmut_6, 
    'x_delete_frame_from_tree__mutmut_7': x_delete_frame_from_tree__mutmut_7, 
    'x_delete_frame_from_tree__mutmut_8': x_delete_frame_from_tree__mutmut_8, 
    'x_delete_frame_from_tree__mutmut_9': x_delete_frame_from_tree__mutmut_9, 
    'x_delete_frame_from_tree__mutmut_10': x_delete_frame_from_tree__mutmut_10, 
    'x_delete_frame_from_tree__mutmut_11': x_delete_frame_from_tree__mutmut_11, 
    'x_delete_frame_from_tree__mutmut_12': x_delete_frame_from_tree__mutmut_12, 
    'x_delete_frame_from_tree__mutmut_13': x_delete_frame_from_tree__mutmut_13, 
    'x_delete_frame_from_tree__mutmut_14': x_delete_frame_from_tree__mutmut_14, 
    'x_delete_frame_from_tree__mutmut_15': x_delete_frame_from_tree__mutmut_15, 
    'x_delete_frame_from_tree__mutmut_16': x_delete_frame_from_tree__mutmut_16, 
    'x_delete_frame_from_tree__mutmut_17': x_delete_frame_from_tree__mutmut_17, 
    'x_delete_frame_from_tree__mutmut_18': x_delete_frame_from_tree__mutmut_18, 
    'x_delete_frame_from_tree__mutmut_19': x_delete_frame_from_tree__mutmut_19, 
    'x_delete_frame_from_tree__mutmut_20': x_delete_frame_from_tree__mutmut_20, 
    'x_delete_frame_from_tree__mutmut_21': x_delete_frame_from_tree__mutmut_21, 
    'x_delete_frame_from_tree__mutmut_22': x_delete_frame_from_tree__mutmut_22, 
    'x_delete_frame_from_tree__mutmut_23': x_delete_frame_from_tree__mutmut_23, 
    'x_delete_frame_from_tree__mutmut_24': x_delete_frame_from_tree__mutmut_24, 
    'x_delete_frame_from_tree__mutmut_25': x_delete_frame_from_tree__mutmut_25, 
    'x_delete_frame_from_tree__mutmut_26': x_delete_frame_from_tree__mutmut_26, 
    'x_delete_frame_from_tree__mutmut_27': x_delete_frame_from_tree__mutmut_27, 
    'x_delete_frame_from_tree__mutmut_28': x_delete_frame_from_tree__mutmut_28, 
    'x_delete_frame_from_tree__mutmut_29': x_delete_frame_from_tree__mutmut_29, 
    'x_delete_frame_from_tree__mutmut_30': x_delete_frame_from_tree__mutmut_30, 
    'x_delete_frame_from_tree__mutmut_31': x_delete_frame_from_tree__mutmut_31, 
    'x_delete_frame_from_tree__mutmut_32': x_delete_frame_from_tree__mutmut_32, 
    'x_delete_frame_from_tree__mutmut_33': x_delete_frame_from_tree__mutmut_33, 
    'x_delete_frame_from_tree__mutmut_34': x_delete_frame_from_tree__mutmut_34, 
    'x_delete_frame_from_tree__mutmut_35': x_delete_frame_from_tree__mutmut_35, 
    'x_delete_frame_from_tree__mutmut_36': x_delete_frame_from_tree__mutmut_36, 
    'x_delete_frame_from_tree__mutmut_37': x_delete_frame_from_tree__mutmut_37
}

def delete_frame_from_tree(*args, **kwargs):
    result = _mutmut_trampoline(x_delete_frame_from_tree__mutmut_orig, x_delete_frame_from_tree__mutmut_mutants, args, kwargs)
    return result 

delete_frame_from_tree.__signature__ = _mutmut_signature(x_delete_frame_from_tree__mutmut_orig)
x_delete_frame_from_tree__mutmut_orig.__name__ = 'x_delete_frame_from_tree'


def x_combine_frames__mutmut_orig(frame: Frame, into: Frame):
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


def x_combine_frames__mutmut_1(frame: Frame, into: Frame):
    """
    Combine two frames into one. The frames must have the same parent.

    :param frame: the frame to remove
    :param into: the frame to combine into
    """
    assert frame.parent is not into.parent

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


def x_combine_frames__mutmut_2(frame: Frame, into: Frame):
    """
    Combine two frames into one. The frames must have the same parent.

    :param frame: the frame to remove
    :param into: the frame to combine into
    """
    assert frame.parent is into.parent

    into.absorbed_time = frame.absorbed_time
    into.time += frame.time

    for attribute, time in frame.attributes.items():
        try:
            into.attributes[attribute] += time
        except KeyError:
            into.attributes[attribute] = time

    into.add_children(frame.children)
    frame.remove_from_parent()
    remove_frame_from_groups(frame, recursive=False)


def x_combine_frames__mutmut_3(frame: Frame, into: Frame):
    """
    Combine two frames into one. The frames must have the same parent.

    :param frame: the frame to remove
    :param into: the frame to combine into
    """
    assert frame.parent is into.parent

    into.absorbed_time -= frame.absorbed_time
    into.time += frame.time

    for attribute, time in frame.attributes.items():
        try:
            into.attributes[attribute] += time
        except KeyError:
            into.attributes[attribute] = time

    into.add_children(frame.children)
    frame.remove_from_parent()
    remove_frame_from_groups(frame, recursive=False)


def x_combine_frames__mutmut_4(frame: Frame, into: Frame):
    """
    Combine two frames into one. The frames must have the same parent.

    :param frame: the frame to remove
    :param into: the frame to combine into
    """
    assert frame.parent is into.parent

    into.absorbed_time += frame.absorbed_time
    into.time = frame.time

    for attribute, time in frame.attributes.items():
        try:
            into.attributes[attribute] += time
        except KeyError:
            into.attributes[attribute] = time

    into.add_children(frame.children)
    frame.remove_from_parent()
    remove_frame_from_groups(frame, recursive=False)


def x_combine_frames__mutmut_5(frame: Frame, into: Frame):
    """
    Combine two frames into one. The frames must have the same parent.

    :param frame: the frame to remove
    :param into: the frame to combine into
    """
    assert frame.parent is into.parent

    into.absorbed_time += frame.absorbed_time
    into.time -= frame.time

    for attribute, time in frame.attributes.items():
        try:
            into.attributes[attribute] += time
        except KeyError:
            into.attributes[attribute] = time

    into.add_children(frame.children)
    frame.remove_from_parent()
    remove_frame_from_groups(frame, recursive=False)


def x_combine_frames__mutmut_6(frame: Frame, into: Frame):
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
            into.attributes[attribute] = time
        except KeyError:
            into.attributes[attribute] = time

    into.add_children(frame.children)
    frame.remove_from_parent()
    remove_frame_from_groups(frame, recursive=False)


def x_combine_frames__mutmut_7(frame: Frame, into: Frame):
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
            into.attributes[attribute] -= time
        except KeyError:
            into.attributes[attribute] = time

    into.add_children(frame.children)
    frame.remove_from_parent()
    remove_frame_from_groups(frame, recursive=False)


def x_combine_frames__mutmut_8(frame: Frame, into: Frame):
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
            into.attributes[attribute] = None

    into.add_children(frame.children)
    frame.remove_from_parent()
    remove_frame_from_groups(frame, recursive=False)


def x_combine_frames__mutmut_9(frame: Frame, into: Frame):
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

    into.add_children(None)
    frame.remove_from_parent()
    remove_frame_from_groups(frame, recursive=False)


def x_combine_frames__mutmut_10(frame: Frame, into: Frame):
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
    remove_frame_from_groups(None, recursive=False)


def x_combine_frames__mutmut_11(frame: Frame, into: Frame):
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
    remove_frame_from_groups(frame, recursive=None)


def x_combine_frames__mutmut_12(frame: Frame, into: Frame):
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
    remove_frame_from_groups(recursive=False)


def x_combine_frames__mutmut_13(frame: Frame, into: Frame):
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
    remove_frame_from_groups(frame, )


def x_combine_frames__mutmut_14(frame: Frame, into: Frame):
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
    remove_frame_from_groups(frame, recursive=True)

x_combine_frames__mutmut_mutants : ClassVar[MutantDict] = {
'x_combine_frames__mutmut_1': x_combine_frames__mutmut_1, 
    'x_combine_frames__mutmut_2': x_combine_frames__mutmut_2, 
    'x_combine_frames__mutmut_3': x_combine_frames__mutmut_3, 
    'x_combine_frames__mutmut_4': x_combine_frames__mutmut_4, 
    'x_combine_frames__mutmut_5': x_combine_frames__mutmut_5, 
    'x_combine_frames__mutmut_6': x_combine_frames__mutmut_6, 
    'x_combine_frames__mutmut_7': x_combine_frames__mutmut_7, 
    'x_combine_frames__mutmut_8': x_combine_frames__mutmut_8, 
    'x_combine_frames__mutmut_9': x_combine_frames__mutmut_9, 
    'x_combine_frames__mutmut_10': x_combine_frames__mutmut_10, 
    'x_combine_frames__mutmut_11': x_combine_frames__mutmut_11, 
    'x_combine_frames__mutmut_12': x_combine_frames__mutmut_12, 
    'x_combine_frames__mutmut_13': x_combine_frames__mutmut_13, 
    'x_combine_frames__mutmut_14': x_combine_frames__mutmut_14
}

def combine_frames(*args, **kwargs):
    result = _mutmut_trampoline(x_combine_frames__mutmut_orig, x_combine_frames__mutmut_mutants, args, kwargs)
    return result 

combine_frames.__signature__ = _mutmut_signature(x_combine_frames__mutmut_orig)
x_combine_frames__mutmut_orig.__name__ = 'x_combine_frames'


def x_remove_frame_from_groups__mutmut_orig(frame: Frame, recursive: bool):
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


def x_remove_frame_from_groups__mutmut_1(frame: Frame, recursive: bool):
    """
    Removes frame from any groups that it is a member of. Should be used when
    removing a frame from a tree, so groups don't keep references to removed
    frames.
    """
    if recursive or frame.children:
        for child in frame.children:
            remove_frame_from_groups(child, recursive=True)

    if frame.group:
        group = frame.group
        group.remove_frame(frame)

        if len(group.frames) == 1:
            # a group with only one frame is meaningless, we'll remove it
            # entirely.
            group.remove_frame(group.frames[0])


def x_remove_frame_from_groups__mutmut_2(frame: Frame, recursive: bool):
    """
    Removes frame from any groups that it is a member of. Should be used when
    removing a frame from a tree, so groups don't keep references to removed
    frames.
    """
    if recursive and frame.children:
        for child in frame.children:
            remove_frame_from_groups(None, recursive=True)

    if frame.group:
        group = frame.group
        group.remove_frame(frame)

        if len(group.frames) == 1:
            # a group with only one frame is meaningless, we'll remove it
            # entirely.
            group.remove_frame(group.frames[0])


def x_remove_frame_from_groups__mutmut_3(frame: Frame, recursive: bool):
    """
    Removes frame from any groups that it is a member of. Should be used when
    removing a frame from a tree, so groups don't keep references to removed
    frames.
    """
    if recursive and frame.children:
        for child in frame.children:
            remove_frame_from_groups(child, recursive=None)

    if frame.group:
        group = frame.group
        group.remove_frame(frame)

        if len(group.frames) == 1:
            # a group with only one frame is meaningless, we'll remove it
            # entirely.
            group.remove_frame(group.frames[0])


def x_remove_frame_from_groups__mutmut_4(frame: Frame, recursive: bool):
    """
    Removes frame from any groups that it is a member of. Should be used when
    removing a frame from a tree, so groups don't keep references to removed
    frames.
    """
    if recursive and frame.children:
        for child in frame.children:
            remove_frame_from_groups(recursive=True)

    if frame.group:
        group = frame.group
        group.remove_frame(frame)

        if len(group.frames) == 1:
            # a group with only one frame is meaningless, we'll remove it
            # entirely.
            group.remove_frame(group.frames[0])


def x_remove_frame_from_groups__mutmut_5(frame: Frame, recursive: bool):
    """
    Removes frame from any groups that it is a member of. Should be used when
    removing a frame from a tree, so groups don't keep references to removed
    frames.
    """
    if recursive and frame.children:
        for child in frame.children:
            remove_frame_from_groups(child, )

    if frame.group:
        group = frame.group
        group.remove_frame(frame)

        if len(group.frames) == 1:
            # a group with only one frame is meaningless, we'll remove it
            # entirely.
            group.remove_frame(group.frames[0])


def x_remove_frame_from_groups__mutmut_6(frame: Frame, recursive: bool):
    """
    Removes frame from any groups that it is a member of. Should be used when
    removing a frame from a tree, so groups don't keep references to removed
    frames.
    """
    if recursive and frame.children:
        for child in frame.children:
            remove_frame_from_groups(child, recursive=False)

    if frame.group:
        group = frame.group
        group.remove_frame(frame)

        if len(group.frames) == 1:
            # a group with only one frame is meaningless, we'll remove it
            # entirely.
            group.remove_frame(group.frames[0])


def x_remove_frame_from_groups__mutmut_7(frame: Frame, recursive: bool):
    """
    Removes frame from any groups that it is a member of. Should be used when
    removing a frame from a tree, so groups don't keep references to removed
    frames.
    """
    if recursive and frame.children:
        for child in frame.children:
            remove_frame_from_groups(child, recursive=True)

    if frame.group:
        group = None
        group.remove_frame(frame)

        if len(group.frames) == 1:
            # a group with only one frame is meaningless, we'll remove it
            # entirely.
            group.remove_frame(group.frames[0])


def x_remove_frame_from_groups__mutmut_8(frame: Frame, recursive: bool):
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
        group.remove_frame(None)

        if len(group.frames) == 1:
            # a group with only one frame is meaningless, we'll remove it
            # entirely.
            group.remove_frame(group.frames[0])


def x_remove_frame_from_groups__mutmut_9(frame: Frame, recursive: bool):
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

        if len(group.frames) != 1:
            # a group with only one frame is meaningless, we'll remove it
            # entirely.
            group.remove_frame(group.frames[0])


def x_remove_frame_from_groups__mutmut_10(frame: Frame, recursive: bool):
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

        if len(group.frames) == 2:
            # a group with only one frame is meaningless, we'll remove it
            # entirely.
            group.remove_frame(group.frames[0])


def x_remove_frame_from_groups__mutmut_11(frame: Frame, recursive: bool):
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
            group.remove_frame(None)


def x_remove_frame_from_groups__mutmut_12(frame: Frame, recursive: bool):
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
            group.remove_frame(group.frames[1])

x_remove_frame_from_groups__mutmut_mutants : ClassVar[MutantDict] = {
'x_remove_frame_from_groups__mutmut_1': x_remove_frame_from_groups__mutmut_1, 
    'x_remove_frame_from_groups__mutmut_2': x_remove_frame_from_groups__mutmut_2, 
    'x_remove_frame_from_groups__mutmut_3': x_remove_frame_from_groups__mutmut_3, 
    'x_remove_frame_from_groups__mutmut_4': x_remove_frame_from_groups__mutmut_4, 
    'x_remove_frame_from_groups__mutmut_5': x_remove_frame_from_groups__mutmut_5, 
    'x_remove_frame_from_groups__mutmut_6': x_remove_frame_from_groups__mutmut_6, 
    'x_remove_frame_from_groups__mutmut_7': x_remove_frame_from_groups__mutmut_7, 
    'x_remove_frame_from_groups__mutmut_8': x_remove_frame_from_groups__mutmut_8, 
    'x_remove_frame_from_groups__mutmut_9': x_remove_frame_from_groups__mutmut_9, 
    'x_remove_frame_from_groups__mutmut_10': x_remove_frame_from_groups__mutmut_10, 
    'x_remove_frame_from_groups__mutmut_11': x_remove_frame_from_groups__mutmut_11, 
    'x_remove_frame_from_groups__mutmut_12': x_remove_frame_from_groups__mutmut_12
}

def remove_frame_from_groups(*args, **kwargs):
    result = _mutmut_trampoline(x_remove_frame_from_groups__mutmut_orig, x_remove_frame_from_groups__mutmut_mutants, args, kwargs)
    return result 

remove_frame_from_groups.__signature__ = _mutmut_signature(x_remove_frame_from_groups__mutmut_orig)
x_remove_frame_from_groups__mutmut_orig.__name__ = 'x_remove_frame_from_groups'
