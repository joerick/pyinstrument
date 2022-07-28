User guide
----------

### Installation

```{include} ../README.md
---
relative-docs: docs/
relative-images:
start-after: '<!-- MARK installation start -->'
end-before: '<!-- MARK installation end -->'
---
```

### Profile a Python script

Call Pyinstrument directly from the command line. Instead of writing
`python script.py`, type `pyinstrument script.py`. Your script will run as
normal, and at the end (or when you press `^C`), Pyinstrument will output a
colored summary showing where most of the time was spent.

Here are the options you can use:

    Usage: pyinstrument [options] scriptfile [arg] ...

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      --load-prev=ID        instead of running a script, load a previous report
      -m MODULE_NAME        run library module as a script, like 'python -m
                            module'
      --from-path           (POSIX only) instead of the working directory, look
                            for scriptfile in the PATH environment variable
      -o OUTFILE, --outfile=OUTFILE
                            save to <outfile>
      -r RENDERER, --renderer=RENDERER
                            how the report should be rendered. One of: 'text',
                            'html', 'json', 'speedscope', or python import path
                            to a renderer class
      -t, --timeline        render as a timeline - preserve ordering and don't
                            condense repeated calls
      --hide=EXPR           glob-style pattern matching the file paths whose
                            frames to hide. Defaults to '*/lib/*'.
      --hide-regex=REGEX    regex matching the file paths whose frames to hide.
                            Useful if --hide doesn't give enough control.
      --show=EXPR           glob-style pattern matching the file paths whose
                            frames to show, regardless of --hide or --hide-regex.
                            For example, use --show '*/<library>/*' to show frames
                            within a library that would otherwise be hidden.
      --show-regex=REGEX    regex matching the file paths whose frames to always
                            show. Useful if --show doesn't give enough control.
      --show-all            show everything
      --unicode             (text renderer only) force unicode text output
      --no-unicode          (text renderer only) force ascii text output
      --color               (text renderer only) force ansi color text output
      --no-color            (text renderer only) force no color text output

**Protip:** `-r html` will give you a interactive profile report as HTML - you
can really explore this way!

### Profile a specific chunk of code

Pyinstrument also has a Python API. Just surround your code with Pyinstrument,
like this:

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
profiler = Profiler(interval=0.0001)
...
```

Experiment with the interval value to see different depths, but keep in mind
that smaller intervals could affect the performance overhead of profiling.

**Protip:** To explore the profile in a web browser, use
{meth}`profiler.open_in_browser() <pyinstrument.Profiler.open_in_browser>`. To
save this HTML for later, use
{meth}`profiler.output_html() <pyinstrument.Profiler.output_html>`.

### Profile code in Jupyter/IPython
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

### Profile a web request in Django

To profile Django web requests, add
`pyinstrument.middleware.ProfilerMiddleware` to `MIDDLEWARE` in your
`settings.py`.

Once installed, add `?profile` to the end of a request URL to activate the
profiler. Your request will run as normal, but instead of getting the response,
you'll get pyinstrument's analysis of the request in a web page.

If you're writing an API, it's not easy to change the URL when you want to
profile something. In this case, add  `PYINSTRUMENT_PROFILE_DIR = 'profiles'`
to your `settings.py`. Pyinstrument will profile every request and save the
HTML output to the folder `profiles` in your working directory.

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

### Profile a web request in Flask

A simple setup to profile a Flask application is the following:

```python
from flask import Flask, g, make_response, request
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

### Profile a web request in FastAPI

To profile call stacks in FastAPI, you can write a middleware extension for
pyinstrument.

Create an async function and decorate with `app.middleware('http')` where
app is the name of your FastAPI application instance.

Make sure you configure a setting to only make this available when required.

```python
from pyinstrument import Profiler


PROFILING = True  # Set this from a settings model

if PROFILING:
    @app.middleware("http")
    async def profile_request(request: Request, call_next):
        profiling = request.query_params.get("profile", False)
        if profiling:
            profiler = Profiler(interval=settings.profiling_interval, async_mode="enabled")
            profiler.start()
            await call_next(request)
            profiler.stop()
            return HTMLResponse(profiler.output_html())
        else:
            return await call_next(request)
```

To invoke, make any request to your application with the GET parameter
`profile=1` and it will print the HTML result from pyinstrument.

### Profile Pytest tests

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
    with open(results_file, "w", encoding="utf-8") as f_html:
        f_html.write(profiler.output_html())
```

This will generate a HTML file for each test node in your test suite inside
the `.profiles` directory.

### Profile something else?

I'd love to have more ways to profile using Pyinstrument - e.g. other web
frameworks. PRs are encouraged!
