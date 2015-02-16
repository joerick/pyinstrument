import django.template.loader
import django.conf
from timeit import Timer
import sys
import profile
import cProfile
import pyinstrument

sys.path.append('django_test')
django.conf.settings.configure(INSTALLED_APPS=(), TEMPLATE_DIRS=('.'))

def test_func_template():
    django.template.loader.render_to_string('test_template.html')

# base
t = Timer(stmt=test_func_template)

base_timings = t.repeat(number=200)

# profile
p = profile.Profile()

profile_timings = p.runcall(lambda: t.repeat(number=200))

# cProfile
cp = cProfile.Profile()

cProfile_timings = cp.runcall(lambda: t.repeat(number=200))

# pyinstrument stat
profiler = pyinstrument.Profiler()

profiler.start()

pyinstrument_stat_timings = t.repeat(number=200)

profiler.stop()

# pyinstrument event
profiler = pyinstrument.Profiler(use_signal=False)

profiler.start()

pyinstrument_event_timings = t.repeat(number=200)

profiler.stop()

# pyinstrument stat
profiler = pyinstrument.Profiler(timeline=True)

profiler.start()

pyinstrument_stat_timeline_timings = t.repeat(number=200)

profiler.stop()

# pyinstrument event timeline
profiler = pyinstrument.Profiler(use_signal=False, timeline=True)

profiler.start()

pyinstrument_event_timeline_timings = t.repeat(number=200)

profiler.stop()

# import pdb; pdb.set_trace()

with open('out.html', 'w') as f:
    f.write(profiler.output_html())

print profiler.output_text(unicode=True, color=True)

print '      Base timings: %s' % base_timings
print '           profile: %s' % profile_timings
print '          cProfile: %s' % cProfile_timings
print ' pyinstrument stat: %s' % pyinstrument_stat_timings
print 'pyinstrument event: %s' % pyinstrument_event_timings
print ' pyi timeline stat: %s' % pyinstrument_stat_timeline_timings
print 'pyi timeline event: %s' % pyinstrument_event_timeline_timings
