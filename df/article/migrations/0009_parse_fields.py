# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from article.models import Article, Link, Image

from itertools import takewhile
from lxml import etree
from lxml import html
from lxml.cssselect import CSSSelector

def _(node):
  return etree.tostring(node, method="html")

def get_imgs(tree):
  imgs = [t for t in tree.getchildren()[:5] if t.tag == 'img']
  for img in imgs:
    img.drop_tree()
  return imgs

def get_byline(tree):
  h4 = [t for t in tree.getchildren() if t.tag == 'h4']
  h4 = [t for t in h4 if "by" in innerHTML(t).lower()]
  if h4:
    h4 = h4[0]
    text = innerHTML(h4)
    if text.lower() == "by steven d. greydanus":
      ret = None
    else:
      ret = text
    h4.drop_tree()
    return ret
      
iframe = CSSSelector("iframe")

def get_iframe(tree):
  frames = list(iframe(tree))
  if len(frames) > 1:
    print "Multiple iframes, ignoring"
    return ''
  if len(frames) == 1:
    html = _(frames[0])
    frames[0].drop_tree()
    return html
  return None
  
about = CSSSelector("p.about")
def external_link(a):
  href = a.attrib.get('href', '')
  if href.startswith("http") and not href.startswith("http://decentfilms.com"):
    return True
  else:
    return False
    
def get_about(tree):
  first_few = tree.getchildren()[:8]
  record = dict(note="", links=[])
  abouts = list(about(tree))
  num_abouts = len(abouts)
  for elem in abouts:
    if elem not in first_few:
      continue
    #print etree.tostring(elem, method="html")
    a = elem.find('a')      
    if a is not None and external_link(a):
      href = a.attrib.get('href','')
      record['links'].append((href, innerHTML(a)))
    else:
      record['note'] += etree.tostring(elem, method="html")
    elem.drop_tree()
    
  return record
      
  
def innerHTML(node):
    s = node.text
    if s is None:
        s = ''
    for child in node:
        s += etree.tostring(child, method="html", encoding='ascii')
    return s

def removeall(lst):
  for elem in lst:
    elem.drop_tree()
    
def text_h4(tree, text):
  h4 = CSSSelector("h4")
  for elem in h4(tree):
    inner = elem.text or ""
    if text in inner.lower().strip():
      return elem

def see_also_p(h4): 
  for next in h4.itersiblings():
    if next.tag == 'p':
      yield p
    else:
      break
  
def get_h4(tree, text):
  output = ''
  h4 = text_h4(tree, text) # there can be only 1
  if h4 is None:
    return ''
  paras = takewhile(lambda e: e.tag == 'p', h4.itersiblings())
  for p in paras:
    if 'class' in p.attrib:
      p.attrib.pop('class')
    output += etree.tostring(p, method="html")
    p.drop_tree()
  h4.drop_tree()
  h4 = text_h4(tree, text) # and if there's another one
  if h4 is not None:
    paras = takewhile(lambda e: e.tag == 'p', h4.itersiblings())
    removeall(list(paras) + [h4])
  return output

assoc = CSSSelector("div.assoc")
p_notebox = CSSSelector("p.notebox")
p_about = CSSSelector("p.about")

class NewArticle(object):
  def __init__(self, **kwargs):
    self.title = ''
    self.amazon = ''
    self.subtitle = ''
    self.see_also = ''
    self.notebox = ''
    self.external_urls = []
    self.img = []
    for k,v in kwargs.items():
      if v is not None:
        setattr(self, k, v)
    self.entry = self.entry.replace("\n", " ")
    
  def __str__(self):
    return str(self.__dict__)

def process_entry(entry, article):
  body = html.fromstring(entry)
  # If it's a truncated post just write it out.
  if not body.getchildren():
    return article
  # articles may have h1 that needs to be extracted and moved to title
  t = body.getchildren()[0]
  if t.tag == 'h1':
    article.title = innerHTML(t)
    t.drop_tree()
  # h2 that is first needs to move to new field "subtitle"
  t = body.getchildren()[0]
  if t.tag == 'h2':
    article.subtitle = innerHTML(t)
    t.drop_tree()
  # 4. Remove "See also" content
  article.see_also = get_h4(body, "see also")
  # same deal for amazon
  article.amazon = get_h4(body, "amazon.com")
  if len(article.amazon) > 500:
    print article.amazon
  # now remove empty div.assoc
  for div in assoc(body):
    if not div.getchildren():
      div.drop_tree()
  #  orphan "info" paragraphs that are NOT in a div classed "assoc," should be bundled with "about" elements
  # 5. Notebox. a "p.notebox" => article.notes
  for p in p_notebox(body):
    article.notebox += etree.tostring(p, method="html")
    p.drop_tree()

  # 6. About. no external hyperlink append to notebox. External link => external (url, text)
  rec = get_about(body)
  if rec['note']:
    article.notebox += rec['note']
  article.external_urls = rec['links']

  # 8. Iframe -> ifram
  article.iframe = get_iframe(body)

  # 9. Credit line. h4 contents if not "By Steven D. Greydanus"
  article.byline = get_byline(body)


  # 10. Pre-text image. image URL and attributes?
  for img in get_imgs(body):
    article.img.append((img.attrib.pop('src'), img.attrib))

  # 11. Lead paragraph, or initial blockquote - if it doesn't have class, add initial
  lead = [elem for elem in body.getchildren() if elem.tag in ['p', 'blockquote']]
  if lead:
    lead = lead[0]
    if not lead.attrib.get('class'):
      lead.attrib['class'] = 'initial'
  article.entry = innerHTML(body).strip()
  return article


def parse_new_fields(apps, schema_editor):
  Article = apps.get_model("article", "Article")
  Link = apps.get_model("article", "Link")
  Image = apps.get_model("article", "Image")  

  for article in Article.objects.all():
    a = NewArticle(**article.__dict__)
    process_entry(a.entry, a)
    for field in ['title', 'amazon', 'subtitle', 'see_also', 'notebox', 'entry']:
      setattr(article, field, getattr(a, field))

    for (url, text) in a.external_urls:
      article.link_set.add(Link(url=url, text=text))

    for (src, attribs) in a.img:
      attribs = " ".join(["{}='{}'".format(*items) for items in attribs.items()])
      article.image_set.add(Image(image=src, attributes=attribs))
    try:
      article.save()
    except Exception as e:
      import pdb;pdb.set_trace()
      print e
            

class Migration(migrations.Migration):

  dependencies = [
        ('article', '0008_amazon_text'),
    ]

  operations = [
      migrations.RunPython(parse_new_fields)
    ]
