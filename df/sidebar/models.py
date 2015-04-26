from django.db import models

from article.models import Article

SIDEBAR_CHOICES = (
    ('LEFT', 'Left'),
    ('RIGHT', 'Right'),
)


class SidebarCategory(models.Model):
    title = models.CharField(max_length=50)
    side = models.CharField(max_length=50, choices=SIDEBAR_CHOICES)
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Side bar categories'
    
    
class SidebarEntry(models.Model):
    category = models.ForeignKey(SidebarCategory)
    title = models.CharField(max_length=255)
    dt = models.DateField("Date", blank=True, null=True)
    article = models.ForeignKey(Article, blank=True, null=True)
    display = models.BooleanField(default=False)
    blurb = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Side bar entries'


    @classmethod
    def dvd(cls):
        latest = cls.objects.filter(category_id=5, display=True).select_related('article').order_by('title')
        recent = cls.objects.filter(category_id=6, display=True).select_related('article').order_by('title')
        return dict(latest=latest, recent=recent, title='Home Video', blurb='')


    @classmethod
    def theater(cls):
        all = cls.objects.filter(category_id=7, display=True).select_related('article').order_by('title')
        latest = cls.objects.filter(category_id=2, display=True).select_related('article').order_by('title')
        return dict(latest=latest, all=all, title='Now Playing', blurb='Currently In theaters.')
