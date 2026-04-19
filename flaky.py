from __future__ import annotations

from typing import Any, Callable, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])


def flaky(*args: Any, **kwargs: Any):
    """
    Lightweight local fallback for the optional flaky dependency used in tests.
    """

    if args and callable(args[0]) and len(args) == 1 and not kwargs:
        return cast(F, args[0])

    def decorator(func: F) -> F:
        return func

    return decorator
