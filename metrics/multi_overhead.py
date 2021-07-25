import cProfile
import profile
import re
import sys
import time
from timeit import Timer

import django.conf

import pyinstrument

django.conf.settings.configure(
    INSTALLED_APPS=(),
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                "./examples/django_example/django_example/templates",
            ],
        }
    ],
)
django.setup()


def test_func_re():
    re.compile(
        r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
    )


def test_func_template():
    django.template.loader.render_to_string("template.html")


# heat caches
test_func_template()


def time_base(function, repeats):
    timer = Timer(stmt=function)
    return timer.repeat(number=repeats)


def time_profile(function, repeats):
    timer = Timer(stmt=function)
    p = profile.Profile()
    return p.runcall(lambda: timer.repeat(number=repeats))


def time_cProfile(function, repeats):
    timer = Timer(stmt=function)
    p = cProfile.Profile()
    return p.runcall(lambda: timer.repeat(number=repeats))


def time_pyinstrument(function, repeats):
    timer = Timer(stmt=function)
    p = pyinstrument.Profiler()
    p.start()
    result = timer.repeat(number=repeats)
    p.stop()
    return result


profilers = (
    ("Base", time_base),
    # ('profile', time_profile),
    ("cProfile", time_cProfile),
    ("pyinstrument", time_pyinstrument),
)

tests = (
    ("re.compile", test_func_re, 120000),
    ("django template render", test_func_template, 400),
)


def timings_for_test(test_func, repeats):
    results = []
    for profiler_tuple in profilers:
        time = profiler_tuple[1](test_func, repeats)
        results += (profiler_tuple[0], min(time))

    return results


# print header
for column in [""] + [test[0] for test in tests]:
    sys.stdout.write(f"{column:>24}")

sys.stdout.write("\n")

for profiler_tuple in profilers:
    sys.stdout.write(f"{profiler_tuple[0]:>24}")
    sys.stdout.flush()
    for test_tuple in tests:
        time = min(profiler_tuple[1](test_tuple[1], test_tuple[2])) * 10
        sys.stdout.write(f"{time:>24.2f}")
        sys.stdout.flush()
    sys.stdout.write("\n")
