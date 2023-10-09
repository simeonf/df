# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from menu.models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'display', 'order')
    search_fields = ('title',)
    list_filter = ('display',)


admin.site.register(MenuItem, MenuItemAdmin)
