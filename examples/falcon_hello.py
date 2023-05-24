import time

from pyinstrument import Profiler

try:
    import falcon

    PROFILING = True  # Use environment variable for setting it
except ImportError:
    print("This example requires falcon.")
    print("Install using `pip install falcon`.")
    exit(1)


class ProfilerMiddleware:
    def __init__(self, interval=0.01):
        self.profiler = Profiler(interval=interval)

    def process_request(self, req, resp):
        self.profiler.start()

    def process_response(self, req, resp, resource, req_succeeded):
        self.profiler.stop()
        self.profiler.open_in_browser()  # Autoloads the file in default browser


class HelloResource:
    def on_get(self, req, resp):
        time.sleep(1)
        resp.media = "hello"


app = falcon.App()
if PROFILING:
    app.add_middleware(ProfilerMiddleware())
app.add_route("/", HelloResource())
