# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='masthead',
            field=models.ImageField(null=True, upload_to=b'articles', blank=True),
            preserve_default=True,
        ),
    ]
