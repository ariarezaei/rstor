from django.conf.urls import patterns, url

from monitor import views

urlpatterns = patterns('monitor.views',
                       url(r'^$', views.index),
                       url(r'^livestat$', views.instant_stat))