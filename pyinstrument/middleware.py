from django.http import HttpResponse
from django.conf import settings
from pyinstrument import Profiler
import time
import os
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class ProfilerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        profile_dir = getattr(settings, 'PYINSTRUMENT_PROFILE_DIR', None)

        if getattr(settings, 'PYINSTRUMENT_URL_ARGUMENT', 'profile') in request.GET or profile_dir:
            profiler = Profiler()
            profiler.start()

            request.profiler = profiler


    def process_response(self, request, response):
        if hasattr(request, 'profiler'):
            request.profiler.stop()

            output_html = request.profiler.output_html()

            profile_dir = getattr(settings, 'PYINSTRUMENT_PROFILE_DIR', None)

            # Limit the length of the file name (255 characters is the max limit on major current OS, but it is rather
            # high and the other parts (see line 36) are to be taken into account; so a hundred will be fine here).
            path = request.get_full_path().replace('/', '_')[:100]

            if profile_dir:
                filename = '{total_time:.3f}s {path} {timestamp:.0f}.html'.format(
                    total_time=request.profiler.root_frame().time(),
                    path=path,
                    timestamp=time.time()
                )

                file_path = os.path.join(profile_dir, filename)

                if not os.path.exists(profile_dir):
                    os.mkdir(profile_dir)

                with open(file_path, 'w') as f:
                    f.write(output_html)

            if getattr(settings, 'PYINSTRUMENT_URL_ARGUMENT', 'profile') in request.GET:
                return HttpResponse(output_html)
            else:
                return response
        else:
            return response
