# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class MenuItem(models.Model):
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=150)
    display = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Menu Items'
        ordering = ['order']
