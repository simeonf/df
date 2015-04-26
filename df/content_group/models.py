from django.db import models

from mailbag.models import MailBagEntry
from article.models import Article

class ContentGroup(models.Model):
    title = models.CharField(max_length=255)
    mailbag_entries = models.ManyToManyField(MailBagEntry, blank=True, null=True)
    articles = models.ManyToManyField(Article, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.title)

    @classmethod
    def get_all_related_to_article(cls, article):
        # Get a content group that contains the article
        cg = cls.objects.filter(articles__id=article.id).first()
        # But also - there may be a mailbag specifically about the article
        mb = MailBagEntry.objects.filter(related_to_id=article.id)
        related = {'article': [], 'mail':list(mb)}
        if cg:
            related['articles'] = list(cg.articles.all().exclude(id=article.id))
            related['mail'] += list(cg.mailbag_entries.all())
        return related

      
