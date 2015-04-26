from itertools import tee
import datetime
from django import template

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
    
