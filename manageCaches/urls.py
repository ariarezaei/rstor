from django.conf.urls import patterns, url

from manageCaches import views

urlpatterns = patterns('manageCaches.views',
                       url(r'^create$', views.create),
                       url(r'^edit/(?P<cache_name>\w+)$', views.edit)
                       )