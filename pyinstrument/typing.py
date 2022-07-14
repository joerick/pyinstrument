import os
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    import typing_extensions

    LiteralStr = typing_extensions.Literal
    assert_never = typing_extensions.assert_never
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
