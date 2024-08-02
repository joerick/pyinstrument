# API Reference

## Command line interface

``pyinstrument`` works just like ``python``, on the command line, so you can
call your scripts like ``pyinstrument script.py`` or ``pyinstrument -m
my_module``.

When your script ends, or when you kill it with `ctrl-c`, pyinstrument will
print a profile report to the console.

```{program-output} pyinstrument --help
```

## Python API

The Python API is also available, for calling pyinstrument directly from
Python and writing integrations with with other tools.

### The `profile` function

For example:

```python
with pyinstrument.profile():
    time.sleep(1)
```

This will print something like:

```
pyinstrument ........................................
.
.  Block at testfile.py:2
.
.  1.000 <module>  testfile.py:1
.  └─ 1.000 sleep  <built-in>
.
.....................................................
```

You can also use it as a function/method decorator, like this:

```python
@pyinstrument.profile()
def my_function():
    time.sleep(1)
```

```{eval-rst}
.. function:: pyinstrument.profile(*, interval=0.001, async_mode="disabled", \
                                 use_timing_thread=None, renderer=None, \
                                 target_description=None)

    Creates a context-manager or function decorator object, which profiles the given code and prints the output to stdout.

    The *interval*, *async_mode* and *use_timing_thread* parameters are passed through to the underlying :class:`pyinstrument.Profiler` object.

    You can pass a renderer to customise the output. By default, it uses a :class:`ConsoleRenderer <pyinstrument.renderers.ConsoleRenderer>` with `short_mode` set.

```

### The Profiler object

```{eval-rst}
.. autoclass:: pyinstrument.Profiler
    :members:
    :special-members: __enter__
```

### Sessions

```{eval-rst}
.. autoclass:: pyinstrument.session.Session
    :members:
```

### Renderers

Renderers transform a tree of {class}`Frame` objects into some form of output.

Rendering has two steps:

1. First, the renderer will 'preprocess' the Frame tree, applying each processor in the ``processor`` property, in turn.
2. The resulting tree is rendered into the desired format.

Therefore, rendering can be customised by changing the ``processors`` property. For example, you can disable time-aggregation (making the profile into a timeline) by removing {func}`aggregate_repeated_calls`.

```{eval-rst}
.. autoclass:: pyinstrument.renderers.FrameRenderer
    :members:

.. autoclass:: pyinstrument.renderers.ConsoleRenderer

.. autoclass:: pyinstrument.renderers.HTMLRenderer

.. autoclass:: pyinstrument.renderers.JSONRenderer

.. autoclass:: pyinstrument.renderers.SpeedscopeRenderer
```

### Processors

```{eval-rst}
.. automodule:: pyinstrument.processors
    :members:
```

### Internals notes

Frames are recorded by the Profiler in a time-linear fashion. While profiling,
the profiler builds a list of frame stacks, with the frames having in format:

    function_name <null> filename <null> function_line_number

When profiling is complete, this list is turned into a tree structure of
Frame objects. This tree contains all the information as gathered by the
profiler, suitable for a flame render.

#### Frame objects, the call tree, and processors

The frames are assembled to a call tree by the profiler session. The
time-linearity is retained at this stage.

Before rendering, the call tree is then fed through a sequence of 'processors'
to transform the tree for output.

The most interesting is `aggregate_repeated_calls`, which combines different
instances of function calls into the same frame. This is intuitive as a
summary of where time was spent during execution.

The rest of the processors focus on removing or hiding irrelevant Frames
from the output.

#### Self time frames vs. frame.self_time

Self time nodes exist to record time spent in a node, but not in its children.
But normal frame objects can have self_time too. Why? frame.self_time is used
to store the self_time of any nodes that were removed during processing.
