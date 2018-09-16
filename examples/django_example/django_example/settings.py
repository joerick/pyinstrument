import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = 'qg7_r+b@)(--as*(4ls$j$$(9i(pl_@y$g0j0r+!=@&$he(+o%'

ROOT_URLCONF = 'django_example.urls'

INSTALLED_APPS = (
    'django_example',
    'django.contrib.contenttypes',
    'django.contrib.auth',
)

MIDDLEWARE_CLASSES = (
    'pyinstrument.middleware.ProfilerMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
