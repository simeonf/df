# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import difflib
import json

from django.apps import apps


class QueryReplace(object):
    def __init__(self, model, field, search, replace, seen=None):
        self.model = apps.get_model(model)
        self.model_description = model
        self.field = field
        self.search_term = search
        self.replace = replace
        self.seen = seen or []

        self.instance = None
        self.diff = None

    @property
    def skipped(self):
        return len(self.seen)

    @property
    def total(self):
        return self.search().count()

    def queryset(self):
        seen = self.seen
        if self.instance:
            seen = self.seen + [self.instance.pk]
        return self.model.objects.filter(pk__in=seen)

    def search(self):
        search_key = "%s__contains" % self.field
        kwargs = {search_key: self.search_term}
        qs = self.model.objects.filter(**kwargs)
        return qs


    def json(self):
        return json.dumps({'raw': '\n'.join(self.diff)})


    def do_replace(self, pk):
        instance = self.model.objects.get(pk=pk)
        text1 = getattr(instance, self.field)
        text2 = text1.replace(self.search_term, self.replace)
        setattr(instance, self.field, text2)
        instance.save()


    def next(self):
        """Returns a unified diff of the next match of the search term or None"""
        qs = self.search()
        self.instance = qs.exclude(pk__in=self.seen).first()

        if not self.instance:
          return None
        text1 = getattr(self.instance, self.field)
        text2 = text1.replace(self.search_term, self.replace)
        fname = "%s.%s" % (self.model_description, self.field)
        diff = difflib.unified_diff(text1.split("\n"),
                                         text2.split("\n"),
                                         fromfile=fname,
                                         tofile=fname,
                                         lineterm="")
        self.diff = list(diff)
        return self.diff
