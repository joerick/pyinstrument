import re
import pyinstrument
from timeit import Timer
import django.conf
import os
from django.template.loader import render_to_string
import sys
import time
import cProfile, profile

sys.path.append('django_test')

django.conf.settings.configure(INSTALLED_APPS=(), TEMPLATE_DIRS=('./examples',))

def test_func_re():
    re.compile("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")

def test_func_template():
    django.template.loader.render_to_string('template.html')

# heat caches
test_func_template()

def TestRun(object):
    def __init__(self, function, repeats):
        self.timer = Timer(stmt=function)
        self.repeats = repeats

def TestRunBase(TestRun):
    def run(self):
        return self.timer.repeat(number=self.repeats)

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

def time_pyinstrument_signal(function, repeats):
    timer = Timer(stmt=function)
    p = pyinstrument.Profiler()
    p.start()
    result = timer.repeat(number=repeats)
    p.stop()
    return result

def time_pyinstrument_event(function, repeats):
    timer = Timer(stmt=function)
    p = pyinstrument.Profiler(use_signal=False)
    p.start()
    result = timer.repeat(number=repeats)
    p.stop()
    return result

profilers = (
    ('Base', time_base),
    # ('profile', time_profile),
    ('cProfile', time_cProfile),
    ('pyinstrument (signal)', time_pyinstrument_signal),
    ('pyinstrument (event)', time_pyinstrument_event),
)

tests = (
    ('re.compile', test_func_re, 120000),
    ('django template render', test_func_template, 400),
)

def timings_for_test(test_func, repeats):
    results = []
    for profiler_tuple in profilers:
        time = profiler_tuple[1](test_func, repeats)
        results += (profiler_tuple[0], min(time))

    return results

# print header
for column in [''] + [test[0] for test in tests]:
    sys.stdout.write('{:>24}'.format(column))

sys.stdout.write('\n')

for profiler_tuple in profilers:
    sys.stdout.write('{:>24}'.format(profiler_tuple[0]))
    sys.stdout.flush()
    for test_tuple in tests:
        time = min(profiler_tuple[1](test_tuple[1], test_tuple[2])) * 10
        sys.stdout.write('{:>24.2f}'.format(time))
        sys.stdout.flush()
    sys.stdout.write('\n')
