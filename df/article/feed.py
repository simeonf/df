from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from .models import Article


class ArticlesFeed(Feed):
    title = "DecentFilms.com"
    link = "http://decentfilms.com"
    description = "Decent Films Guide"

    def items(self):
        return Article.objects.filter(display=True).order_by('-dt')[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.blurb

    def item_link(self, item):
        return "http://decentfilms.com" + item.get_absolute_url()
