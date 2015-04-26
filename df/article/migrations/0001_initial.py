# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=765)),
                ('category', models.CharField(max_length=7, choices=[(b'ARTICLE', b'Article'), (b'REVIEW', b'Review'), (b'POST', b'Blog Post')])),
                ('blurb', models.TextField(help_text=b"For blog posts, the blurb will show up on the\n                               search and 'recent' page. No &lt;p&gt; tags...", blank=True)),
                ('feature', models.BooleanField(default=False, help_text=b'If this is a Article or Review, fill out the blurb                                             and check "Feature" to display on the blog.')),
                ('entry', models.TextField()),
                ('below_the_fold', models.TextField(help_text=b'Used for Blog Posts only...', blank=True)),
                ('dt', models.DateTimeField(null=True, verbose_name=b'Date Posted', blank=True)),
                ('dt_modified', models.DateTimeField(help_text=b'Updating the timestamp will put the                                                   article back into the RSS feeds.', verbose_name=b'Date Updated', blank=True)),
                ('tags', models.CharField(max_length=255, blank=True)),
                ('alttitle', models.CharField(max_length=255, verbose_name=b'Alt. Title', blank=True)),
                ('cast', models.TextField(blank=True)),
                ('objections', models.TextField(blank=True)),
                ('filename', models.CharField(help_text=b'Assign your article a human-friendly name.                                                 Use lowercase letters and hyphens and keep it short.', max_length=300)),
                ('dt_dvd', models.DateField(verbose_name=b'DVD Release Date', blank=True)),
                ('display', models.BooleanField(default=False, help_text=b'Show or hide entry from list views.')),
                ('exclude_from_search', models.BooleanField(default=False, help_text=b'Excluded this article from the search page.')),
                ('product_notes', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['-dt', 'filename', 'title'],
                'db_table': 'blog',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('articles', models.ManyToManyField(related_name='article_set', to='article.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('articles', models.ManyToManyField(related_name='labeled', to='article.Article')),
            ],
            options={
                'verbose_name_plural': 'tags',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='genre',
            field=models.ManyToManyField(to='article.Genre', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='labels',
            field=models.ManyToManyField(to='article.Tags', blank=True),
            preserve_default=True,
        ),
    ]
