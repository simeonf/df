from django.contrib import admin
from article.models import Article, Tags, Genre, Link, Image
from django.db import models
from django import forms

class ArticleForm(forms.ModelForm):
    tags = forms.CharField(max_length=255,
                            widget=forms.TextInput(attrs={'size':'140'}),
                            required=False)
    entry = forms.CharField(widget=forms.Textarea(attrs={'rows':'25','cols':'110'}))

    class Meta:
        model = Article
        exclude = []


class LinkAdmin(admin.TabularInline):
    model = Link

class ImageAdmin(admin.TabularInline):
    model = Image

class GenreAdmin(admin.ModelAdmin):
    filter_horizontal = ('articles',)
    model = Genre

class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'dt'
    list_display = ('title','cast','category', 'date')
    search_fields = ('title','alttitle')
    list_filter = ('category','feature','display','exclude_from_search')
    form = ArticleForm
    filter_horizontal = ('genre','labels')
    inlines = [LinkAdmin, ImageAdmin]
    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'subtitle', 'alttitle', 'filename', 'blurb', 'lead_content',
                       'entry', 'below_the_fold', 'display', 'see_also', 'amazon', 'notebox',
                       'iframe', 'byline', 'masthead', 'exclude_from_search', 'genre', 'labels',)
        }),
        ('Featured', {
            'classes': ('collapse',),
            'fields': ('feature',)
        }),
        ('Date', {
            'classes': ('collapse',),
            'fields': ('dt', 'dt_modified', 'dt_dvd')
        }),
        ('Review Details', {
            'classes': ('collapse',),
            'fields': ('tags', 'cast', 'objections', 'product_notes', 'stars',
                       'overall', 'year', 'moral', 'spiritual', 'age', 'mpaa', 'usccb')

        }),
    )


class TagAdmin(admin.ModelAdmin):
    filter_horizontal = ('articles',)
    list_display = ('title', 'related_articles')

admin.site.register(Tags, TagAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Article, ArticleAdmin)
