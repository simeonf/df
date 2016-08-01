from django import template

from sidebar.models import SidebarCategory, SidebarEntry
from article.models import Article

register = template.Library()

def get_articles(cats):
  """Return unique articles for set of sidebar entries in sidebar.title order."""
  se = SidebarEntry.objects.filter(category__in=cats).select_related('article').order_by('title')
  sidebar_order = {entry.article.id: i for (i, entry) in enumerate(se)}
  articles = list(set([s.article for s in se]))
  articles = sorted(articles, key=lambda a: sidebar_order[a.id])
  return articles[:10]
  
@register.inclusion_tag('sidebar.html')
def sidebar():

  cats = SidebarCategory.objects.filter(title__startswith='In Theatres')
  now_playing = get_articles(cats)
  dvd_cats = SidebarCategory.objects.filter(title__startswith='DVD - Latest')
  dvd = get_articles(dvd_cats)
  return {'recent': Article.objects.filter(display=True).order_by('-dt')[:5],
          'theatres': now_playing,
          'dvd': dvd,
          }
         
