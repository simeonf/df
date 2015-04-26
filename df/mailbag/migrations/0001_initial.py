# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailBag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('dt', models.DateTimeField(verbose_name=b'date')),
                ('display', models.BooleanField(default=False)),
                ('blurb', models.TextField(help_text=b'The blurb can synopsise the individual entries...\n                                       Keep it short - it gets wrapped in a single &lt;p&gt; tag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailBagEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Optional. Leave blank if entry corresponds to particular movie.', max_length=255, blank=True)),
                ('search_blurb', models.TextField(blank=True)),
                ('search', models.BooleanField(default=False, verbose_name=b'enable search')),
                ('quote', models.TextField()),
                ('quote_below_the_fold', models.TextField(blank=True)),
                ('entry', models.TextField(verbose_name=b'response', blank=True)),
                ('below_the_fold', models.TextField(blank=True)),
                ('display', models.BooleanField(default=False)),
                ('mail_bag', models.ForeignKey(to='mailbag.MailBag')),
                ('related_to', models.ForeignKey(blank=True, to='article.Article', help_text=b'Select the article or Review this mailbag entry is related to', null=True)),
            ],
            options={
                'verbose_name_plural': 'Mail bag entries',
            },
            bases=(models.Model,),
        ),
    ]
