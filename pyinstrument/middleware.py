from django.http import HttpResponse
from django.conf import settings
from pyinstrument import Profiler
from pyinstrument.profiler import NotMainThreadError

not_main_thread_message = (
    'pyinstrument can only be used on the main thread. Run your server process in single-threaded '
    'mode. \n\nWith the built-in server, you can do this with '
    '\n./manage.py runserver --nothreading --noreload')


class ProfilerMiddleware(object):
    def __init__(self):
        self.profiler = None

    def process_request(self, request):
        if getattr(settings, 'PYINSTRUMENT_URL_ARGUMENT', 'profile') in request.GET:
            self.profiler = Profiler()
            try:
                self.profiler.start()
            except NotMainThreadError:
                raise NotMainThreadError(not_main_thread_message)
                self.profiler = None


    def process_response(self, request, response):
        if self.profiler:
            try:
                self.profiler.stop()

                return HttpResponse(self.profiler.output_html())
            except NotMainThreadError:
                raise NotMainThreadError(not_main_thread_message)
            finally:
                self.profiler = None
        else:
            return response
