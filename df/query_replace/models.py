# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class SearchDetail(models.Model):
    model = models.CharField(max_length=255, help_text="Specify an app.Model string.")
    field = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s.%s" % (self.model, self.field)
