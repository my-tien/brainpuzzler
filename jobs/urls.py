__author__ = 'tieni'

from django.conf.urls import patterns, url

from jobs import views

urlpatterns = patterns('',
                       url(r'^job_(?P<job_id>\d+)/camp_(?P<campaign_id>\.+)/mw_(?P<worker_id>\.+)/$', views.job, name='job'),
                       url(r'^job_(?P<job_id>\d+)/submit/$', views.job_submit, name='job_submit'),
                       url(r'index.html', views.index, name='index'),
                       )

