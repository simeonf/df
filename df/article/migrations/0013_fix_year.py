# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from article.models import Genre, Article

            
def extract_tags(apps, schema_editor):
    for article in Article.objects.all():
        tags = article.tags.split()

        used = []
        for tag in tags:
            if tag.startswith('year'):
                article.year = tag[-4:]
        left_over = set(tags) - set(used)
        #article.tags = " ".join(left_over)
        article.save()

class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_auto_20150204_0212'),
    ]

    operations = [ migrations.RunPython(extract_tags),
    ]
