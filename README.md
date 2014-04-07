pyinstrument
============

A Python profiler that records the call stack of the executing code, instead
of just the final function in it.

![Screenshot](screenshot.png)

Sample console output

    0.098 _render     django/template/base.py:133
    └─ 0.096 render   django/template/base.py:836
       ├─ 0.085 render_node   django/template/base.py:853
       │  └─ 0.085 render     django/template/loader_tags.py:48
       │     ├─ 0.068 render  django/template/base.py:836
       │     │  ├─ 0.053 render_node  django/template/base.py:853
       │     │  │  └─ 0.052 render    django/template/defaulttags.py:387
       │     │  │     ├─ 0.013 wrapper    django/utils/functional.py:197
       │     │  │     │  └─ 0.007 strip_spaces_between_tags   django/utils/html.py:153
       │     │  │     │     └─ 0.006 sub  re.py:144
       │     │  │     │        └─ 0.004 _compile  re.py:226
       │     │  │     └─ 0.011 render     django/template/base.py:836
       │     │  │        ├─ 0.005 mark_safe   django/utils/safestring.py:104
       │     │  │        ├─ 0.001 render_node     django/template/base.py:853
       │     │  │        └─ 0.001 force_text  django/utils/encoding.py:84
       │     │  ├─ 0.002 force_text   django/utils/encoding.py:84
       │     │  └─ 0.002 mark_safe    django/utils/safestring.py:104
       │     ├─ 0.004 push    django/template/context.py:37
       │     ├─ 0.002 __init__    django/template/loader_tags.py:42
       │     ├─ 0.001 pop     django/template/context.py:42
       │     ├─ 0.001 pop     django/template/loader_tags.py:26
       │     ├─ 0.001 __setitem__     django/template/context.py:47
       │     └─ 0.001 push    django/template/loader_tags.py:32
       └─ 0.004 force_text    django/utils/encoding.py:84

It uses a **statistical profiler**, meaning the code samples the stack
periodically (by default, every 1 ms). This is lower overhead than event-
based profiling (as done by `profile` and `cProfile`), but does not currently
work on Windows due to the lack of `signal.setitimer`. In these cases, you can
still use the old event-based profiler `pyinstrument.EventProfiler`.

This module is still very young, so I'd love any feedback/bug reports/pull
requests!

Installation
------------

    pip install -e git+https://github.com/joerick/pyinstrument.git#egg=pyinstrument

Usage
-----

-   **Django**
    
    Add `pyinstrument.middleware.ProfilerMiddleware` to `MIDDLEWARE_CLASSES`.
    If you want to profile your middleware as well as your view (you probably
    do) then put it at the start of the list.

    Then add `?profile` to the end of the request URL to activate the
    profiler.

-   **Stand-alone**

        from pyinstrument import Profiler

        profiler = Profiler()
        profiler.start()

        # code you want to profile

        profiler.stop()

        print(profiler.output_text(unicode=True))

    If your terminal doesn't support unicode, you can omit the `unicode=True`
    flag.

Known issues
------------

-   Statistical profiling doesn't work under Windows. Use
    `pyinstrument.EventProfiler` instead.

-   When profiling Django, I'd recommend disabling django-debug-toolbar,
    django-devserver etc., as their instrumentation distort timings.

Why?
----

The standard Python profilers [`profile`][1] and [`cProfile`][2] produce
output where time is totalled according to the time spent in each function.
This is great, but it falls down when you profile code where most time is
spent in framework code that you're not familiar with.

[1]: http://docs.python.org/2/library/profile.html#module-profile
[2]: http://docs.python.org/2/library/profile.html#module-cProfile

Here's an example of profile output when using Django.

    151940 function calls (147672 primitive calls) in 1.696 seconds

       Ordered by: cumulative time

       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    1.696    1.696 profile:0(<code object <module> at 0x1053d6a30, file "./manage.py", line 2>)
            1    0.001    0.001    1.693    1.693 manage.py:2(<module>)
            1    0.000    0.000    1.586    1.586 __init__.py:394(execute_from_command_line)
            1    0.000    0.000    1.586    1.586 __init__.py:350(execute)
            1    0.000    0.000    1.142    1.142 __init__.py:254(fetch_command)
           43    0.013    0.000    1.124    0.026 __init__.py:1(<module>)
          388    0.008    0.000    1.062    0.003 re.py:226(_compile)
          158    0.005    0.000    1.048    0.007 sre_compile.py:496(compile)
            1    0.001    0.001    1.042    1.042 __init__.py:78(get_commands)
          153    0.001    0.000    1.036    0.007 re.py:188(compile)
      106/102    0.001    0.000    1.030    0.010 __init__.py:52(__getattr__)
            1    0.000    0.000    1.029    1.029 __init__.py:31(_setup)
            1    0.000    0.000    1.021    1.021 __init__.py:57(_configure_logging)
            2    0.002    0.001    1.011    0.505 log.py:1(<module>)


When you're using big frameworks like Django, it's very hard to understand how
your own code relates to these traces.

Pyinstrument records the entire stack each time a function is called, so
tracking expensive calls is much easier.
