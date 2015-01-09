__author__ = 'tieni'

from django.conf.urls import patterns, url

from jobs import views

urlpatterns = patterns('',
                       url(r'^(?job_P<job_id>\d+)/$', views.job, name='job'))