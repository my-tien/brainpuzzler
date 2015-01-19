from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^jobs/', include('jobs.urls')),
                       url(r'^admin/', include(admin.site.urls)))
