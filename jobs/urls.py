__author__ = 'tieni'

from django.conf.urls import patterns, url

from jobs import views

urlpatterns = patterns('',
                       url(r'^job_(?P<job_id>\d+)/camp_(?P<campaign_id>\d+)/mw_(?P<worker_id>\d+)/$', views.job, name='job'),
                       url(r'index.html', views.index, name='index'),
                       )

