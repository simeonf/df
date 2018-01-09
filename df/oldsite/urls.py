from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<category>[\w]+)/(?P<slug>[.\w-]+)$', views.old_urls_redirect),
]
