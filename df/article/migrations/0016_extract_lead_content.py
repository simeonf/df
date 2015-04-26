# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from lxml import etree
from lxml import html
from lxml.cssselect import CSSSelector


from django.db import models, migrations

from article.models import Article

def _(node):
    return etree.tostring(node, method="html")

def parse_lead(*args):
    sel = CSSSelector("content-lead")
    for article in Article.objects.all():
        body = html.fromstring(article.entry)
        lead = list(sel(body))
        if len(lead) == 1:
            els = lead[0].getchildren()
            # pop off class="initial" while we're at it
            for el in els:
                if 'class' in el.attrib:
                    el.attrib.pop('class')
            article.lead_content = "\n".join([_(el) for el in els])
            article.save()
        elif len(lead) > 1:
            print article.id, article.title, len(lead)


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0015_auto_20150215_1655'),
    ]

    operations = [
      migrations.RunPython(parse_lead)
    ]

