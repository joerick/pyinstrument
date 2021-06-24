# Reference

## The Profiler object

```{eval-rst}
.. autoclass:: pyinstrument.Profiler
    :members:
    :special-members: __enter__
```

## Sessions

```{eval-rst}
.. autoclass:: pyinstrument.session.Session
    :members:
```

## Renderers

Renderers transform a tree of {class}`Frame` objects into some form of output.

Rendering has two steps:

1. First, the renderer will 'preprocess' the Frame tree, applying each processor in the ``processor`` property, in turn.
2. The resulting tree is renderered into the desired format.

Therefore, rendering can be customised by changing the ``processors`` property. For example, you can disable time-aggregation (making the profile into a timeline) by removing {func}`aggregate_repeated_calls`.

```{eval-rst}
.. autoclass:: pyinstrument.renderers.Renderer
    :members:

.. autoclass:: pyinstrument.renderers.ConsoleRenderer

.. autoclass:: pyinstrument.renderers.HTMLRenderer

.. autoclass:: pyinstrument.renderers.JSONRenderer
```

## Processors

```{eval-rst}
.. automodule:: pyinstrument.processors
    :members:
```
