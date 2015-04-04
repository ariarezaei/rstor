from django.conf.urls import patterns, url

from monitor import views

urlpatterns = patterns('shop.views',
                       url(r'^$', views.index))