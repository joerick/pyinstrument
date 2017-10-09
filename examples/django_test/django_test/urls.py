from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'django_test.views.hello_world'),
)
