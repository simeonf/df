from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from article.feed import ArticlesFeed

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'df.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^rss$', ArticlesFeed()),
                       url(r'^', include('article.urls')),
                       url(r'^home-video$', 'sidebar.views.dvd'),
                       url(r'^now-playing$', 'sidebar.views.theater'),
                       url(r'^sections/', include('oldsite.urls')),
                       url(r'^search$', 'search.views.search'),
                       url(r'^mail', include('mailbag.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'uploads/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
