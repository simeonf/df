# -*- coding: utf-8 -*-
import json
import re


from django.apps import apps
from django.contrib import admin
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from .models import SearchDetail
from .forms import QuerySearchForm, ChooseFieldForm
from .query_replace import QueryReplace

from admin_views.admin import AdminViews

class QueryReplaceAdmin(AdminViews):
    admin_views = [('Search and Replace', 'replace')]

    @staticmethod
    def do_search(model, field, data, seen):
        search, replace = data['search'], data['replace']
        qr = QueryReplace(model, field, search, replace, seen)
        qr.next()
        return qr

    def replace(self, request):
      # Choose an app.model.field
      form1 = ChooseFieldForm(request.GET)
      if not form1.is_valid():
        return render(request, "query_replace/choose.html", {'form': form1})
      # Get the chosen SearchDetail
      sd = form1.cleaned_data['sd']
      form = QuerySearchForm(request.POST or None)
      search = None
      if form.is_valid():
          seen = form.cleaned_data.get('skip', [])
          search = self.do_search(sd.model, sd.field, form.cleaned_data, seen)
          if search.instance:
              # If we've found a new record add it to the skiplist
              form.update(search.instance.pk)
          if request.POST.get('next') == 'Replace':
              # Do the replacement on the previous record
              search.do_replace(form.cleaned_data['current_pk'])
      return render(request, "query_replace/search.html",
                    {'form': form, 'search':search, 'model': sd.model, 'field': sd.field})



admin.site.register(SearchDetail, QueryReplaceAdmin)
