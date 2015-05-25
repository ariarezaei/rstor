from django.conf.urls import patterns, url

from monitor import views

urlpatterns = patterns('monitor.views',
                       url(r'^$', views.index),
                       url(r'^livestat/(?P<cache_name>\w+)$', views.instant_stat),
                       url(r'^dbstat$', views.retrieve_db),
                       url(r'^(?P<cache_name>\w+)$', views.cache_config),
                       url(r'^$'))