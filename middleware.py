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

                location = os.path.dirname(os.path.abspath(__file__))

                with open(os.path.join(location, 'style.css')) as f:
                    css = f.read()

                with open(os.path.join(location, 'profile.js')) as f:
                    js = f.read()

                response = '''
                    <html>
                    <head>
                        <style>{css}</style>
                        <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
                    </head>
                    <body>
                        {body}
                        <script>{js}</script>
                    </body>
                    </html>'''.format(css=css, js=js, body=self.profiler.output_html())

                return HttpResponse(response)
            finally:
                self.profiler = None
        else:
            return response
