import os
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from typing_extensions import Literal, assert_never

    LiteralStr = Literal
else:
    # a type, that when subscripted, returns `str`.
    class _LiteralStr:
        def __getitem__(self, values):
            return str

    LiteralStr = _LiteralStr()

    def assert_never(value: Any):
        raise ValueError(value)


PathOrStr = Union[str, "os.PathLike[str]"]

__all__ = ["PathOrStr", "LiteralStr", "assert_never"]
