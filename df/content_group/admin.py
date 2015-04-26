from django.contrib import admin
from content_group.models import ContentGroup
from django.db import models
from django import forms


class ContentGroupAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title','mailbag_entries__title','articles__title')
    filter_horizontal = ('mailbag_entries','articles')
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('Mailbag Entries', {
            'classes': ('',),
            'fields': ('mailbag_entries',)
        }),
        ('Articles', {
            'classes': ('',),
            'fields': ('articles',)
        }),
    )


admin.site.register(ContentGroup, ContentGroupAdmin)
