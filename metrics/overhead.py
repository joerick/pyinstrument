import cProfile
import profile
from timeit import Timer

import django.conf
import django.template.loader

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


def test_func_template():
    django.template.loader.render_to_string("template.html")


t = Timer(stmt=test_func_template)
test_func = lambda: t.repeat(number=4000)

# base
base_timings = test_func()

# # profile
# p = profile.Profile()
# profile_timings = p.runcall(lambda: test_func())

# cProfile
cp = cProfile.Profile()
cProfile_timings = cp.runcall(test_func)

# pyinstrument
profiler = pyinstrument.Profiler()
profiler.start()
pyinstrument_timings = test_func()
profiler.stop()

# pyinstrument timeline
# profiler = pyinstrument.Profiler(timeline=True)
# profiler.start()
# pyinstrument_timeline_timings = test_func()
# profiler.stop()

with open("out.html", "w") as f:
    f.write(profiler.output_html())

print(profiler.output_text(unicode=True, color=True))

graph_data = (
    ("Base timings", min(base_timings)),
    # ('profile', min(profile_timings)),
    ("cProfile", min(cProfile_timings)),
    ("pyinstrument", min(pyinstrument_timings)),
    # ('pyinstrument timeline', min(pyinstrument_timeline_timings)),
)

from ascii_graph import Pyasciigraph

graph = Pyasciigraph(float_format="{0:.3f}")
for line in graph.graph("Profiler overhead", graph_data):
    print(line)
