from django.http import HttpResponse
from django.conf import settings
from .profiler import Profiler
import os

class ProfilerMiddleware(object):
    def __init__(self):
        self.profiler = None

    def process_request(self, request):
        if getattr(settings, 'PYINSTRUMENT_URL_ARGUMENT', 'profile') in request.GET:
            self.profiler = Profiler()
            self.profiler.start()

    def process_response(self, request, response):
        if self.profiler:
            try:
                self.profiler.stop()

                return HttpResponse(self.profiler.output_html())
            finally:
                self.profiler = None
        else:
            return response
