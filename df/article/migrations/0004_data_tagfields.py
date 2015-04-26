# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from article.models import Genre, Article

            
def extract_tags(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    #Article = apps.get_model("article", "Article")
    #Genre = apps.get_model("article", "Genre")
    for article in Article.objects.all():
        tags = article.tags.split()
        prefixes = ['overall', 'moral', 'spiritual', 'age', 'stars', 'mpaa', 'usccb']
        used = []
        for tag in tags:
            # fix some stray usccb tags
            if tag in ['usccbNA', 'usccbNot']:
                tag = 'usccbNR'
            if tag.startswith('usccbAdult'):
                tag = 'usccbA-III'
            for prefix in prefixes:
                if tag.lower().startswith(prefix):
                    used.append(tag)
                    try:
                        setattr(article, prefix, tag[len(prefix):])
                    except:
                        import pdb;pdb.set_trace()
                    break
            # Handle year separately due to yearus/yearalt tags
            if tag.startswith('year'):
                article.year = tag[:4]
            # Verify genre record exists
            if tag.startswith('genre'):
                used.append(tag)
                title = tag[len('genre'):].replace("_", " ")
                if not article.genre.filter(title=title):
                    genre, created = Genre.objects.get_or_create(title=title)
                    article.genre.add(genre)
        left_over = set(tags) - set(used)
        article.tags = " ".join(left_over)
        article.save()

class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_add_tagfields'),
    ]

    operations = [ migrations.RunPython(extract_tags),
    ]
