__author__ = 'tieni'

from django.conf.urls import patterns, url

from jobs import views

urlpatterns = patterns('',
   url(r'^get_job/camp_(?P<camp_id>.+)/mw_(?P<mw_id>.+)/rand_(?P<rand_key>.+)/$', views.get_job, name='get_job'),
   url(r'^job_(?P<job_id>-?\d+)/camp_(?P<campaign_id>.+)/mw_(?P<worker_id>.+)/rand_(?P<rand_key>.+)/$', views.job, name='job'),
   url(r'^job_(?P<job_id>-?\d+)/submit/$', views.job_submit, name='job_submit')
   )

