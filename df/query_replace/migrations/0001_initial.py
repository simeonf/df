# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-02 23:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(help_text='Specify an app.Model string.', max_length=255)),
                ('field', models.CharField(max_length=255)),
            ],
        ),
    ]
