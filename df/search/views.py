from urllib import urlencode
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

from utility import page

from .forms import SearchForm, empty_choice
from .search import build_query
from article.models import Article, Genre, Tags

@csrf_exempt
def search(request):
    letters = [chr(num) for num in range(ord('A'), ord('Z') + 1)]
    form = SearchForm(request.GET or None)
    form.fields['genre'].choices = empty_choice + [(g.id, g.title) for g in Genre.objects.all().order_by('title')]
    form.fields['label'].choices = empty_choice + [(tag.id, tag.title) for tag in Tags.objects.all().order_by('title')]
    if request.GET:
        if form.is_valid():
            sql, values = build_query(request.GET)
            hits = list(Article.objects.raw(sql, values))
            if len(hits) == 1:
                return redirect(hits[0])
            paginator = Paginator(hits, 20)
            data = dict(request.GET)
            if 'page' in data:
              data.pop('page')
            data = dict((k, v[0]) for k,v in data.items() if v[0])
            return render(request, "search/list.html", {'hits': page(request, paginator), 'qs': "&" + urlencode(data)})
    return render(request, "search/search.html", {'letters': letters, 'form': form})
