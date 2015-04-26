# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0013_fix_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.CharField(max_length=768),
            preserve_default=True,
        ),
    ]
