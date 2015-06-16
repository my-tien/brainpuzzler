__author__ = 'tieni'

from django.conf.urls import patterns, url

from challenge import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'))

