from itertools import chain

from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import HttpResponsePermanentRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page

from utility import page, sorta

from .models import Article, Tags, Genre
from mailbag.models import MailBag

PER_PAGE = 25


def debug(request):
  return render(request, "article/debug.html")

@cache_page(180)
def article_index(request):
    paginator = Paginator(Article.articles.all().order_by("-dt"), 20)
    return render(request, "article/archive.html", {'articles': page(request, paginator),
                                                    'blurb': "Articles index",
                                                    'title': 'Articles'})

@cache_page(180)
def blog_index(request):
    paginator = Paginator(Article.posts.all().order_by("-dt"), 20)
    return render(request, "article/archive.html", {'articles': page(request, paginator),
                                                    'blurb': "Blog index",
                                                    'title': 'Blog'})

@cache_page(180)
def review_index(request):
    paginator = Paginator(Article.reviews.all().order_by("-dt"), 20)
    return render(request, "article/archive.html", {'articles': page(request, paginator),
                                                    'blurb': "Reviews index",
                                                    'title': 'Reviews'})
@cache_page(180)
def article(request, slug, type):
    if slug.endswith(".html"):
        url = request.path.replace(".html", "")
        return HttpResponsePermanentRedirect(url)
    else:
        article = get_object_or_404(Article, Q(filename=slug) | Q(filename=slug + ".html"), category=type)

        return render(request, "article/article.html", {'article': article,
                                                        'title': article.title,
                                                        'blurb': article.blurb,
                                                        'og_image': article.masthead
                                                      })

@cache_page(180)
def index(request):
    """
    View for the front page /
    """
    streams = [iter(Article.objects.filter(display=True).exclude(feature=True).order_by("-dt")[:50]),
               iter(MailBag.objects.filter(display=True).order_by("-dt")[:50])]
    mixed = sorta(streams, key=lambda obj: obj.dt, order=max, total=50)
    paginator = Paginator(list(mixed), 10)
    return render(request, "index.html", {'objects': page(request, paginator),
                                          'featured': Article.objects.filter(feature=True)[:1],
                                          'og_image': 'static/_theme/img/df-masthead.jpg',
                                          'title': ""
                                        })

@cache_page(180)
def recent(request):
    """
    Recent page - all the things.
    """
    streams = [iter(Article.objects.filter(display=True).exclude(feature=True).order_by("-dt")[:100]),
               iter(MailBag.objects.filter(display=True).order_by("-dt")[:100])]
    mixed = sorta(streams, key=lambda obj: obj.dt, order=max, total=100)
    paginator = Paginator(list(mixed), 30)
    return render(request, "article/archive.html", {'articles': page(request, paginator),
                                                    'title': 'Recent',
                                                    'blurb': 'Recently added content'})

@cache_page(180)
def tags_index(request):
    def title(obj):
        return obj.title
    qs1 = Tags.objects.all().annotate(num=Count('articles')).order_by('title')
    qs2 = Genre.objects.all().annotate(num=Count('articles')).order_by('title')
    return render(request, 'article/tags.html', {'tags': sorted(chain(qs1, qs2), key=title),
                                                 'title': 'Tags Page',
                                                 'blurb': 'Content grouped by tag and genre'})
@cache_page(180)
def tag(request, slug):
    tag = Tags.objects.filter(title=slug).first()
    if not tag:
        tag = Genre.objects.filter(title=slug).first()
    if not tag:
        raise Http404
    return render(request, 'article/tag.html', {'tag': tag, 'articles': tag.articles.all(),
                                                'title': 'Tags :: %s' % tag.title,
                                                'blurb': 'Articles for %s' % tag.title})
