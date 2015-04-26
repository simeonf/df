# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_article_masthead'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='age',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'K', b'Kids &amp; Up'), (b'K*', b'Kids &amp; Up*'), (b'T', b'Teens &amp; Up'), (b'T*', b'Teens &amp; Up*'), (b'A', b'Adults'), (b'A*', b'Adults*'), (b'Z', b'No One')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='moral',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(4, 4), (3, 3), (2, 2), (1, 1), (0, 0), (-1, -1), (-2, -2), (-3, -3), (-4, -4)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='mpaa',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'G', b'G'), (b'PG', b'PG'), (b'PG-13', b'PG-13'), (b'R', b'R'), (b'NR', b'NR')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='overall',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'A+', b'A+'), (b'A', b'A'), (b'A-', b'A-'), (b'B+', b'B+'), (b'B', b'B'), (b'B-', b'B-'), (b'C+', b'C+'), (b'C', b'C'), (b'C-', b'C-'), (b'D+', b'D+'), (b'D', b'D'), (b'D-', b'D-'), (b'F', b'F')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='spiritual',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(4, 4), (3, 3), (2, 2), (1, 1), (0, 0), (-1, -1), (-2, -2), (-3, -3), (-4, -4)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='stars',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'40', b'4 Stars'), (b'35', b'3.5'), (b'30', b'3.0'), (b'25', b'2.5'), (b'20', b'2.0'), (b'15', b'1.5'), (b'10', b'1'), (b'05', b'.5'), (b'00', b'0')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='usccb',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'A-I', b'A-I'), (b'A-II', b'A-II'), (b'A-III', b'A-III'), (b'O', b'O'), (b'NR', b'NR')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='year',
            field=models.CharField(max_length=4, null=True, blank=True),
            preserve_default=True,
        ),
    ]
