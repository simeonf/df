from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
                       url(r'^(?P<category>[\w]+)/(?P<slug>[.\w-]+)$', views.old_urls_redirect),
                       
)
