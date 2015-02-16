import django.template.loader
import django.conf
import sys

sys.path.append('django_test')
django.conf.settings.configure(INSTALLED_APPS=(), TEMPLATE_DIRS=('.', 'examples',))

for x in range(0,100):
    django.template.loader.render_to_string('template.html')
