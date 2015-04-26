import datetime
from itertools import tee, chain
import re
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save, pre_delete

from rebuild_index import rebuild_recent

CATEGORY_CHOICES = (('ARTICLE', "Article"),('REVIEW', "Review"),('POST', "Blog Post"))
STAR_CHOICES = [('40', '4 Stars'),
                ('35', '3.5'),
                ('30', '3.0'),
                ('25', '2.5'),
                ('20','2.0'),
                ('15', '1.5'),
                ('10', '1'),
                ('05','.5'),
                ('00', '0')]
OVERALL_CHOICES = zip(*tee(['A+','A','A-', 'B+','B','B-','C+','C','C-','D+','D','D-','F',]))
MORAL_CHOICES = zip(*tee(map(str, [4,3,2,1,0,-1,-2,-3,-4])))
AGE_CHOICES = [('K', 'Kids & Up'),
               ('K*', 'Kids & Up*'),
               ('T', 'Teens & Up'),
               ('T*', 'Teens & Up*'),
               ('A', 'Adults'),
               ('A*', 'Adults*'),
               ('Z', 'No One')]
MPAA_CHOICES = zip(*tee(['G','PG','PG-13','R','NR']))
USCCB_CHOICES = zip(*tee(['A-I','A-II','A-III','A-IV','O', 'L', 'NR']))

class Link(models.Model):
    class Meta:
        db_table = 'article_link'
    url = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    expires = models.DateTimeField(null=True, blank=True,
                                    help_text="Set an expires date for a 'continue reading' experience.")    
    article = models.ForeignKey("Article")
    
    def __unicode__(self):
        return u"%s" % self.url

class Image(models.Model):
    class Meta:
        db_table = 'article_image'  
    image = models.CharField(max_length=768)
    attributes = models.CharField(max_length=255)
    article = models.ForeignKey("Article")
    
    def __unicode__(self):
        return u"%s" % self.image
    
class Genre(models.Model):
    class Meta:
        db_table = 'article_genre'
    title = models.CharField(max_length=128)
    articles = models.ManyToManyField("Article", related_name='article_set')
    
    @classmethod
    def name_to_id(cls, genre):
        """Given an id or title return the id or look up the title and return the id. Returns None on failure."""
        if not genre:
            return None
        if not genre.isdigit():
            return getattr(cls.objects.filter(title=genre).first(), 'id', None)
        else:
            return genre
    
    def __unicode__(self):
        return u"%s" % self.title

class Tags(models.Model):
    class Meta:
        db_table = 'article_tags'  
    title = models.CharField(max_length=128)
    articles = models.ManyToManyField('Article', related_name="labeled")

    class Meta:
        verbose_name_plural = "tags"

    def related_articles(self):
        return self.articles.all().count()

    def get_absolute_url(self):
        return "/tags/%s" % self.title
      
    def __unicode__(self):
        return u"%s" % self.title

class ArticleQuerySet(models.QuerySet):
    def datetimes(self, *args, **kwargs):
        x = super(ArticleQuerySet, self).dates(*args, **kwargs)
        return filter(None, x)

class AllArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

class ReviewManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db).filter(category="REVIEW", display=True)

class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db).filter(category="ARTICLE", display=True)

class BlogManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db).filter(category="POST", display=True)


class Article(models.Model):
    title = models.CharField(max_length=765)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    see_also = models.CharField(max_length=765, blank=True, null=True)
    amazon = models.TextField(blank=True, null=True)
    notebox = models.TextField(blank=True, null=True)
    iframe = models.CharField(max_length=255, blank=True, null=True)
    byline = models.CharField(max_length=255, blank=True, null=True)
    masthead = models.ImageField(upload_to="articles", null=True, blank=True)
    category = models.CharField(max_length=7, choices=CATEGORY_CHOICES)
    blurb = models.TextField(blank=True,help_text="""For blog posts, the blurb will show up on the
                               search and 'recent' page. No &lt;p&gt; tags...""")
    feature = models.BooleanField(help_text='If this is a Article or Review, fill out the blurb\
                                             and check "Feature" to display on the blog.', default=False)
    lead_content = models.TextField(null=True, blank=True)
    entry = models.TextField()
    
    below_the_fold = models.TextField(help_text="Used for Blog Posts or link posts...", blank=True)
    dt = models.DateTimeField("Date Posted", null=True, blank=True)
    dt_modified = models.DateTimeField("Date Updated",
                                       help_text='Updating the timestamp will put the \
                                                  article back into the RSS feeds.', blank=True)

    tags = models.CharField(max_length=255, blank=True)

    alttitle = models.CharField("Alt. Title", max_length=255, blank=True, help_text="Only used in search")
    cast = models.TextField(blank=True)
    objections = models.TextField(blank=True)
    filename = models.CharField(max_length=300, help_text="Assign your article a human-friendly name. \
                                                Use lowercase letters and hyphens and keep it short.")
    dt_dvd = models.DateField("DVD Release Date", blank=True)
    display = models.BooleanField(help_text='Show or hide entry from list views.', default=False)
    exclude_from_search = models.BooleanField(help_text='Excluded this article from the search page.', default=False)
    product_notes = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, through=Genre.articles.through, blank=True)
    labels = models.ManyToManyField(Tags, through=Tags.articles.through, blank=True)
    
    stars = models.CharField(max_length=2, choices=STAR_CHOICES, blank=True, null=True)
    overall = models.CharField(max_length=2, choices=OVERALL_CHOICES, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    moral = models.CharField(max_length=2, choices=MORAL_CHOICES, blank=True, null=True)
    spiritual = models.CharField(max_length=2, choices=MORAL_CHOICES, blank=True, null=True)
    age = models.CharField(max_length=2, choices=AGE_CHOICES, blank=True, null=True)
    mpaa = models.CharField(max_length=5, choices=MPAA_CHOICES, blank=True, null=True)
    usccb = models.CharField(max_length=5, choices=USCCB_CHOICES, blank=True, null=True)
    
    # Managers
    objects = AllArticleManager()
    reviews = ReviewManager()
    articles = ArticleManager()
    posts = BlogManager()

    class Meta:
        db_table = u'blog'
        ordering = ['-dt', 'filename', 'title']

    @property
    def moral_rating(self):
        """There are two ratings. If one is unset the rating is the other. If both ar set and they differ show both"""
        a, b = self.moral, self.spiritual
        def pos(x):
          if x.isdigit() and int(x) > 0:
            return "+" + x
          else:
            return x
        if a is None:
            return pos(b)
        if b is None:
            return pos(a)
        if a == b:
          return pos(a)
        return "{} / {}".format(*map(pos, sorted([a, b], reverse=True)))
        
    @property
    def related_tags(self):
        if getattr(self, '_related_tags', None):
          return self._related_tags
        tags = Tags.objects.filter(article=self)
        genres = Genre.objects.filter(article=self)
        self._related_tags = sorted(chain(tags, genres), key=lambda x: x.title)
        return self._related_tags

    @property
    def continue_reading(self):
      if getattr(self, '_link', None):
        return self._link
      link = self.source
      if link.expires and datetime.datetime.now() < link.expires:
        self._link = link
        return link

    @property
    def source(self):
      if getattr(self, '_source', None) is None:
        self._source = self.link_set.all().first() or False
      return self._source
        
    @property
    def stars_list(self):
        """Return list of 4 stars: whole, half, or empty. Eg ['whole','half',0,0]."""
        stars = [0, 0, 0, 0]
        try:
            whole, half = self.stars # which should be a two char string like "25"
        except (TypeError, ValueError):
            return stars
        x = -1
        for x in range(int(whole)):
          stars[x] = 'whole'
        if half == '5':
          stars[x+1] = "half"
        if not any(stars):
          stars = []
        return stars

        
    @property
    def age_display(self):
        values = {
            'K': 'Kids &amp; Up',
            'K*': 'Kids &amp; Up*',
            'T': 'Teens &amp; Up',
            'T*': 'Teens &amp; Up*',
            'A': 'Adults',
            'A*': 'Adults*',
            'Z': 'No One',
          }
        return values.get(self.age, '')

    def get_absolute_url(self):
        category = str(self.category).lower()
        if category == "post":
            category = "blog"
        else:
            category += "s"
        return "/%s/%s" % (category, self.filename.replace(".html", ""))


    def __unicode__(self):
        result = self.title
        if self.year:
            result = "%s (%s)" % (self.title, self.year)
        result = result + " (" + self.category + ")"
        result = re.sub("\&[^; ]+;", "", result)
        result = re.sub("<[^> ]+>", "", result)
        return result

    def date(self):
        if self.dt:
            return self.dt
        else:
            return '0000-00-00'
    date.admin_order_field = 'dt'

    def save(self, force_insert=False, force_update=False):
        # Go ahead and add a genre record if necessary
        if not self.dt_modified:
            self.dt_modified = self.dt
        super(Article, self).save(force_insert, force_update)
        rebuild_recent()

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" %
                       (self._meta.app_label, self._meta.module_name), args=(self.id,))
