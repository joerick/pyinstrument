import os
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from typing_extensions import Literal as LiteralStr
    from typing_extensions import TypeAlias, Unpack, assert_never
else:
    # a type, that when subscripted, returns `str`.
    class _LiteralStr:
        def __getitem__(self, values):
            return str

    LiteralStr = _LiteralStr()

    def assert_never(value: Any):
        raise ValueError(value)

    Unpack = Any
    TypeAlias = Any


PathOrStr = Union[str, "os.PathLike[str]"]

__all__ = ["PathOrStr", "LiteralStr", "assert_never", "Unpack", "TypeAlias"]
