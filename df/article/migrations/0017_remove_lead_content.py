# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from lxml import etree
from lxml import html
from lxml.cssselect import CSSSelector


from django.db import models, migrations

from article.models import Article

def _(node):
    return etree.tostring(node, method="html")

def remove_lead(*args):
    sel = CSSSelector("content-lead")
    for article in Article.objects.all():
        body = html.fromstring(article.entry)
        lead = list(sel(body))
        if len(lead) == 1:
            lead[0].drop_tree()
            article.entry = _(body)
            article.save()
        elif len(lead) > 1:
            print article.id, article.title, len(lead)


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0016_extract_lead_content'),
    ]

    operations = [
      migrations.RunPython(remove_lead)
    ]
