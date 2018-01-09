from django.conf.urls import include, url

import views

urlpatterns = [
    url(r'^$', views.index, name='mailbag_home'),
    url(r'^/(?P<slug>[\w-]+)$', views.mailbag, name='mailbag_detail'),
]
