# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_rm_old_label_column'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='amazon',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
