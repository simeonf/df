# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from lxml import etree
from lxml import html
from lxml.cssselect import CSSSelector

from django.db import models, migrations
from django.db.models import Q

from article.models import Article

def _(node):
    return etree.tostring(node, method="html")

def missing_lead(*args):
    para = CSSSelector("p")
    for article in Article.objects.filter(Q(lead_content=None)|Q(lead_content='')):
        body = html.fromstring(article.entry)
        lead = list(para(body))
        if lead:
            p = lead[0]
            if 'class' in p.attrib:
                p.attrib.pop('class')
            article.lead_content = _(p)
            p.drop_tree()
            if p is body: # Only 1 para in body, drop didn't work
              article.entry = ''
            else:
              article.entry = _(body)
            article.save()

class Migration(migrations.Migration):

    dependencies = [
        ('article', '0017_remove_lead_content'),
    ]

    operations = [
      migrations.RunPython(missing_lead)
    ]
