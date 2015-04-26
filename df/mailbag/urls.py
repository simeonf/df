from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='mailbag_home'),
                       url(r'^/(?P<slug>[\w-]+)$', views.mailbag, name='mailbag_detail'),

                       
)
