from django import template

from sidebar.models import SidebarCategory, SidebarEntry
from article.models import Article

register = template.Library()

def get_articles(cats):
  se = SidebarEntry.objects.filter(category__in=cats).select_related('article')
  articles = set([s.article for s in se])
  return sorted(articles, key=lambda a: a.title)[:10]
  
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
         
