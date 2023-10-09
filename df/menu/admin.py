# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.cache import cache
from django.contrib import admin
from menu.models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'display', 'order')
    search_fields = ('title',)
    list_filter = ('display',)

    def save_model(self, request, obj, form, change):
        cache.clear()
        super(MenuItemAdmin, self).save_model(request, obj, form, change)


admin.site.register(MenuItem, MenuItemAdmin)
