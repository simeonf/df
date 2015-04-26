# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0011_initial_para'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='source',
        ),
        migrations.AddField(
            model_name='link',
            name='expires',
            field=models.DateTimeField(help_text=b"Set an expires date for a 'continue reading' experience.", null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='alttitle',
            field=models.CharField(help_text=b'Only used in search', max_length=255, verbose_name=b'Alt. Title', blank=True),
            preserve_default=True,
        ),
    ]
