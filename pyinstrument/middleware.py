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


def get_renderer(path) -> Renderer:
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


class ProfilerMiddleware(MiddlewareMixin):  # type: ignore
    def process_request(self, request):
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

    def process_response(self, request, response):
        if hasattr(request, "profiler"):
            profile_session = request.profiler.stop()

            configured_renderer = getattr(settings, "PYINSTRUMENT_PROFILE_DIR_RENDERER", None)
            renderer = get_renderer(configured_renderer)

            output = renderer.render(profile_session)

            profile_dir = getattr(settings, "PYINSTRUMENT_PROFILE_DIR", None)

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace("/", "_")[:100]

            # Swap ? for _qs_ on Windows, as it does not support ? in filenames.
            if sys.platform in ["win32", "cygwin"]:
                path = path.replace("?", "_qs_")

            if profile_dir:
                default_filename = "{total_time:.3f}s {path} {timestamp:.0f}.{ext}"
                filename = getattr(settings, "PYINSTRUMENT_FILENAME", default_filename).format(
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
