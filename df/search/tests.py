from unittest import TestCase
import doctest
#from django.test import TestCase

import search

from .forms import stars, add_plus
from .search import Ratings

import utility

class FormTests(TestCase):

  def test_stars(self):
    """The star functions maps a numeric rating to a textual description."""
    self.assertEqual(stars(10), "*")
    self.assertEqual(stars(5), "1/2")
    self.assertEqual(stars(45), "****1/2")
    self.assertEqual(stars(0), "No stars")

  def test_moral(self):
    """moral ratings go from -4 to +4"""
    self.assertEqual(add_plus(-1), "-1")
    self.assertEqual(add_plus(1), "+1")
    self.assertEqual(add_plus(0), "0")


class SearchTest(TestCase):
  def test_overall(self):
    """The overall rating is eg A+"""
    self.assertEqual("(overall='A+' or overall='A')", Ratings.sql(["overall"], "A", ">="))
    self.assertEqual("(overall='A')", Ratings.sql(["overall"], "A", "="))
    self.assertEqual("(overall='D' or overall='D-' or overall='F')", Ratings.sql(["overall"], "D", "<="))



class SortableStringTest(TestCase):
  """Strings that start with a quotes, an article, <em>, &lquo;, etc get normalized for searching/sorting purposes"""

  def test_make_sortable_article(self):
    self.assertEqual("full title", utility.make_sortable("The Full Title"))

  def test_make_sortable_quote(self):
    self.assertEqual('quote" to start', utility.make_sortable('"A quote" to start'))

  def test_make_sortable_entity(self):
    self.assertEqual("full title", utility.make_sortable("&lquo;The Full Title&rquo;"))

class DocTestTests(TestCase):
  doctest.testmod(search)
