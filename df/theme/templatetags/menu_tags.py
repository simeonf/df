from itertools import tee
import datetime
from django import template


from menu.models import MenuItem

register = template.Library()


@register.simple_tag
def here(path, item):
    if item == '/':
        if item == path:
            return "home here"
        else:
          return "home"
    elif path.startswith(item):
        return "here"
    else:
      return ""


@register.inclusion_tag('menu.html')
def display_menu():
    items = MenuItem.objects.filter(display=True)
    return dict(items=items)
