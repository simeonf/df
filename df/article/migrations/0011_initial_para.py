# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from lxml import etree
from lxml import html
from lxml.cssselect import CSSSelector

from django.db import models, migrations
from article.models import Article


def _(node):
    return etree.tostring(node, method="html")

def add_content_lead(apps, schema_editor):
    init = CSSSelector("p.initial")
    reviews = Article.objects.all()
    for review in reviews:
      body = html.fromstring(review.entry)
      ps = init(body)
      if ps:
        cl = etree.Element("content-lead")
        first = ps[0]
        first.addprevious(cl)
        for i, el in enumerate(ps):
          cl.insert(i, el)
        review.entry = _(body)
        review.save()


class Migration(migrations.Migration):
    dependencies = [
        ('article', '0010_linksource'),
    ]
    operations = [
      migrations.RunPython(add_content_lead)      
    ]
