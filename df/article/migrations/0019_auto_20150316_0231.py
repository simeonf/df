# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0018_lead_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='age',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'K', b'Kids & Up'), (b'K*', b'Kids & Up*'), (b'T', b'Teens & Up'), (b'T*', b'Teens & Up*'), (b'A', b'Adults'), (b'A*', b'Adults*'), (b'Z', b'No One')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='below_the_fold',
            field=models.TextField(help_text=b'Used for Blog Posts or link posts...', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='moral',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'4', b'4'), (b'3', b'3'), (b'2', b'2'), (b'1', b'1'), (b'0', b'0'), (b'-1', b'-1'), (b'-2', b'-2'), (b'-3', b'-3'), (b'-4', b'-4')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='spiritual',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'4', b'4'), (b'3', b'3'), (b'2', b'2'), (b'1', b'1'), (b'0', b'0'), (b'-1', b'-1'), (b'-2', b'-2'), (b'-3', b'-3'), (b'-4', b'-4')]),
            preserve_default=True,
        ),
        migrations.AlterModelTable(
            name='genre',
            table='article_genre',
        ),
        migrations.AlterModelTable(
            name='image',
            table='article_image',
        ),
        migrations.AlterModelTable(
            name='link',
            table='article_link',
        ),
    ]
