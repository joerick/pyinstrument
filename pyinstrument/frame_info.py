from typing import List, Tuple

# pyright: strict


IDENTIFIER_SEP = "\x00"
ATTRIBUTES_SEP = "\x01"

ATTRIBUTE_MARKER_CLASS_NAME = "c"
ATTRIBUTE_MARKER_LINE_NUMBER = "l"
ATTRIBUTE_MARKER_TRACEBACKHIDE = "h"


def parse_frame_info(frame_info: str) -> Tuple[str, List[str]]:
    """
    Parses a frame_info string, returns a tuple of (identifier, attributes),
    where `identifier` is a unique identifier for this code (e.g. a function
    or method), and `attributes` is a list of invocation-specific attributes
    that were captured at profile-time.
    """

    identifier, _, attributes_str = frame_info.partition(ATTRIBUTES_SEP)

    if not attributes_str:
        return identifier, []

    return identifier, attributes_str.split(ATTRIBUTES_SEP)


def frame_info_get_identifier(frame_info: str) -> str:
    """
    Equivalent to `parse_frame_info(frame_info)[0]`, but faster.
    """
    index = frame_info.find(ATTRIBUTES_SEP)

    if index == -1:
        # no attributes
        return frame_info

    return frame_info[0:index]
