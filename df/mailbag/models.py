import datetime

from django.db import models
from django.core.urlresolvers import reverse

from article.models import Article


class MailBag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    dt = models.DateTimeField("date", default=datetime.datetime.now)
    display = models.BooleanField(default=False)
    blurb = models.TextField(help_text="""The blurb can synopsise the individual entries...
                                       Keep it short - it gets wrapped in a single &lt;p&gt; tag""")
    @staticmethod
    def masthead():
      """Here for compatibility in template with articles."""
      return False

    @staticmethod
    def category():
      """Here for compatibility in template with articles."""
      return "Mailbag"

    def get_absolute_url(self):
        return "/mail/%s" % self.slug


    def get_admin_url(self):
        return reverse("admin:%s_%s_change" %
                       (self._meta.app_label, self._meta.module_name), args=(self.id,))

    def __unicode__(self):
        if(self.title):
            return unicode(self.title)
        return ''

class MailBagEntry(models.Model):
    title = models.CharField(max_length=255, blank=True,
                             help_text="Optional. Leave blank if entry corresponds to particular movie.")
    related_to = models.ForeignKey(Article, blank=True, null=True,
                                   help_text="Select the article or Review this mailbag entry is related to")
    mail_bag = models.ForeignKey(MailBag)
    search_blurb = models.TextField(blank=True)
    search = models.BooleanField("enable search", default=False)
    quote = models.TextField()
    quote_below_the_fold = models.TextField(blank=True)
    entry = models.TextField("response", blank=True)
    below_the_fold = models.TextField(blank=True)
    display = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Mail bag entries'

    def get_absolute_url(self):
        url = "/mail/%s" % self.mail_bag.slug
        return "%s#entry-%s" % (url, self.id)

    def __unicode__(self):
        if self.title:
            return unicode(self.mail_bag.title + " :: " + self.title)
        elif self.related_to:
            return unicode(self.mail_bag.title + " :: " + self.related_to.title)
        else:
            return self.mail_bag.title
