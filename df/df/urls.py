from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from article.feed import ArticlesFeed

import debug_toolbar
import sidebar.views
import search.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rss$', ArticlesFeed()),
    url(r'^', include('article.urls')),
    url(r'^home-video$', sidebar.views.dvd),
    url(r'^now-playing$', sidebar.views.theater),
    url(r'^sections/', include('oldsite.urls')),
    url(r'^search$', search.views.search),
    url(r'^mail', include('mailbag.urls')),
]


if settings.DEBUG:
    urlpatterns.extend([
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ])

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
