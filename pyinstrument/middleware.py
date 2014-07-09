from django.http import HttpResponse
from django.conf import settings
from pyinstrument import Profiler
from pyinstrument.profiler import NotMainThreadError

not_main_thread_message = (
    'pyinstrument can only be used on the main thread in signal mode. Run your server process in '
    'single-threaded mode. \n\n'
    'With the built-in server, you can do this with\n'
    './manage.py runserver --nothreading --noreload\n\n'
    "Alternatively, you can set 'PYINSTRUMENT_USE_SIGNAL = False' in your settings.py to run in"
    "'setprofile' mode. For more information, see\n"
    'https://github.com/joerick/pyinstrument#signal-or-setprofile-mode')


class ProfilerMiddleware(object):
    def process_request(self, request):
        use_signal = getattr(settings, 'PYINSTRUMENT_USE_SIGNAL', True)

        if getattr(settings, 'PYINSTRUMENT_URL_ARGUMENT', 'profile') in request.GET:
            profiler = Profiler(use_signal=use_signal)
            try:
                profiler.start()
                request.profiler = profiler
            except NotMainThreadError:
                raise NotMainThreadError(not_main_thread_message)


    def process_response(self, request, response):
        if hasattr(request, 'profiler'):
            try:
                request.profiler.stop()

                return HttpResponse(request.profiler.output_html())
            except NotMainThreadError:
                raise NotMainThreadError(not_main_thread_message)
        else:
            return response
