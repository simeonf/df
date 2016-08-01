from django.test import TestCase
from article.factories import ArticleFactory
from .models import SidebarEntry, SidebarCategory
from .templatetags.sidebar_tags import get_articles

class SidebarOrdering(TestCase):
    """Sidebar entries have different titles than articles they represent and should be so sorted."""

    def setUp(self):
        self.article_titles = ["The Hobbit", "Hurtful intent"]
        self.sidebar_titles = ["Hobbit, The", "Hurtful intent"]
        self.sc = SidebarCategory.objects.create(id=5, title='DVD - Latest')
        self.articles = [ArticleFactory.create(title=title) for title in self.article_titles]
        for title, article in zip(self.sidebar_titles, self.articles):
          SidebarEntry.objects.create(category=self.sc, title=title, display=True, article=article)

    def test_dvd_classmethod_sorted_by_title(self):
        """Sidebar entries are ordered by own title."""
        entries = SidebarEntry.dvd()
        entries = list(entries['latest'])
        for i, title in enumerate(self.sidebar_titles):
          self.assertEqual(entries[i].title, title)


    def test_dvd_templatetag_sorted_by_title(self):
        """Sidebar entries are ordered by own title."""
        entries = get_articles([self.sc])
        for i, title in enumerate(self.article_titles):
          self.assertEqual(entries[i].title, title)

        
