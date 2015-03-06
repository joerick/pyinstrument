from django.http import HttpResponse
from django.conf import settings
from pyinstrument import Profiler
from pyinstrument.profiler import NotMainThreadError
import time
import os

not_main_thread_message = (
    "pyinstrument can only be used on the main thread in signal mode. Run your server process in "
    "single-threaded mode. \n\n"
    "With the built-in server, you can do this with\n"
    "./manage.py runserver --nothreading --noreload\n\n"
    "Alternatively, you can set 'PYINSTRUMENT_USE_SIGNAL = False' in your settings.py to run in"
    "'setprofile' mode. For more information, see\n"
    "https://github.com/joerick/pyinstrument#signal-or-setprofile-mode")


class ProfilerMiddleware(object):
    def process_request(self, request):
        profile_dir = getattr(settings, 'PYINSTRUMENT_PROFILE_DIR', None)
        use_signal = getattr(settings, 'PYINSTRUMENT_USE_SIGNAL', True)
        collect_args = getattr(settings, 'PYINSTRUMENT_COLLECT_ARGS', False)

        profiler = None
        if getattr(settings, 'PYINSTRUMENT_URL_COLLECT_ARGS_ARGUMENT', 'profile_collect_args') in request.GET:
            profiler = Profiler(use_signal=use_signal, collect_args=True)
        elif getattr(settings, 'PYINSTRUMENT_URL_ARGUMENT', 'profile') in request.GET or profile_dir:
            profiler = Profiler(use_signal=use_signal, collect_args=collect_args)

        if profiler:
            try:
                profiler.start()
                request.profiler = profiler
            except NotMainThreadError:
                raise NotMainThreadError(not_main_thread_message)


    def process_response(self, request, response):
        if hasattr(request, 'profiler'):
            try:
                request.profiler.stop()

                output_html = request.profiler.output_html()

                profile_dir = getattr(settings, 'PYINSTRUMENT_PROFILE_DIR', None)

                if profile_dir:
                    filename = '{total_time:.3f}s {path} {timestamp:.0f}.html'.format(
                        total_time=request.profiler.root_frame().time(),
                        path=request.get_full_path().replace('/', '_'),
                        timestamp=time.time()
                    )

                    file_path = os.path.join(profile_dir, filename)

                    if not os.path.exists(profile_dir):
                        os.mkdir(profile_dir)

                    with open(file_path, 'w') as f:
                        f.write(output_html)
                if any((trig in request.GET for trig in [getattr(settings, 'PYINSTRUMENT_URL_COLLECT_ARGS_ARGUMENT', 'profile_collect_args'), getattr(settings, 'PYINSTRUMENT_URL_ARGUMENT', 'profile')])):
                    return HttpResponse(output_html)
                else:
                    return response
            except NotMainThreadError:
                raise NotMainThreadError(not_main_thread_message)
        else:
            return response
