from django.contrib import admin
from article.models import Article, Tags, Genre, Link, Image
from django.contrib.admin.widgets import FilteredSelectMultiple
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

article_widget = FilteredSelectMultiple("Article", False, attrs={'rows':'2'})

class ArticleM2MForm(forms.ModelForm):
    article = forms.ModelMultipleChoiceField(Article.objects.all(),
                                             required=False,
                                             widget=article_widget)
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.get('initial', {})
            initial['article'] = instance.articles.all()
            kwargs['initial'] = initial
        super(ArticleM2MForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        value = super(ArticleM2MForm, self).save(*args, **kwargs)
        if kwargs.get('commit') is not False:
            a, b = set(self.instance.articles.all()), set(self.cleaned_data['article'])
            new = b - a
            for article in new:
                self.instance.articles.add(article)
            removed = a - b
            for article in removed:
                self.instance.articles.remove(article)
        return value


class GenreAdmin(admin.ModelAdmin):
    model = Genre
    form = ArticleM2MForm

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
    model = Tags
    form = ArticleM2MForm

admin.site.register(Tags, TagAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Article, ArticleAdmin)
