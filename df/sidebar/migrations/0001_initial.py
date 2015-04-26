# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SidebarCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('side', models.CharField(max_length=50, choices=[(b'LEFT', b'Left'), (b'RIGHT', b'Right')])),
            ],
            options={
                'verbose_name_plural': 'Side bar categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('dt', models.DateField(null=True, verbose_name=b'Date', blank=True)),
                ('display', models.BooleanField(default=False)),
                ('blurb', models.TextField(blank=True)),
                ('article', models.ForeignKey(blank=True, to='article.Article', null=True)),
                ('category', models.ForeignKey(to='sidebar.SidebarCategory')),
            ],
            options={
                'verbose_name_plural': 'Side bar entries',
            },
            bases=(models.Model,),
        ),
    ]
