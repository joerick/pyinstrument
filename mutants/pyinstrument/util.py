import codecs
import importlib
import math
import os
import re
import sys
import warnings
from typing import IO, Any, AnyStr, Callable

from pyinstrument.vendor.decorator import decorator
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


def x_object_with_import_path__mutmut_orig(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(".", 1)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_1(import_path: str) -> Any:
    if "XX.XX" not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(".", 1)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_2(import_path: str) -> Any:
    if "." in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(".", 1)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_3(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError(None)
    module_path, object_name = import_path.rsplit(".", 1)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_4(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" / import_path)
    module_path, object_name = import_path.rsplit(".", 1)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_5(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("XXCan't import '%s', it is not a valid import pathXX" % import_path)
    module_path, object_name = import_path.rsplit(".", 1)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_6(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(".", 1)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_7(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("CAN'T IMPORT '%S', IT IS NOT A VALID IMPORT PATH" % import_path)
    module_path, object_name = import_path.rsplit(".", 1)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_8(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = None

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_9(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(None, 1)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_10(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(".", None)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_11(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(1)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_12(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(".", )

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_13(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.split(".", 1)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_14(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit("XX.XX", 1)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_15(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(".", 2)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_16(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(".", 1)

    module = None
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_17(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(".", 1)

    module = importlib.import_module(None)
    return getattr(module, object_name)


def x_object_with_import_path__mutmut_18(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(".", 1)

    module = importlib.import_module(module_path)
    return getattr(None, object_name)


def x_object_with_import_path__mutmut_19(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(".", 1)

    module = importlib.import_module(module_path)
    return getattr(module, None)


def x_object_with_import_path__mutmut_20(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(".", 1)

    module = importlib.import_module(module_path)
    return getattr(object_name)


def x_object_with_import_path__mutmut_21(import_path: str) -> Any:
    if "." not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit(".", 1)

    module = importlib.import_module(module_path)
    return getattr(module, )

x_object_with_import_path__mutmut_mutants : ClassVar[MutantDict] = {
'x_object_with_import_path__mutmut_1': x_object_with_import_path__mutmut_1, 
    'x_object_with_import_path__mutmut_2': x_object_with_import_path__mutmut_2, 
    'x_object_with_import_path__mutmut_3': x_object_with_import_path__mutmut_3, 
    'x_object_with_import_path__mutmut_4': x_object_with_import_path__mutmut_4, 
    'x_object_with_import_path__mutmut_5': x_object_with_import_path__mutmut_5, 
    'x_object_with_import_path__mutmut_6': x_object_with_import_path__mutmut_6, 
    'x_object_with_import_path__mutmut_7': x_object_with_import_path__mutmut_7, 
    'x_object_with_import_path__mutmut_8': x_object_with_import_path__mutmut_8, 
    'x_object_with_import_path__mutmut_9': x_object_with_import_path__mutmut_9, 
    'x_object_with_import_path__mutmut_10': x_object_with_import_path__mutmut_10, 
    'x_object_with_import_path__mutmut_11': x_object_with_import_path__mutmut_11, 
    'x_object_with_import_path__mutmut_12': x_object_with_import_path__mutmut_12, 
    'x_object_with_import_path__mutmut_13': x_object_with_import_path__mutmut_13, 
    'x_object_with_import_path__mutmut_14': x_object_with_import_path__mutmut_14, 
    'x_object_with_import_path__mutmut_15': x_object_with_import_path__mutmut_15, 
    'x_object_with_import_path__mutmut_16': x_object_with_import_path__mutmut_16, 
    'x_object_with_import_path__mutmut_17': x_object_with_import_path__mutmut_17, 
    'x_object_with_import_path__mutmut_18': x_object_with_import_path__mutmut_18, 
    'x_object_with_import_path__mutmut_19': x_object_with_import_path__mutmut_19, 
    'x_object_with_import_path__mutmut_20': x_object_with_import_path__mutmut_20, 
    'x_object_with_import_path__mutmut_21': x_object_with_import_path__mutmut_21
}

def object_with_import_path(*args, **kwargs):
    result = _mutmut_trampoline(x_object_with_import_path__mutmut_orig, x_object_with_import_path__mutmut_mutants, args, kwargs)
    return result 

object_with_import_path.__signature__ = _mutmut_signature(x_object_with_import_path__mutmut_orig)
x_object_with_import_path__mutmut_orig.__name__ = 'x_object_with_import_path'


def x_truncate__mutmut_orig(string: str, max_length: int) -> str:
    if len(string) > max_length:
        return string[0 : max_length - 3] + "..."
    return string


def x_truncate__mutmut_1(string: str, max_length: int) -> str:
    if len(string) >= max_length:
        return string[0 : max_length - 3] + "..."
    return string


def x_truncate__mutmut_2(string: str, max_length: int) -> str:
    if len(string) > max_length:
        return string[0 : max_length - 3] - "..."
    return string


def x_truncate__mutmut_3(string: str, max_length: int) -> str:
    if len(string) > max_length:
        return string[1 : max_length - 3] + "..."
    return string


def x_truncate__mutmut_4(string: str, max_length: int) -> str:
    if len(string) > max_length:
        return string[0 : max_length + 3] + "..."
    return string


def x_truncate__mutmut_5(string: str, max_length: int) -> str:
    if len(string) > max_length:
        return string[0 : max_length - 4] + "..."
    return string


def x_truncate__mutmut_6(string: str, max_length: int) -> str:
    if len(string) > max_length:
        return string[0 : max_length - 3] + "XX...XX"
    return string

x_truncate__mutmut_mutants : ClassVar[MutantDict] = {
'x_truncate__mutmut_1': x_truncate__mutmut_1, 
    'x_truncate__mutmut_2': x_truncate__mutmut_2, 
    'x_truncate__mutmut_3': x_truncate__mutmut_3, 
    'x_truncate__mutmut_4': x_truncate__mutmut_4, 
    'x_truncate__mutmut_5': x_truncate__mutmut_5, 
    'x_truncate__mutmut_6': x_truncate__mutmut_6
}

def truncate(*args, **kwargs):
    result = _mutmut_trampoline(x_truncate__mutmut_orig, x_truncate__mutmut_mutants, args, kwargs)
    return result 

truncate.__signature__ = _mutmut_signature(x_truncate__mutmut_orig)
x_truncate__mutmut_orig.__name__ = 'x_truncate'


@decorator
def deprecated(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Marks a function as deprecated."""
    warnings.warn(
        f"{func} is deprecated and should no longer be used.",
        DeprecationWarning,
        stacklevel=3,
    )
    return func(*args, **kwargs)


def x_deprecated_option__mutmut_orig(option_name: str, message: str = "") -> Any:
    """Marks an option as deprecated."""

    def caller(func, *args, **kwargs):
        if option_name in kwargs:
            warnings.warn(
                f"{option_name} is deprecated. {message}",
                DeprecationWarning,
                stacklevel=3,
            )

        return func(*args, **kwargs)

    return decorator(caller)


def x_deprecated_option__mutmut_1(option_name: str, message: str = "XXXX") -> Any:
    """Marks an option as deprecated."""

    def caller(func, *args, **kwargs):
        if option_name in kwargs:
            warnings.warn(
                f"{option_name} is deprecated. {message}",
                DeprecationWarning,
                stacklevel=3,
            )

        return func(*args, **kwargs)

    return decorator(caller)


def x_deprecated_option__mutmut_2(option_name: str, message: str = "") -> Any:
    """Marks an option as deprecated."""

    def caller(func, *args, **kwargs):
        if option_name not in kwargs:
            warnings.warn(
                f"{option_name} is deprecated. {message}",
                DeprecationWarning,
                stacklevel=3,
            )

        return func(*args, **kwargs)

    return decorator(caller)


def x_deprecated_option__mutmut_3(option_name: str, message: str = "") -> Any:
    """Marks an option as deprecated."""

    def caller(func, *args, **kwargs):
        if option_name in kwargs:
            warnings.warn(
                None,
                DeprecationWarning,
                stacklevel=3,
            )

        return func(*args, **kwargs)

    return decorator(caller)


def x_deprecated_option__mutmut_4(option_name: str, message: str = "") -> Any:
    """Marks an option as deprecated."""

    def caller(func, *args, **kwargs):
        if option_name in kwargs:
            warnings.warn(
                f"{option_name} is deprecated. {message}",
                None,
                stacklevel=3,
            )

        return func(*args, **kwargs)

    return decorator(caller)


def x_deprecated_option__mutmut_5(option_name: str, message: str = "") -> Any:
    """Marks an option as deprecated."""

    def caller(func, *args, **kwargs):
        if option_name in kwargs:
            warnings.warn(
                f"{option_name} is deprecated. {message}",
                DeprecationWarning,
                stacklevel=None,
            )

        return func(*args, **kwargs)

    return decorator(caller)


def x_deprecated_option__mutmut_6(option_name: str, message: str = "") -> Any:
    """Marks an option as deprecated."""

    def caller(func, *args, **kwargs):
        if option_name in kwargs:
            warnings.warn(
                DeprecationWarning,
                stacklevel=3,
            )

        return func(*args, **kwargs)

    return decorator(caller)


def x_deprecated_option__mutmut_7(option_name: str, message: str = "") -> Any:
    """Marks an option as deprecated."""

    def caller(func, *args, **kwargs):
        if option_name in kwargs:
            warnings.warn(
                f"{option_name} is deprecated. {message}",
                stacklevel=3,
            )

        return func(*args, **kwargs)

    return decorator(caller)


def x_deprecated_option__mutmut_8(option_name: str, message: str = "") -> Any:
    """Marks an option as deprecated."""

    def caller(func, *args, **kwargs):
        if option_name in kwargs:
            warnings.warn(
                f"{option_name} is deprecated. {message}",
                DeprecationWarning,
                )

        return func(*args, **kwargs)

    return decorator(caller)


def x_deprecated_option__mutmut_9(option_name: str, message: str = "") -> Any:
    """Marks an option as deprecated."""

    def caller(func, *args, **kwargs):
        if option_name in kwargs:
            warnings.warn(
                f"{option_name} is deprecated. {message}",
                DeprecationWarning,
                stacklevel=4,
            )

        return func(*args, **kwargs)

    return decorator(caller)


def x_deprecated_option__mutmut_10(option_name: str, message: str = "") -> Any:
    """Marks an option as deprecated."""

    def caller(func, *args, **kwargs):
        if option_name in kwargs:
            warnings.warn(
                f"{option_name} is deprecated. {message}",
                DeprecationWarning,
                stacklevel=3,
            )

        return func(**kwargs)

    return decorator(caller)


def x_deprecated_option__mutmut_11(option_name: str, message: str = "") -> Any:
    """Marks an option as deprecated."""

    def caller(func, *args, **kwargs):
        if option_name in kwargs:
            warnings.warn(
                f"{option_name} is deprecated. {message}",
                DeprecationWarning,
                stacklevel=3,
            )

        return func(*args, )

    return decorator(caller)


def x_deprecated_option__mutmut_12(option_name: str, message: str = "") -> Any:
    """Marks an option as deprecated."""

    def caller(func, *args, **kwargs):
        if option_name in kwargs:
            warnings.warn(
                f"{option_name} is deprecated. {message}",
                DeprecationWarning,
                stacklevel=3,
            )

        return func(*args, **kwargs)

    return decorator(None)

x_deprecated_option__mutmut_mutants : ClassVar[MutantDict] = {
'x_deprecated_option__mutmut_1': x_deprecated_option__mutmut_1, 
    'x_deprecated_option__mutmut_2': x_deprecated_option__mutmut_2, 
    'x_deprecated_option__mutmut_3': x_deprecated_option__mutmut_3, 
    'x_deprecated_option__mutmut_4': x_deprecated_option__mutmut_4, 
    'x_deprecated_option__mutmut_5': x_deprecated_option__mutmut_5, 
    'x_deprecated_option__mutmut_6': x_deprecated_option__mutmut_6, 
    'x_deprecated_option__mutmut_7': x_deprecated_option__mutmut_7, 
    'x_deprecated_option__mutmut_8': x_deprecated_option__mutmut_8, 
    'x_deprecated_option__mutmut_9': x_deprecated_option__mutmut_9, 
    'x_deprecated_option__mutmut_10': x_deprecated_option__mutmut_10, 
    'x_deprecated_option__mutmut_11': x_deprecated_option__mutmut_11, 
    'x_deprecated_option__mutmut_12': x_deprecated_option__mutmut_12
}

def deprecated_option(*args, **kwargs):
    result = _mutmut_trampoline(x_deprecated_option__mutmut_orig, x_deprecated_option__mutmut_mutants, args, kwargs)
    return result 

deprecated_option.__signature__ = _mutmut_signature(x_deprecated_option__mutmut_orig)
x_deprecated_option__mutmut_orig.__name__ = 'x_deprecated_option'


def x_file_supports_color__mutmut_orig(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "Pocket PC" and (plat != "win32" or "ANSICON" in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_1(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = None
    supported_platform = plat != "Pocket PC" and (plat != "win32" or "ANSICON" in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_2(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = None

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_3(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "Pocket PC" or (plat != "win32" or "ANSICON" in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_4(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat == "Pocket PC" and (plat != "win32" or "ANSICON" in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_5(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "XXPocket PCXX" and (plat != "win32" or "ANSICON" in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_6(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "pocket pc" and (plat != "win32" or "ANSICON" in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_7(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "POCKET PC" and (plat != "win32" or "ANSICON" in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_8(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "Pocket PC" and (plat != "win32" and "ANSICON" in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_9(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "Pocket PC" and (plat == "win32" or "ANSICON" in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_10(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "Pocket PC" and (plat != "XXwin32XX" or "ANSICON" in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_11(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "Pocket PC" and (plat != "WIN32" or "ANSICON" in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_12(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "Pocket PC" and (plat != "win32" or "XXANSICONXX" in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_13(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "Pocket PC" and (plat != "win32" or "ansicon" in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_14(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "Pocket PC" and (plat != "win32" or "ANSICON" not in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_15(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "Pocket PC" and (plat != "win32" or "ANSICON" in os.environ)

    is_a_tty = None

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_16(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "Pocket PC" and (plat != "win32" or "ANSICON" in os.environ)

    is_a_tty = file_is_a_tty(None)

    return supported_platform and is_a_tty


def x_file_supports_color__mutmut_17(file_obj: IO[AnyStr]) -> bool:
    """
    Returns True if the running system's terminal supports color.

    Borrowed from Django
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "Pocket PC" and (plat != "win32" or "ANSICON" in os.environ)

    is_a_tty = file_is_a_tty(file_obj)

    return supported_platform or is_a_tty

x_file_supports_color__mutmut_mutants : ClassVar[MutantDict] = {
'x_file_supports_color__mutmut_1': x_file_supports_color__mutmut_1, 
    'x_file_supports_color__mutmut_2': x_file_supports_color__mutmut_2, 
    'x_file_supports_color__mutmut_3': x_file_supports_color__mutmut_3, 
    'x_file_supports_color__mutmut_4': x_file_supports_color__mutmut_4, 
    'x_file_supports_color__mutmut_5': x_file_supports_color__mutmut_5, 
    'x_file_supports_color__mutmut_6': x_file_supports_color__mutmut_6, 
    'x_file_supports_color__mutmut_7': x_file_supports_color__mutmut_7, 
    'x_file_supports_color__mutmut_8': x_file_supports_color__mutmut_8, 
    'x_file_supports_color__mutmut_9': x_file_supports_color__mutmut_9, 
    'x_file_supports_color__mutmut_10': x_file_supports_color__mutmut_10, 
    'x_file_supports_color__mutmut_11': x_file_supports_color__mutmut_11, 
    'x_file_supports_color__mutmut_12': x_file_supports_color__mutmut_12, 
    'x_file_supports_color__mutmut_13': x_file_supports_color__mutmut_13, 
    'x_file_supports_color__mutmut_14': x_file_supports_color__mutmut_14, 
    'x_file_supports_color__mutmut_15': x_file_supports_color__mutmut_15, 
    'x_file_supports_color__mutmut_16': x_file_supports_color__mutmut_16, 
    'x_file_supports_color__mutmut_17': x_file_supports_color__mutmut_17
}

def file_supports_color(*args, **kwargs):
    result = _mutmut_trampoline(x_file_supports_color__mutmut_orig, x_file_supports_color__mutmut_mutants, args, kwargs)
    return result 

file_supports_color.__signature__ = _mutmut_signature(x_file_supports_color__mutmut_orig)
x_file_supports_color__mutmut_orig.__name__ = 'x_file_supports_color'


def x_file_supports_unicode__mutmut_orig(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr(file_obj, "encoding", None)
    if not encoding:
        return False

    codec_info = codecs.lookup(encoding)

    return "utf" in codec_info.name


def x_file_supports_unicode__mutmut_1(file_obj: IO[AnyStr]) -> bool:
    encoding = None
    if not encoding:
        return False

    codec_info = codecs.lookup(encoding)

    return "utf" in codec_info.name


def x_file_supports_unicode__mutmut_2(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr(None, "encoding", None)
    if not encoding:
        return False

    codec_info = codecs.lookup(encoding)

    return "utf" in codec_info.name


def x_file_supports_unicode__mutmut_3(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr(file_obj, None, None)
    if not encoding:
        return False

    codec_info = codecs.lookup(encoding)

    return "utf" in codec_info.name


def x_file_supports_unicode__mutmut_4(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr("encoding", None)
    if not encoding:
        return False

    codec_info = codecs.lookup(encoding)

    return "utf" in codec_info.name


def x_file_supports_unicode__mutmut_5(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr(file_obj, None)
    if not encoding:
        return False

    codec_info = codecs.lookup(encoding)

    return "utf" in codec_info.name


def x_file_supports_unicode__mutmut_6(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr(file_obj, "encoding", )
    if not encoding:
        return False

    codec_info = codecs.lookup(encoding)

    return "utf" in codec_info.name


def x_file_supports_unicode__mutmut_7(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr(file_obj, "XXencodingXX", None)
    if not encoding:
        return False

    codec_info = codecs.lookup(encoding)

    return "utf" in codec_info.name


def x_file_supports_unicode__mutmut_8(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr(file_obj, "ENCODING", None)
    if not encoding:
        return False

    codec_info = codecs.lookup(encoding)

    return "utf" in codec_info.name


def x_file_supports_unicode__mutmut_9(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr(file_obj, "encoding", None)
    if encoding:
        return False

    codec_info = codecs.lookup(encoding)

    return "utf" in codec_info.name


def x_file_supports_unicode__mutmut_10(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr(file_obj, "encoding", None)
    if not encoding:
        return True

    codec_info = codecs.lookup(encoding)

    return "utf" in codec_info.name


def x_file_supports_unicode__mutmut_11(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr(file_obj, "encoding", None)
    if not encoding:
        return False

    codec_info = None

    return "utf" in codec_info.name


def x_file_supports_unicode__mutmut_12(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr(file_obj, "encoding", None)
    if not encoding:
        return False

    codec_info = codecs.lookup(None)

    return "utf" in codec_info.name


def x_file_supports_unicode__mutmut_13(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr(file_obj, "encoding", None)
    if not encoding:
        return False

    codec_info = codecs.lookup(encoding)

    return "XXutfXX" in codec_info.name


def x_file_supports_unicode__mutmut_14(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr(file_obj, "encoding", None)
    if not encoding:
        return False

    codec_info = codecs.lookup(encoding)

    return "UTF" in codec_info.name


def x_file_supports_unicode__mutmut_15(file_obj: IO[AnyStr]) -> bool:
    encoding = getattr(file_obj, "encoding", None)
    if not encoding:
        return False

    codec_info = codecs.lookup(encoding)

    return "utf" not in codec_info.name

x_file_supports_unicode__mutmut_mutants : ClassVar[MutantDict] = {
'x_file_supports_unicode__mutmut_1': x_file_supports_unicode__mutmut_1, 
    'x_file_supports_unicode__mutmut_2': x_file_supports_unicode__mutmut_2, 
    'x_file_supports_unicode__mutmut_3': x_file_supports_unicode__mutmut_3, 
    'x_file_supports_unicode__mutmut_4': x_file_supports_unicode__mutmut_4, 
    'x_file_supports_unicode__mutmut_5': x_file_supports_unicode__mutmut_5, 
    'x_file_supports_unicode__mutmut_6': x_file_supports_unicode__mutmut_6, 
    'x_file_supports_unicode__mutmut_7': x_file_supports_unicode__mutmut_7, 
    'x_file_supports_unicode__mutmut_8': x_file_supports_unicode__mutmut_8, 
    'x_file_supports_unicode__mutmut_9': x_file_supports_unicode__mutmut_9, 
    'x_file_supports_unicode__mutmut_10': x_file_supports_unicode__mutmut_10, 
    'x_file_supports_unicode__mutmut_11': x_file_supports_unicode__mutmut_11, 
    'x_file_supports_unicode__mutmut_12': x_file_supports_unicode__mutmut_12, 
    'x_file_supports_unicode__mutmut_13': x_file_supports_unicode__mutmut_13, 
    'x_file_supports_unicode__mutmut_14': x_file_supports_unicode__mutmut_14, 
    'x_file_supports_unicode__mutmut_15': x_file_supports_unicode__mutmut_15
}

def file_supports_unicode(*args, **kwargs):
    result = _mutmut_trampoline(x_file_supports_unicode__mutmut_orig, x_file_supports_unicode__mutmut_mutants, args, kwargs)
    return result 

file_supports_unicode.__signature__ = _mutmut_signature(x_file_supports_unicode__mutmut_orig)
x_file_supports_unicode__mutmut_orig.__name__ = 'x_file_supports_unicode'


def x_file_is_a_tty__mutmut_orig(file_obj: IO[AnyStr]) -> bool:
    return hasattr(file_obj, "isatty") and file_obj.isatty()


def x_file_is_a_tty__mutmut_1(file_obj: IO[AnyStr]) -> bool:
    return hasattr(file_obj, "isatty") or file_obj.isatty()


def x_file_is_a_tty__mutmut_2(file_obj: IO[AnyStr]) -> bool:
    return hasattr(None, "isatty") and file_obj.isatty()


def x_file_is_a_tty__mutmut_3(file_obj: IO[AnyStr]) -> bool:
    return hasattr(file_obj, None) and file_obj.isatty()


def x_file_is_a_tty__mutmut_4(file_obj: IO[AnyStr]) -> bool:
    return hasattr("isatty") and file_obj.isatty()


def x_file_is_a_tty__mutmut_5(file_obj: IO[AnyStr]) -> bool:
    return hasattr(file_obj, ) and file_obj.isatty()


def x_file_is_a_tty__mutmut_6(file_obj: IO[AnyStr]) -> bool:
    return hasattr(file_obj, "XXisattyXX") and file_obj.isatty()


def x_file_is_a_tty__mutmut_7(file_obj: IO[AnyStr]) -> bool:
    return hasattr(file_obj, "ISATTY") and file_obj.isatty()

x_file_is_a_tty__mutmut_mutants : ClassVar[MutantDict] = {
'x_file_is_a_tty__mutmut_1': x_file_is_a_tty__mutmut_1, 
    'x_file_is_a_tty__mutmut_2': x_file_is_a_tty__mutmut_2, 
    'x_file_is_a_tty__mutmut_3': x_file_is_a_tty__mutmut_3, 
    'x_file_is_a_tty__mutmut_4': x_file_is_a_tty__mutmut_4, 
    'x_file_is_a_tty__mutmut_5': x_file_is_a_tty__mutmut_5, 
    'x_file_is_a_tty__mutmut_6': x_file_is_a_tty__mutmut_6, 
    'x_file_is_a_tty__mutmut_7': x_file_is_a_tty__mutmut_7
}

def file_is_a_tty(*args, **kwargs):
    result = _mutmut_trampoline(x_file_is_a_tty__mutmut_orig, x_file_is_a_tty__mutmut_mutants, args, kwargs)
    return result 

file_is_a_tty.__signature__ = _mutmut_signature(x_file_is_a_tty__mutmut_orig)
x_file_is_a_tty__mutmut_orig.__name__ = 'x_file_is_a_tty'


def x_unwrap__mutmut_orig(string: str) -> str:
    string = string.replace("\n", " ")
    string = re.sub(r"\s+", " ", string)
    return string.strip()


def x_unwrap__mutmut_1(string: str) -> str:
    string = None
    string = re.sub(r"\s+", " ", string)
    return string.strip()


def x_unwrap__mutmut_2(string: str) -> str:
    string = string.replace(None, " ")
    string = re.sub(r"\s+", " ", string)
    return string.strip()


def x_unwrap__mutmut_3(string: str) -> str:
    string = string.replace("\n", None)
    string = re.sub(r"\s+", " ", string)
    return string.strip()


def x_unwrap__mutmut_4(string: str) -> str:
    string = string.replace(" ")
    string = re.sub(r"\s+", " ", string)
    return string.strip()


def x_unwrap__mutmut_5(string: str) -> str:
    string = string.replace("\n", )
    string = re.sub(r"\s+", " ", string)
    return string.strip()


def x_unwrap__mutmut_6(string: str) -> str:
    string = string.replace("XX\nXX", " ")
    string = re.sub(r"\s+", " ", string)
    return string.strip()


def x_unwrap__mutmut_7(string: str) -> str:
    string = string.replace("\n", "XX XX")
    string = re.sub(r"\s+", " ", string)
    return string.strip()


def x_unwrap__mutmut_8(string: str) -> str:
    string = string.replace("\n", " ")
    string = None
    return string.strip()


def x_unwrap__mutmut_9(string: str) -> str:
    string = string.replace("\n", " ")
    string = re.sub(None, " ", string)
    return string.strip()


def x_unwrap__mutmut_10(string: str) -> str:
    string = string.replace("\n", " ")
    string = re.sub(r"\s+", None, string)
    return string.strip()


def x_unwrap__mutmut_11(string: str) -> str:
    string = string.replace("\n", " ")
    string = re.sub(r"\s+", " ", None)
    return string.strip()


def x_unwrap__mutmut_12(string: str) -> str:
    string = string.replace("\n", " ")
    string = re.sub(" ", string)
    return string.strip()


def x_unwrap__mutmut_13(string: str) -> str:
    string = string.replace("\n", " ")
    string = re.sub(r"\s+", string)
    return string.strip()


def x_unwrap__mutmut_14(string: str) -> str:
    string = string.replace("\n", " ")
    string = re.sub(r"\s+", " ", )
    return string.strip()


def x_unwrap__mutmut_15(string: str) -> str:
    string = string.replace("\n", " ")
    string = re.sub(r"XX\s+XX", " ", string)
    return string.strip()


def x_unwrap__mutmut_16(string: str) -> str:
    string = string.replace("\n", " ")
    string = re.sub(r"\s+", " ", string)
    return string.strip()


def x_unwrap__mutmut_17(string: str) -> str:
    string = string.replace("\n", " ")
    string = re.sub(r"\s+", " ", string)
    return string.strip()


def x_unwrap__mutmut_18(string: str) -> str:
    string = string.replace("\n", " ")
    string = re.sub(r"\s+", "XX XX", string)
    return string.strip()

x_unwrap__mutmut_mutants : ClassVar[MutantDict] = {
'x_unwrap__mutmut_1': x_unwrap__mutmut_1, 
    'x_unwrap__mutmut_2': x_unwrap__mutmut_2, 
    'x_unwrap__mutmut_3': x_unwrap__mutmut_3, 
    'x_unwrap__mutmut_4': x_unwrap__mutmut_4, 
    'x_unwrap__mutmut_5': x_unwrap__mutmut_5, 
    'x_unwrap__mutmut_6': x_unwrap__mutmut_6, 
    'x_unwrap__mutmut_7': x_unwrap__mutmut_7, 
    'x_unwrap__mutmut_8': x_unwrap__mutmut_8, 
    'x_unwrap__mutmut_9': x_unwrap__mutmut_9, 
    'x_unwrap__mutmut_10': x_unwrap__mutmut_10, 
    'x_unwrap__mutmut_11': x_unwrap__mutmut_11, 
    'x_unwrap__mutmut_12': x_unwrap__mutmut_12, 
    'x_unwrap__mutmut_13': x_unwrap__mutmut_13, 
    'x_unwrap__mutmut_14': x_unwrap__mutmut_14, 
    'x_unwrap__mutmut_15': x_unwrap__mutmut_15, 
    'x_unwrap__mutmut_16': x_unwrap__mutmut_16, 
    'x_unwrap__mutmut_17': x_unwrap__mutmut_17, 
    'x_unwrap__mutmut_18': x_unwrap__mutmut_18
}

def unwrap(*args, **kwargs):
    result = _mutmut_trampoline(x_unwrap__mutmut_orig, x_unwrap__mutmut_mutants, args, kwargs)
    return result 

unwrap.__signature__ = _mutmut_signature(x_unwrap__mutmut_orig)
x_unwrap__mutmut_orig.__name__ = 'x_unwrap'


def x_format_float_with_sig_figs__mutmut_orig(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_1(value: float, sig_figs: int = 4, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_2(value: float, sig_figs: int = 3, trim_zeroes=True) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_3(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value != 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_4(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 1:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_5(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "XX0XX"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_6(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = None
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_7(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs + 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_8(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) - sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_9(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(None) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_10(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(+math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_11(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(None)) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_12(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(None))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_13(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 2
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_14(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision <= 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_15(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 1:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_16(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = None
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_17(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 1
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_18(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = None

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_19(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(None, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_20(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=None)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_21(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_22(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, )

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_23(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "XX{:.{precision}f}XX".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_24(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{PRECISION}F}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_25(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes or "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_26(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "XX.XX" in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_27(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." not in result:
        result = result.rstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_28(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = None

    return result


def x_format_float_with_sig_figs__mutmut_29(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip(None)

    return result


def x_format_float_with_sig_figs__mutmut_30(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").lstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_31(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip(None).rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_32(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.lstrip("0").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_33(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("XX0XX").rstrip(".")

    return result


def x_format_float_with_sig_figs__mutmut_34(value: float, sig_figs: int = 3, trim_zeroes=False) -> str:
    """
    Format a float to a string with a specific number of significant figures.
    Doesn't use scientific notation.
    """
    if value == 0:
        return "0"

    precision = math.ceil(-math.log10(abs(value))) + sig_figs - 1
    if precision < 0:
        precision = 0
    result = "{:.{precision}f}".format(value, precision=precision)

    if trim_zeroes and "." in result:
        result = result.rstrip("0").rstrip("XX.XX")

    return result

x_format_float_with_sig_figs__mutmut_mutants : ClassVar[MutantDict] = {
'x_format_float_with_sig_figs__mutmut_1': x_format_float_with_sig_figs__mutmut_1, 
    'x_format_float_with_sig_figs__mutmut_2': x_format_float_with_sig_figs__mutmut_2, 
    'x_format_float_with_sig_figs__mutmut_3': x_format_float_with_sig_figs__mutmut_3, 
    'x_format_float_with_sig_figs__mutmut_4': x_format_float_with_sig_figs__mutmut_4, 
    'x_format_float_with_sig_figs__mutmut_5': x_format_float_with_sig_figs__mutmut_5, 
    'x_format_float_with_sig_figs__mutmut_6': x_format_float_with_sig_figs__mutmut_6, 
    'x_format_float_with_sig_figs__mutmut_7': x_format_float_with_sig_figs__mutmut_7, 
    'x_format_float_with_sig_figs__mutmut_8': x_format_float_with_sig_figs__mutmut_8, 
    'x_format_float_with_sig_figs__mutmut_9': x_format_float_with_sig_figs__mutmut_9, 
    'x_format_float_with_sig_figs__mutmut_10': x_format_float_with_sig_figs__mutmut_10, 
    'x_format_float_with_sig_figs__mutmut_11': x_format_float_with_sig_figs__mutmut_11, 
    'x_format_float_with_sig_figs__mutmut_12': x_format_float_with_sig_figs__mutmut_12, 
    'x_format_float_with_sig_figs__mutmut_13': x_format_float_with_sig_figs__mutmut_13, 
    'x_format_float_with_sig_figs__mutmut_14': x_format_float_with_sig_figs__mutmut_14, 
    'x_format_float_with_sig_figs__mutmut_15': x_format_float_with_sig_figs__mutmut_15, 
    'x_format_float_with_sig_figs__mutmut_16': x_format_float_with_sig_figs__mutmut_16, 
    'x_format_float_with_sig_figs__mutmut_17': x_format_float_with_sig_figs__mutmut_17, 
    'x_format_float_with_sig_figs__mutmut_18': x_format_float_with_sig_figs__mutmut_18, 
    'x_format_float_with_sig_figs__mutmut_19': x_format_float_with_sig_figs__mutmut_19, 
    'x_format_float_with_sig_figs__mutmut_20': x_format_float_with_sig_figs__mutmut_20, 
    'x_format_float_with_sig_figs__mutmut_21': x_format_float_with_sig_figs__mutmut_21, 
    'x_format_float_with_sig_figs__mutmut_22': x_format_float_with_sig_figs__mutmut_22, 
    'x_format_float_with_sig_figs__mutmut_23': x_format_float_with_sig_figs__mutmut_23, 
    'x_format_float_with_sig_figs__mutmut_24': x_format_float_with_sig_figs__mutmut_24, 
    'x_format_float_with_sig_figs__mutmut_25': x_format_float_with_sig_figs__mutmut_25, 
    'x_format_float_with_sig_figs__mutmut_26': x_format_float_with_sig_figs__mutmut_26, 
    'x_format_float_with_sig_figs__mutmut_27': x_format_float_with_sig_figs__mutmut_27, 
    'x_format_float_with_sig_figs__mutmut_28': x_format_float_with_sig_figs__mutmut_28, 
    'x_format_float_with_sig_figs__mutmut_29': x_format_float_with_sig_figs__mutmut_29, 
    'x_format_float_with_sig_figs__mutmut_30': x_format_float_with_sig_figs__mutmut_30, 
    'x_format_float_with_sig_figs__mutmut_31': x_format_float_with_sig_figs__mutmut_31, 
    'x_format_float_with_sig_figs__mutmut_32': x_format_float_with_sig_figs__mutmut_32, 
    'x_format_float_with_sig_figs__mutmut_33': x_format_float_with_sig_figs__mutmut_33, 
    'x_format_float_with_sig_figs__mutmut_34': x_format_float_with_sig_figs__mutmut_34
}

def format_float_with_sig_figs(*args, **kwargs):
    result = _mutmut_trampoline(x_format_float_with_sig_figs__mutmut_orig, x_format_float_with_sig_figs__mutmut_mutants, args, kwargs)
    return result 

format_float_with_sig_figs.__signature__ = _mutmut_signature(x_format_float_with_sig_figs__mutmut_orig)
x_format_float_with_sig_figs__mutmut_orig.__name__ = 'x_format_float_with_sig_figs'


def x_strtobool__mutmut_orig(val: str) -> bool:
    return val.lower() in {"y", "yes", "t", "true", "on", "1"}


def x_strtobool__mutmut_1(val: str) -> bool:
    return val.upper() in {"y", "yes", "t", "true", "on", "1"}


def x_strtobool__mutmut_2(val: str) -> bool:
    return val.lower() not in {"y", "yes", "t", "true", "on", "1"}


def x_strtobool__mutmut_3(val: str) -> bool:
    return val.lower() in {"XXyXX", "yes", "t", "true", "on", "1"}


def x_strtobool__mutmut_4(val: str) -> bool:
    return val.lower() in {"Y", "yes", "t", "true", "on", "1"}


def x_strtobool__mutmut_5(val: str) -> bool:
    return val.lower() in {"y", "XXyesXX", "t", "true", "on", "1"}


def x_strtobool__mutmut_6(val: str) -> bool:
    return val.lower() in {"y", "YES", "t", "true", "on", "1"}


def x_strtobool__mutmut_7(val: str) -> bool:
    return val.lower() in {"y", "yes", "XXtXX", "true", "on", "1"}


def x_strtobool__mutmut_8(val: str) -> bool:
    return val.lower() in {"y", "yes", "T", "true", "on", "1"}


def x_strtobool__mutmut_9(val: str) -> bool:
    return val.lower() in {"y", "yes", "t", "XXtrueXX", "on", "1"}


def x_strtobool__mutmut_10(val: str) -> bool:
    return val.lower() in {"y", "yes", "t", "TRUE", "on", "1"}


def x_strtobool__mutmut_11(val: str) -> bool:
    return val.lower() in {"y", "yes", "t", "true", "XXonXX", "1"}


def x_strtobool__mutmut_12(val: str) -> bool:
    return val.lower() in {"y", "yes", "t", "true", "ON", "1"}


def x_strtobool__mutmut_13(val: str) -> bool:
    return val.lower() in {"y", "yes", "t", "true", "on", "XX1XX"}

x_strtobool__mutmut_mutants : ClassVar[MutantDict] = {
'x_strtobool__mutmut_1': x_strtobool__mutmut_1, 
    'x_strtobool__mutmut_2': x_strtobool__mutmut_2, 
    'x_strtobool__mutmut_3': x_strtobool__mutmut_3, 
    'x_strtobool__mutmut_4': x_strtobool__mutmut_4, 
    'x_strtobool__mutmut_5': x_strtobool__mutmut_5, 
    'x_strtobool__mutmut_6': x_strtobool__mutmut_6, 
    'x_strtobool__mutmut_7': x_strtobool__mutmut_7, 
    'x_strtobool__mutmut_8': x_strtobool__mutmut_8, 
    'x_strtobool__mutmut_9': x_strtobool__mutmut_9, 
    'x_strtobool__mutmut_10': x_strtobool__mutmut_10, 
    'x_strtobool__mutmut_11': x_strtobool__mutmut_11, 
    'x_strtobool__mutmut_12': x_strtobool__mutmut_12, 
    'x_strtobool__mutmut_13': x_strtobool__mutmut_13
}

def strtobool(*args, **kwargs):
    result = _mutmut_trampoline(x_strtobool__mutmut_orig, x_strtobool__mutmut_mutants, args, kwargs)
    return result 

strtobool.__signature__ = _mutmut_signature(x_strtobool__mutmut_orig)
x_strtobool__mutmut_orig.__name__ = 'x_strtobool'
