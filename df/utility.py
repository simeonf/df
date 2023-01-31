import re
from collections import namedtuple
from django.core.paginator import EmptyPage, PageNotAnInteger

ENTITY_PAT = re.compile("&[^;]+;")
TAG_PAT = re.compile("<[^>]+>")
STRIP_LIST = ["a ", "an ", "the "] # "<em>", "<i>"


def make_sortable(orig):
    orig = orig.lower()
    # deal with leading html entities
    if orig[0] == "&":
        orig = ENTITY_PAT.sub("", orig)
    # deal with leading simple tags
    if orig[0] == "<":
        orig = TAG_PAT.sub("", orig)
    # Deal with unicode quotes, ', ", etc
    if not orig[0].isalnum():
        orig = orig[1:]
    for item in STRIP_LIST:
        if orig.startswith(item):
            orig = orig[len(item):]
            break
    return orig



def page(request, paginator):
    page = request.GET.get('page')
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    return records

def get(stream):
  try:
      val = next(stream)
      return val
  except StopIteration:
      return None

Cell = namedtuple("Cell", "index, value")

def sorta(streams, key=None, total=None, order=min):
  # if we only got one
  if len(streams) == 1:
      for val in streams[0]:
          yield val
      return
  # compose the values
  values = [get(stream) for stream in streams]
  num = 0
  def keyfunc(cell):
      if key:
          return key(cell.value)
      else:
          return cell.value
  while True:
      # if all streams are exhausted - we're done!
      if set(values) == {None}:
          return
      # reload values
      for index, val in enumerate(values):
          if val is None:
              values[index] = get(streams[index])
      # pick the minimal cell
      cell = order([Cell(i, v) for (i, v) in enumerate(values) if v is not None], key=keyfunc)
      yield cell.value
      values[cell.index] = None
      num += 1
      # Don't go too far
      if total is not None and num >= total:
          return
