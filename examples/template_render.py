import django.template.loader
import django.conf
import sys, os

os.chdir(os.path.dirname(__file__))

django.conf.settings.configure(
    INSTALLED_APPS=(), 
    TEMPLATES=[{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['.']
    }],
)
django.setup()

for x in range(0,100):
    django.template.loader.render_to_string('template.html')
