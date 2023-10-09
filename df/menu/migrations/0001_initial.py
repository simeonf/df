# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-10-09 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=150)),
                ('display', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Menu Items',
            },
        ),
    ]
