import re

from django import template

from content_group.models import ContentGroup

register = template.Library()

@register.assignment_tag
def get_article_related(article):
    return ContentGroup.get_all_related_to_article(article)

@register.filter    
def toint(val):
  return int(val)

@register.filter
def int_value(val):
    try:
        score = int(val)
    except (ValueError, TypeError) as e:
        return 0
    if score > 0:
        return "+%s" % score
    else:
        return str(val)
        

link = re.compile("<(/)?a[^>]*>")

@register.filter
def strip_anchor(txt):
    return link.sub("", txt)

        
        
