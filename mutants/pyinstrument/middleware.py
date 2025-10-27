import io
import os
import sys
import time

from django.conf import settings
from django.http import HttpResponse
from django.utils.module_loading import import_string

from pyinstrument import Profiler
from pyinstrument.renderers import Renderer
from pyinstrument.renderers.html import HTMLRenderer

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object
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


def x_get_renderer__mutmut_orig(path) -> Renderer:
    """Return the renderer instance."""
    if path:
        try:
            renderer = import_string(path)()
        except ImportError as exc:
            print("Unable to import the class: %s" % path)
            raise exc

        if not isinstance(renderer, Renderer):
            raise ValueError(f"Renderer should subclass: {Renderer}")

        return renderer
    else:
        return HTMLRenderer()


def x_get_renderer__mutmut_1(path) -> Renderer:
    """Return the renderer instance."""
    if path:
        try:
            renderer = None
        except ImportError as exc:
            print("Unable to import the class: %s" % path)
            raise exc

        if not isinstance(renderer, Renderer):
            raise ValueError(f"Renderer should subclass: {Renderer}")

        return renderer
    else:
        return HTMLRenderer()


def x_get_renderer__mutmut_2(path) -> Renderer:
    """Return the renderer instance."""
    if path:
        try:
            renderer = import_string(None)()
        except ImportError as exc:
            print("Unable to import the class: %s" % path)
            raise exc

        if not isinstance(renderer, Renderer):
            raise ValueError(f"Renderer should subclass: {Renderer}")

        return renderer
    else:
        return HTMLRenderer()


def x_get_renderer__mutmut_3(path) -> Renderer:
    """Return the renderer instance."""
    if path:
        try:
            renderer = import_string(path)()
        except ImportError as exc:
            print(None)
            raise exc

        if not isinstance(renderer, Renderer):
            raise ValueError(f"Renderer should subclass: {Renderer}")

        return renderer
    else:
        return HTMLRenderer()


def x_get_renderer__mutmut_4(path) -> Renderer:
    """Return the renderer instance."""
    if path:
        try:
            renderer = import_string(path)()
        except ImportError as exc:
            print("Unable to import the class: %s" / path)
            raise exc

        if not isinstance(renderer, Renderer):
            raise ValueError(f"Renderer should subclass: {Renderer}")

        return renderer
    else:
        return HTMLRenderer()


def x_get_renderer__mutmut_5(path) -> Renderer:
    """Return the renderer instance."""
    if path:
        try:
            renderer = import_string(path)()
        except ImportError as exc:
            print("XXUnable to import the class: %sXX" % path)
            raise exc

        if not isinstance(renderer, Renderer):
            raise ValueError(f"Renderer should subclass: {Renderer}")

        return renderer
    else:
        return HTMLRenderer()


def x_get_renderer__mutmut_6(path) -> Renderer:
    """Return the renderer instance."""
    if path:
        try:
            renderer = import_string(path)()
        except ImportError as exc:
            print("unable to import the class: %s" % path)
            raise exc

        if not isinstance(renderer, Renderer):
            raise ValueError(f"Renderer should subclass: {Renderer}")

        return renderer
    else:
        return HTMLRenderer()


def x_get_renderer__mutmut_7(path) -> Renderer:
    """Return the renderer instance."""
    if path:
        try:
            renderer = import_string(path)()
        except ImportError as exc:
            print("UNABLE TO IMPORT THE CLASS: %S" % path)
            raise exc

        if not isinstance(renderer, Renderer):
            raise ValueError(f"Renderer should subclass: {Renderer}")

        return renderer
    else:
        return HTMLRenderer()


def x_get_renderer__mutmut_8(path) -> Renderer:
    """Return the renderer instance."""
    if path:
        try:
            renderer = import_string(path)()
        except ImportError as exc:
            print("Unable to import the class: %s" % path)
            raise exc

        if isinstance(renderer, Renderer):
            raise ValueError(f"Renderer should subclass: {Renderer}")

        return renderer
    else:
        return HTMLRenderer()


def x_get_renderer__mutmut_9(path) -> Renderer:
    """Return the renderer instance."""
    if path:
        try:
            renderer = import_string(path)()
        except ImportError as exc:
            print("Unable to import the class: %s" % path)
            raise exc

        if not isinstance(renderer, Renderer):
            raise ValueError(None)

        return renderer
    else:
        return HTMLRenderer()

x_get_renderer__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_renderer__mutmut_1': x_get_renderer__mutmut_1, 
    'x_get_renderer__mutmut_2': x_get_renderer__mutmut_2, 
    'x_get_renderer__mutmut_3': x_get_renderer__mutmut_3, 
    'x_get_renderer__mutmut_4': x_get_renderer__mutmut_4, 
    'x_get_renderer__mutmut_5': x_get_renderer__mutmut_5, 
    'x_get_renderer__mutmut_6': x_get_renderer__mutmut_6, 
    'x_get_renderer__mutmut_7': x_get_renderer__mutmut_7, 
    'x_get_renderer__mutmut_8': x_get_renderer__mutmut_8, 
    'x_get_renderer__mutmut_9': x_get_renderer__mutmut_9
}

def get_renderer(*args, **kwargs):
    result = _mutmut_trampoline(x_get_renderer__mutmut_orig, x_get_renderer__mutmut_mutants, args, kwargs)
    return result 

get_renderer.__signature__ = _mutmut_signature(x_get_renderer__mutmut_orig)
x_get_renderer__mutmut_orig.__name__ = 'x_get_renderer'


class ProfilerMiddleware(MiddlewareMixin):  # type: ignore
    def xǁProfilerMiddlewareǁprocess_request__mutmut_orig(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_1(self, request):
        profile_dir = None

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_2(self, request):
        profile_dir = getattr(None, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_3(self, request):
        profile_dir = getattr(settings, None, None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_4(self, request):
        profile_dir = getattr("PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_5(self, request):
        profile_dir = getattr(settings, None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_6(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", )

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_7(self, request):
        profile_dir = getattr(settings, "XXPYINSTRUMENT_PROFILE_DIRXX", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_8(self, request):
        profile_dir = getattr(settings, "pyinstrument_profile_dir", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_9(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = None
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_10(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(None, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_11(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, None, None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_12(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr("PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_13(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_14(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", )
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_15(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "XXPYINSTRUMENT_SHOW_CALLBACKXX", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_16(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "pyinstrument_show_callback", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_17(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = None
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_18(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(None)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_19(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(None):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_20(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = None
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_21(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = None

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_22(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: None

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_23(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: False

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_24(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) and profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_25(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request) or getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_26(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(None)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_27(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(None, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_28(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, None, "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_29(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", None) in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_30(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr("PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_31(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_32(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", ) in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_33(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "XXPYINSTRUMENT_URL_ARGUMENTXX", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_34(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "pyinstrument_url_argument", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_35(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "XXprofileXX") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_36(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "PROFILE") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_37(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") not in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_38(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = None
            profiler.start()

            request.profiler = profiler
    def xǁProfilerMiddlewareǁprocess_request__mutmut_39(self, request):
        profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

        func_or_path = getattr(settings, "PYINSTRUMENT_SHOW_CALLBACK", None)
        if isinstance(func_or_path, str):
            show_pyinstrument = import_string(func_or_path)
        elif callable(func_or_path):
            show_pyinstrument = func_or_path
        else:
            show_pyinstrument = lambda request: True

        if (
            show_pyinstrument(request)
            and getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET
        ) or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = None
    
    xǁProfilerMiddlewareǁprocess_request__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerMiddlewareǁprocess_request__mutmut_1': xǁProfilerMiddlewareǁprocess_request__mutmut_1, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_2': xǁProfilerMiddlewareǁprocess_request__mutmut_2, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_3': xǁProfilerMiddlewareǁprocess_request__mutmut_3, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_4': xǁProfilerMiddlewareǁprocess_request__mutmut_4, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_5': xǁProfilerMiddlewareǁprocess_request__mutmut_5, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_6': xǁProfilerMiddlewareǁprocess_request__mutmut_6, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_7': xǁProfilerMiddlewareǁprocess_request__mutmut_7, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_8': xǁProfilerMiddlewareǁprocess_request__mutmut_8, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_9': xǁProfilerMiddlewareǁprocess_request__mutmut_9, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_10': xǁProfilerMiddlewareǁprocess_request__mutmut_10, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_11': xǁProfilerMiddlewareǁprocess_request__mutmut_11, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_12': xǁProfilerMiddlewareǁprocess_request__mutmut_12, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_13': xǁProfilerMiddlewareǁprocess_request__mutmut_13, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_14': xǁProfilerMiddlewareǁprocess_request__mutmut_14, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_15': xǁProfilerMiddlewareǁprocess_request__mutmut_15, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_16': xǁProfilerMiddlewareǁprocess_request__mutmut_16, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_17': xǁProfilerMiddlewareǁprocess_request__mutmut_17, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_18': xǁProfilerMiddlewareǁprocess_request__mutmut_18, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_19': xǁProfilerMiddlewareǁprocess_request__mutmut_19, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_20': xǁProfilerMiddlewareǁprocess_request__mutmut_20, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_21': xǁProfilerMiddlewareǁprocess_request__mutmut_21, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_22': xǁProfilerMiddlewareǁprocess_request__mutmut_22, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_23': xǁProfilerMiddlewareǁprocess_request__mutmut_23, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_24': xǁProfilerMiddlewareǁprocess_request__mutmut_24, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_25': xǁProfilerMiddlewareǁprocess_request__mutmut_25, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_26': xǁProfilerMiddlewareǁprocess_request__mutmut_26, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_27': xǁProfilerMiddlewareǁprocess_request__mutmut_27, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_28': xǁProfilerMiddlewareǁprocess_request__mutmut_28, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_29': xǁProfilerMiddlewareǁprocess_request__mutmut_29, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_30': xǁProfilerMiddlewareǁprocess_request__mutmut_30, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_31': xǁProfilerMiddlewareǁprocess_request__mutmut_31, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_32': xǁProfilerMiddlewareǁprocess_request__mutmut_32, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_33': xǁProfilerMiddlewareǁprocess_request__mutmut_33, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_34': xǁProfilerMiddlewareǁprocess_request__mutmut_34, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_35': xǁProfilerMiddlewareǁprocess_request__mutmut_35, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_36': xǁProfilerMiddlewareǁprocess_request__mutmut_36, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_37': xǁProfilerMiddlewareǁprocess_request__mutmut_37, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_38': xǁProfilerMiddlewareǁprocess_request__mutmut_38, 
        'xǁProfilerMiddlewareǁprocess_request__mutmut_39': xǁProfilerMiddlewareǁprocess_request__mutmut_39
    }
    
    def process_request(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerMiddlewareǁprocess_request__mutmut_orig"), object.__getattribute__(self, "xǁProfilerMiddlewareǁprocess_request__mutmut_mutants"), args, kwargs, self)
        return result 
    
    process_request.__signature__ = _mutmut_signature(xǁProfilerMiddlewareǁprocess_request__mutmut_orig)
    xǁProfilerMiddlewareǁprocess_request__mutmut_orig.__name__ = 'xǁProfilerMiddlewareǁprocess_request'

    def xǁProfilerMiddlewareǁprocess_response__mutmut_orig(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_1(self, request, response):
        if hasattr(None, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_2(self, request, response):
        if hasattr(request, None):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_3(self, request, response):
        if hasattr("profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_4(self, request, response):
        if hasattr(request, ):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_5(self, request, response):
        if hasattr(request, "XXprofilerXX"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_6(self, request, response):
        if hasattr(request, "PROFILER"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_7(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = None
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_8(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = None

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_9(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "XX{total_time:.3f}s {path} {timestamp:.0f}.{ext}XX"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_10(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{TOTAL_TIME:.3F}S {PATH} {TIMESTAMP:.0F}.{EXT}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_11(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = None
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_12(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(None, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_13(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, None, None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_14(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr("PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_15(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_16(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", )
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_17(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "XXPYINSTRUMENT_PROFILE_DIR_RENDERERXX", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_18(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "pyinstrument_profile_dir_renderer", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_19(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = None

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_20(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(None)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_21(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = None

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_22(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(None)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_23(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = None

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_24(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(None, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_25(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, None, None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_26(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr("PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_27(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_28(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", )

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_29(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "XXPYINSTRUMENT_PROFILE_DIRXX", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_30(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "pyinstrument_profile_dir", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_31(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = None

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_32(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(None, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_33(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, None, None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_34(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr("PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_35(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_36(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", )

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_37(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "XXPYINSTRUMENT_FILENAME_CALLBACKXX", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_38(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "pyinstrument_filename_callback", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_39(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = None

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_40(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                None, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_41(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, None, default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_42(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", None
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_43(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_44(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_45(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_46(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "XXPYINSTRUMENT_FILENAMEXX", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_47(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "pyinstrument_filename", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_48(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = None

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_49(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace(None, "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_50(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", None)[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_51(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_52(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", )[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_53(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("XX/XX", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_54(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "XX_XX")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_55(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:101]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_56(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform not in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_57(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["XXwin32XX", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_58(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["WIN32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_59(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "XXcygwinXX"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_60(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "CYGWIN"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_61(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = None

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_62(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace(None, "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_63(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", None)

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_64(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_65(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", )

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_66(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("XX?XX", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_67(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "XX_qs_XX")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_68(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_QS_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_69(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb or callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_70(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(None):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_71(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = None
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_72(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(None, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_73(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, None, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_74(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, None)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_75(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_76(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_77(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, )
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_78(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_79(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError(None)
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_80(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("XXFilename callback return value should be a stringXX")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_81(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_82(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("FILENAME CALLBACK RETURN VALUE SHOULD BE A STRING")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_83(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = None

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_84(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=None,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_85(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=None,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_86(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=None,
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_87(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=None,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_88(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_89(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_90(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_91(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_92(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = None

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_93(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(None, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_94(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, None)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_95(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_96(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, )

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_97(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_98(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(None):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_99(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(None)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_100(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(None, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_101(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, None, encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_102(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding=None) as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_103(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open("w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_104(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_105(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", ) as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_106(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "XXwXX", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_107(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "W", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_108(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="XXutf-8XX") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_109(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="UTF-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_110(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(None)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_111(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(None, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_112(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, None, "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_113(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", None) in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_114(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr("PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_115(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_116(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", ) in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_117(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "XXPYINSTRUMENT_URL_ARGUMENTXX", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_118(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "pyinstrument_url_argument", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_119(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "XXprofileXX") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_120(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "PROFILE") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_121(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") not in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_122(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(None)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_123(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = None
                    output = renderer.render(profile_session)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_124(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = None
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_125(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(None)
                    return HttpResponse(output)  # type: ignore
            else:
                return response
        else:
            return response

    def xǁProfilerMiddlewareǁprocess_response__mutmut_126(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()
            default_filename_template = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            filename_cb = getattr(settings, "PYINSTRUMENT_FILENAME_CALLBACK", None)

            filename_template = getattr(
                settings, "PYINSTRUMENT_FILENAME", default_filename_template
            )

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                if filename_cb and callable(filename_cb):
                    filename = filename_cb(request, profile_session, renderer)
                    if not isinstance(filename, str):
                        raise ValueError("Filename callback return value should be a string")
                else:
                    filename = filename_template.format(
                        total_time=profile_session.duration,
                        path=path,
                        timestamp=time.time(),
                        ext=renderer.output_file_extension,
                    )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

            if getattr(settings, "PYINSTRUMENT_URL_ARGUMENT", "profile") in request.GET:
                if isinstance(renderer, HTMLRenderer):
                    return HttpResponse(output)  # type: ignore
                else:
                    renderer = HTMLRenderer()
                    output = renderer.render(profile_session)
                    return HttpResponse(None)  # type: ignore
            else:
                return response
        else:
            return response
    
    xǁProfilerMiddlewareǁprocess_response__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfilerMiddlewareǁprocess_response__mutmut_1': xǁProfilerMiddlewareǁprocess_response__mutmut_1, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_2': xǁProfilerMiddlewareǁprocess_response__mutmut_2, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_3': xǁProfilerMiddlewareǁprocess_response__mutmut_3, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_4': xǁProfilerMiddlewareǁprocess_response__mutmut_4, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_5': xǁProfilerMiddlewareǁprocess_response__mutmut_5, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_6': xǁProfilerMiddlewareǁprocess_response__mutmut_6, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_7': xǁProfilerMiddlewareǁprocess_response__mutmut_7, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_8': xǁProfilerMiddlewareǁprocess_response__mutmut_8, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_9': xǁProfilerMiddlewareǁprocess_response__mutmut_9, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_10': xǁProfilerMiddlewareǁprocess_response__mutmut_10, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_11': xǁProfilerMiddlewareǁprocess_response__mutmut_11, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_12': xǁProfilerMiddlewareǁprocess_response__mutmut_12, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_13': xǁProfilerMiddlewareǁprocess_response__mutmut_13, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_14': xǁProfilerMiddlewareǁprocess_response__mutmut_14, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_15': xǁProfilerMiddlewareǁprocess_response__mutmut_15, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_16': xǁProfilerMiddlewareǁprocess_response__mutmut_16, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_17': xǁProfilerMiddlewareǁprocess_response__mutmut_17, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_18': xǁProfilerMiddlewareǁprocess_response__mutmut_18, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_19': xǁProfilerMiddlewareǁprocess_response__mutmut_19, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_20': xǁProfilerMiddlewareǁprocess_response__mutmut_20, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_21': xǁProfilerMiddlewareǁprocess_response__mutmut_21, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_22': xǁProfilerMiddlewareǁprocess_response__mutmut_22, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_23': xǁProfilerMiddlewareǁprocess_response__mutmut_23, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_24': xǁProfilerMiddlewareǁprocess_response__mutmut_24, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_25': xǁProfilerMiddlewareǁprocess_response__mutmut_25, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_26': xǁProfilerMiddlewareǁprocess_response__mutmut_26, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_27': xǁProfilerMiddlewareǁprocess_response__mutmut_27, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_28': xǁProfilerMiddlewareǁprocess_response__mutmut_28, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_29': xǁProfilerMiddlewareǁprocess_response__mutmut_29, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_30': xǁProfilerMiddlewareǁprocess_response__mutmut_30, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_31': xǁProfilerMiddlewareǁprocess_response__mutmut_31, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_32': xǁProfilerMiddlewareǁprocess_response__mutmut_32, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_33': xǁProfilerMiddlewareǁprocess_response__mutmut_33, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_34': xǁProfilerMiddlewareǁprocess_response__mutmut_34, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_35': xǁProfilerMiddlewareǁprocess_response__mutmut_35, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_36': xǁProfilerMiddlewareǁprocess_response__mutmut_36, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_37': xǁProfilerMiddlewareǁprocess_response__mutmut_37, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_38': xǁProfilerMiddlewareǁprocess_response__mutmut_38, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_39': xǁProfilerMiddlewareǁprocess_response__mutmut_39, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_40': xǁProfilerMiddlewareǁprocess_response__mutmut_40, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_41': xǁProfilerMiddlewareǁprocess_response__mutmut_41, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_42': xǁProfilerMiddlewareǁprocess_response__mutmut_42, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_43': xǁProfilerMiddlewareǁprocess_response__mutmut_43, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_44': xǁProfilerMiddlewareǁprocess_response__mutmut_44, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_45': xǁProfilerMiddlewareǁprocess_response__mutmut_45, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_46': xǁProfilerMiddlewareǁprocess_response__mutmut_46, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_47': xǁProfilerMiddlewareǁprocess_response__mutmut_47, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_48': xǁProfilerMiddlewareǁprocess_response__mutmut_48, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_49': xǁProfilerMiddlewareǁprocess_response__mutmut_49, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_50': xǁProfilerMiddlewareǁprocess_response__mutmut_50, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_51': xǁProfilerMiddlewareǁprocess_response__mutmut_51, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_52': xǁProfilerMiddlewareǁprocess_response__mutmut_52, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_53': xǁProfilerMiddlewareǁprocess_response__mutmut_53, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_54': xǁProfilerMiddlewareǁprocess_response__mutmut_54, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_55': xǁProfilerMiddlewareǁprocess_response__mutmut_55, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_56': xǁProfilerMiddlewareǁprocess_response__mutmut_56, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_57': xǁProfilerMiddlewareǁprocess_response__mutmut_57, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_58': xǁProfilerMiddlewareǁprocess_response__mutmut_58, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_59': xǁProfilerMiddlewareǁprocess_response__mutmut_59, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_60': xǁProfilerMiddlewareǁprocess_response__mutmut_60, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_61': xǁProfilerMiddlewareǁprocess_response__mutmut_61, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_62': xǁProfilerMiddlewareǁprocess_response__mutmut_62, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_63': xǁProfilerMiddlewareǁprocess_response__mutmut_63, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_64': xǁProfilerMiddlewareǁprocess_response__mutmut_64, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_65': xǁProfilerMiddlewareǁprocess_response__mutmut_65, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_66': xǁProfilerMiddlewareǁprocess_response__mutmut_66, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_67': xǁProfilerMiddlewareǁprocess_response__mutmut_67, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_68': xǁProfilerMiddlewareǁprocess_response__mutmut_68, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_69': xǁProfilerMiddlewareǁprocess_response__mutmut_69, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_70': xǁProfilerMiddlewareǁprocess_response__mutmut_70, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_71': xǁProfilerMiddlewareǁprocess_response__mutmut_71, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_72': xǁProfilerMiddlewareǁprocess_response__mutmut_72, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_73': xǁProfilerMiddlewareǁprocess_response__mutmut_73, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_74': xǁProfilerMiddlewareǁprocess_response__mutmut_74, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_75': xǁProfilerMiddlewareǁprocess_response__mutmut_75, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_76': xǁProfilerMiddlewareǁprocess_response__mutmut_76, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_77': xǁProfilerMiddlewareǁprocess_response__mutmut_77, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_78': xǁProfilerMiddlewareǁprocess_response__mutmut_78, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_79': xǁProfilerMiddlewareǁprocess_response__mutmut_79, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_80': xǁProfilerMiddlewareǁprocess_response__mutmut_80, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_81': xǁProfilerMiddlewareǁprocess_response__mutmut_81, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_82': xǁProfilerMiddlewareǁprocess_response__mutmut_82, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_83': xǁProfilerMiddlewareǁprocess_response__mutmut_83, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_84': xǁProfilerMiddlewareǁprocess_response__mutmut_84, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_85': xǁProfilerMiddlewareǁprocess_response__mutmut_85, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_86': xǁProfilerMiddlewareǁprocess_response__mutmut_86, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_87': xǁProfilerMiddlewareǁprocess_response__mutmut_87, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_88': xǁProfilerMiddlewareǁprocess_response__mutmut_88, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_89': xǁProfilerMiddlewareǁprocess_response__mutmut_89, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_90': xǁProfilerMiddlewareǁprocess_response__mutmut_90, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_91': xǁProfilerMiddlewareǁprocess_response__mutmut_91, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_92': xǁProfilerMiddlewareǁprocess_response__mutmut_92, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_93': xǁProfilerMiddlewareǁprocess_response__mutmut_93, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_94': xǁProfilerMiddlewareǁprocess_response__mutmut_94, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_95': xǁProfilerMiddlewareǁprocess_response__mutmut_95, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_96': xǁProfilerMiddlewareǁprocess_response__mutmut_96, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_97': xǁProfilerMiddlewareǁprocess_response__mutmut_97, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_98': xǁProfilerMiddlewareǁprocess_response__mutmut_98, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_99': xǁProfilerMiddlewareǁprocess_response__mutmut_99, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_100': xǁProfilerMiddlewareǁprocess_response__mutmut_100, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_101': xǁProfilerMiddlewareǁprocess_response__mutmut_101, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_102': xǁProfilerMiddlewareǁprocess_response__mutmut_102, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_103': xǁProfilerMiddlewareǁprocess_response__mutmut_103, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_104': xǁProfilerMiddlewareǁprocess_response__mutmut_104, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_105': xǁProfilerMiddlewareǁprocess_response__mutmut_105, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_106': xǁProfilerMiddlewareǁprocess_response__mutmut_106, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_107': xǁProfilerMiddlewareǁprocess_response__mutmut_107, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_108': xǁProfilerMiddlewareǁprocess_response__mutmut_108, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_109': xǁProfilerMiddlewareǁprocess_response__mutmut_109, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_110': xǁProfilerMiddlewareǁprocess_response__mutmut_110, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_111': xǁProfilerMiddlewareǁprocess_response__mutmut_111, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_112': xǁProfilerMiddlewareǁprocess_response__mutmut_112, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_113': xǁProfilerMiddlewareǁprocess_response__mutmut_113, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_114': xǁProfilerMiddlewareǁprocess_response__mutmut_114, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_115': xǁProfilerMiddlewareǁprocess_response__mutmut_115, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_116': xǁProfilerMiddlewareǁprocess_response__mutmut_116, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_117': xǁProfilerMiddlewareǁprocess_response__mutmut_117, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_118': xǁProfilerMiddlewareǁprocess_response__mutmut_118, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_119': xǁProfilerMiddlewareǁprocess_response__mutmut_119, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_120': xǁProfilerMiddlewareǁprocess_response__mutmut_120, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_121': xǁProfilerMiddlewareǁprocess_response__mutmut_121, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_122': xǁProfilerMiddlewareǁprocess_response__mutmut_122, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_123': xǁProfilerMiddlewareǁprocess_response__mutmut_123, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_124': xǁProfilerMiddlewareǁprocess_response__mutmut_124, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_125': xǁProfilerMiddlewareǁprocess_response__mutmut_125, 
        'xǁProfilerMiddlewareǁprocess_response__mutmut_126': xǁProfilerMiddlewareǁprocess_response__mutmut_126
    }
    
    def process_response(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfilerMiddlewareǁprocess_response__mutmut_orig"), object.__getattribute__(self, "xǁProfilerMiddlewareǁprocess_response__mutmut_mutants"), args, kwargs, self)
        return result 
    
    process_response.__signature__ = _mutmut_signature(xǁProfilerMiddlewareǁprocess_response__mutmut_orig)
    xǁProfilerMiddlewareǁprocess_response__mutmut_orig.__name__ = 'xǁProfilerMiddlewareǁprocess_response'
