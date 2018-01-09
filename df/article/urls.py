from django.conf.urls import include, url

import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    # url(r'^debug$', views.debug),
    url(r'^recent$', views.recent, name='recent'),
    url(r'^articles$', views.article_index, name='article_home'),
    url(r'^articles/(?P<slug>[.\w-]+)$', views.article, {'type': 'ARTICLE'}, name='post'),
    url(r'^blog$', views.blog_index, name='blog_home'),
    url(r'^blog/(?P<slug>[.\w-]+)$', views.article,{'type': 'POST'}),
    url(r'^reviews$', views.review_index, name='review_home'),
    url(r'^reviews/(?P<slug>[.\w-]+)$', views.article, {'type': 'REVIEW'}),
    url(r'^tags$', views.tags_index, name='tags_home'),
    url(r'^tags/(?P<slug>[^/]+)$', views.tag)
]
