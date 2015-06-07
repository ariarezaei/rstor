from django.conf.urls import patterns, url

from monitor import views

urlpatterns = patterns('monitor.views',
                       url(r'^live$', views.index),
                       url(r'^live/(?P<cache_name>\w+)$', views.instant_stat),
                       url(r'^dbstat$', views.retrieve_db),
                       url(r'^config/(?P<cache_name>\w+)$', views.cache_config),
                       url(r'^$', views.stats))