from django.http import HttpResponseRedirect, Http404

from article.models import Article


def old_urls_redirect(request, category, slug):
  if slug.isdigit():
    try:
      article = Article.objects.get(id=slug)
      return HttpResponseRedirect(article.get_absolute_url())
    except Article.DoesNotExist:
      pass
  return HttpResponseRedirect("/%s/%s" % (category, slug))
