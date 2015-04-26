# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_image_link'),
    ]

    operations = [
      migrations.RunSQL('alter table blog change labels labels_old varchar(255)')
    ]
