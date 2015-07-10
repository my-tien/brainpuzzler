from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^segem-challenge/', include('challenge.urls')),
                       url(r'^jobs/', include('jobs.urls')))
