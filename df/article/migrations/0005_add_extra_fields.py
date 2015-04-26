# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_data_tagfields'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='amazon',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='byline',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='iframe',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='notebox',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='see_also',
            field=models.CharField(max_length=765, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='subtitle',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='usccb',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'A-I', b'A-I'), (b'A-II', b'A-II'), (b'A-III', b'A-III'), (b'A-IV', b'A-IV'), (b'O', b'O'), (b'L', b'L'), (b'NR', b'NR')]),
            preserve_default=True,
        ),
    ]
