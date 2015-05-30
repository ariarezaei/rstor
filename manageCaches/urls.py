from django.conf.urls import patterns, url

from manageCaches import views

urlpatterns = patterns('manageCaches.views',
                       url(r'^create$', views.create),
                       url(r'^edit$', views.edit),
                       url(r'^remove/(?P<cache_name>\w+)$', views.edit)
                       )