# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_parse_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='source',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
