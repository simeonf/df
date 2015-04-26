# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.db import models, migrations

BASE_DIR = os.path.dirname(__file__)


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_add_extra_fields'),
    ]

    operations = [
        migrations.RunSQL(open(BASE_DIR + "/innodb.sql").read()),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'articles')),
                ('attributes', models.CharField(max_length=255)),
                ('article', models.ForeignKey(to='article.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=255)),
                ('text', models.CharField(max_length=255)),
                ('article', models.ForeignKey(to='article.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
