import time

from pyinstrument import Profiler

try:
    from flask import Flask, g, make_response, request
except ImportError:
    print("This example requires Flask.")
    print("Install using `pip install flask`.")
    exit(1)

app = Flask(__name__)


@app.before_request
def before_request():
    if "profile" in request.args:
        g.profiler = Profiler()
        g.profiler.start()


@app.after_request
def after_request(response):
    if not hasattr(g, "profiler"):
        return response
    g.profiler.stop()
    output_html = g.profiler.output_html()
    return make_response(output_html)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/sleep")
def sleep():
    time.sleep(0.1)
    return "Good morning!"


@app.route("/dosomething")
def do_something():
    import requests

    requests.get("http://google.com")
    return "Google says hello!"
