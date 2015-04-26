# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0014_auto_20150210_0428'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='lead_content',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
