import time
from datetime import datetime

from pyinstrument import Profiler

try:
    import falcon

    PROFILING = True  # Use environment variable for setting it
except ImportError:
    print("This example requires falcon.")
    print("Install using `pip install falcon`.")
    exit(1)


class ProfilerMiddleware:
    filename = "pyinstrument-profile"

    def __init__(self, interval=0.01):
        self.profiler = Profiler(interval=interval)

    def process_request(self, req, resp):
        self.profiler.start()

    def process_response(self, req, resp, resource, req_succeeded):
        self.profiler.stop()
        filename = f"{self.filename}-{datetime.now().strftime('%m%d%Y-%H%M%S')}.html"
        with open(filename, "w") as file:
            file.write(self.profiler.output_html())


class HelloResource:
    def on_get(self, req, resp):
        time.sleep(1)
        resp.media = "hello"


app = falcon.App()
if PROFILING:
    app.add_middleware(ProfilerMiddleware())
app.add_route("/", HelloResource())
