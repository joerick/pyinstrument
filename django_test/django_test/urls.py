from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django_test.views.hello_world'),

    url(r'^admin/', include(admin.site.urls)),
)
