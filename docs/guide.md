User guide
==========

## Installation

```{include} ../README.md
---
relative-docs: docs/
relative-images:
start-after: '<!-- MARK installation start -->'
end-before: '<!-- MARK installation end -->'
---
```

## Profile a Python script

Call Pyinstrument directly from the command line. Instead of writing
`python script.py`, type `pyinstrument script.py`. Your script will run as
normal, and at the end (or when you press `^C`), Pyinstrument will output a
colored summary showing where most of the time was spent.

Here are the options you can use:

```{program-output} python -m pyinstrument --help
```

**Protip:** `-r html` will give you a interactive profile report as HTML - you
can really explore this way!

## Profile a Python CLI command

For profiling an installed Python script via the
["console_script" entry point](https://packaging.python.org/en/latest/specifications/entry-points/#use-for-scripts),
call Pyinstrument directly from the command line with the `--from-path` flag.
Instead of writing `cli-script`, type `pyinstrument --from-path cli-script`.
Your script will run as normal, and at the end (or when you press `^C`),
Pyinstrument will output a colored summary showing where most of the time was
spent.

## Profile a specific chunk of code

Pyinstrument also has a Python API. You can use a with-block, like this:

```python
import pyinstrument

with pyinstrument.profile():
    # code you want to profile
```

Or you can decorate a function/method, like this:

```python
import pyinstrument

@pyinstrument.profile()
def my_function():
    # code you want to profile

```

There's also a lower-level API called Profiler, that's more flexible:

```python
from pyinstrument import Profiler

profiler = Profiler()
profiler.start()

# code you want to profile

profiler.stop()
profiler.print()
```

If you get "No samples were recorded." because your code executed in under
1ms, hooray! If you **still** want to instrument the code, set an interval
value smaller than the default 0.001 (1 millisecond) like this:

```python
pyinstrument.profile(interval=0.0001)
# or,
profiler = Profiler(interval=0.0001)
...
```

Experiment with the interval value to see different depths, but keep in mind
that smaller intervals could affect the performance overhead of profiling.

**Protip:** To explore the profile in a web browser, use
{meth}`profiler.open_in_browser() <pyinstrument.Profiler.open_in_browser>`. To
save this HTML for later, use
{meth}`profiler.output_html() <pyinstrument.Profiler.output_html>`.

## Profile code in Jupyter/IPython

Via [IPython magics](https://ipython.readthedocs.io/en/stable/interactive/magics.html),
you can profile a line or a cell in IPython or Jupyter.

Example:
```python
%load_ext pyinstrument
```

```
%%pyinstrument
import time

def a():
    b()
    c()
def b():
    d()
def c():
    d()
def d():
    e()
def e():
    time.sleep(1)
a()
```

To customize options, see `%%pyinstrument??`.

## Profile a web request in Django

To profile Django web requests, add
`pyinstrument.middleware.ProfilerMiddleware` to `MIDDLEWARE` in your
`settings.py`.

**Profile specific request**

Once installed, add `?profile` to the end of a request URL to activate the
profiler. Your request will run as normal, but instead of getting the response,
you'll get pyinstrument's analysis of the request in a web page.

**Save all requests to a directory**

If you're writing an API, it's not easy to change the URL when you want to
profile something. In this case, add  `PYINSTRUMENT_PROFILE_DIR = 'profiles'`
to your `settings.py`. Pyinstrument will profile every request and save the
HTML output to the folder `profiles` in your working directory.

**Custom file name by string**

You can further customize the filename by adding `PYINSTRUMENT_FILENAME` to
`settings.py`, default value is `"{total_time:.3f}s {path} {timestamp:.0f}.{ext}"`.

**Custom file name by callback function**

For more control you can provide a callback function by adding
`PYINSTRUMENT_FILENAME_CALLBACK` to `settings.py`, that returns a filename as a string.

```python
def get_pyinstrument_filename(request, session, renderer):
    path = request.get_full_path().replace("/", "_")[:100]
    ext = renderer.output_file_extension
    filename = f"{request.method}_{session.duration}{path}.{ext}"
    return filename

PYINSTRUMENT_FILENAME_CALLBACK = get_pyinstrument_filename
```

(This callback takes precedence over `PYINSTRUMENT_FILENAME`).

**Control shown profiling page**

If you want to show the profiling page depending on the request you can define
`PYINSTRUMENT_SHOW_CALLBACK` as dotted path to a function used for determining
whether the page should show or not.
You can provide your own function callback(request) which returns True or False
in your settings.py.

```python
def custom_show_pyinstrument(request):
    return request.user.is_superuser


PYINSTRUMENT_SHOW_CALLBACK = "%s.custom_show_pyinstrument" % __name__
```

You can configure the profile output type using setting's variable `PYINSTRUMENT_PROFILE_DIR_RENDERER`.
Default value is `pyinstrument.renderers.HTMLRenderer`. The supported renderers are
`pyinstrument.renderers.JSONRenderer`, `pyinstrument.renderers.HTMLRenderer`,
`pyinstrument.renderers.SpeedscopeRenderer`.

## Profile a web request in Flask

A simple setup to profile a Flask application is the following:

```python
from flask import Flask, g, make_response, request
from pyinstrument import Profiler

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
```

This will check for the `?profile` query param on each request and if found,
it starts profiling. After each request where the profiler was running it
creates the html output and returns that instead of the actual response.

## Profile a web request in FastAPI

To profile call stacks in FastAPI, you can write a middleware extension for
pyinstrument.

```{caution}
Only `async` path operation functions are profiled with this approach. Routes that are defined without `async def` are executed in a separate execution thread, and therefore not profiled by this approach.
See [issue #257](https://github.com/joerick/pyinstrument/issues/257) and [FastAPI Concurrency and async / await](https://fastapi.tiangolo.com/async/) for more information.
```

Create an async function and decorate with `app.middleware('http')` where
app is the name of your FastAPI application instance.

Make sure you configure a setting to only make this available when required.

```python
from fastapi import Request
from fastapi.responses import HTMLResponse
from pyinstrument import Profiler


PROFILING = True  # Set this from a settings model

if PROFILING:
    @app.middleware("http")
    async def profile_request(request: Request, call_next):
        profiling = request.query_params.get("profile", False)
        if profiling:
            profiler = Profiler()
            profiler.start()
            await call_next(request)
            profiler.stop()
            return HTMLResponse(profiler.output_html())
        else:
            return await call_next(request)
```

To invoke, make any request to your application with the GET parameter
`profile=1` and it will print the HTML result from pyinstrument.

## Profile a web request in Falcon

For profile call stacks in Falcon, you can write a middleware extension using
pyinstrument.

Create a middleware class and start the profiler at `process_request` and stop it at `process_response`.
The middleware can be added to the app.

Make sure you configure a setting to only make this available when required.

```python
from pyinstrument import Profiler
import falcon

class ProfilerMiddleware:
    def __init__(self, interval=0.01):
        self.profiler = Profiler(interval=interval)

    def process_request(self, req, resp):
        self.profiler.start()

    def process_response(self, req, resp, resource, req_succeeded):
        self.profiler.stop()
        self.profiler.open_in_browser()

PROFILING = True  # Set this from a settings model

app = falcon.App()
if PROFILING:
    app.add_middleware(ProfilerMiddleware())
```

To invoke, make any request to your application and it launch a new window
printing the HTML result from pyinstrument.

## Profile a web request in Litestar

Minimal application setup allowing request profiling.

The middleware overrides the response to return a profiling report in HTML format.

```python
from __future__ import annotations

from asyncio import sleep

from litestar import Litestar, get
from litestar.middleware import MiddlewareProtocol
from litestar.types import ASGIApp, Message, Receive, Scope, Send

from pyinstrument import Profiler


class ProfilingMiddleware(MiddlewareProtocol):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)  # type: ignore
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        profiler = Profiler(interval=0.001, async_mode="enabled")
        profiler.start()
        profile_html: str | None = None

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                profiler.stop()
                nonlocal profile_html
                profile_html = profiler.output_html()
                message["headers"] = [
                    (b"content-type", b"text/html; charset=utf-8"),
                    (b"content-length", str(len(profile_html)).encode()),
                ]
            elif message["type"] == "http.response.body":
                assert profile_html is not None
                message["body"] = profile_html.encode()
            await send(message)

        await self.app(scope, receive, send_wrapper)


@get("/")
async def index() -> str:
    await sleep(1)
    return "Hello, world!"


app = Litestar(
    route_handlers=[index],
    middleware=[ProfilingMiddleware],
)
```

To invoke, make any request to your application and it will return the HTML result from pyinstrument instead of your application's response.

## Profile a web request in aiohttp.web

You can use a simple middleware to profile aiohttp web server requests with
Pyinstrument:

```python
from aiohttp import web
from pyinstrument import Profiler

@web.middleware
async def profiler_middleware(request, handler):
    with Profiler() as p:
        await handler(request)
    return web.Response(text=p.output_html(), content_type="text/html")

app = web.Application(middlewares=(profiler_middleware,))
```

Pyinstrument's HTML output will be returned as response, showing the profiling
result of each request.

Make use of aiohttp.web development CLI feature to isolate configurations and
make sure profiling is only enabled when needed:

```python
...

def dev_app(argv):
    app = web.Application(middlewares=(profiler_middleware,))
    app.add_routes(routes)
    return app # for development

if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(...) # for deployment
```

```bash
python3 -m aiohttp.web app:dev_app # develop with profiling and debug enabled
python3 ./app.py # run app without profiling
```

## Profile Pytest tests

Pyinstrument can be invoked via the command-line to run pytest, giving you a
consolidated report for the test suite.

```
pyinstrument -m pytest [pytest-args...]
```

Or, to instrument specific tests, create and auto-use fixture in `conftest.py`
in your test folder:

```python
from pathlib import Path
import pytest
from pyinstrument import Profiler

TESTS_ROOT = Path.cwd()

@pytest.fixture(autouse=True)
def auto_profile(request):
    PROFILE_ROOT = (TESTS_ROOT / ".profiles")
    # Turn profiling on
    profiler = Profiler()
    profiler.start()

    yield  # Run test

    profiler.stop()
    PROFILE_ROOT.mkdir(exist_ok=True)
    results_file = PROFILE_ROOT / f"{request.node.name}.html"
    profiler.write_html(results_file)
```

This will generate a HTML file for each test node in your test suite inside
the `.profiles` directory.

## Profile something else?

I'd love to have more ways to profile using Pyinstrument - e.g. other web
frameworks. PRs are encouraged!
