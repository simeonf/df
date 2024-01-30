from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from utility import cache_page_for_guests as cache_page

from .models import MailBag

PER_PAGE = 20

def page(request, paginator):
    page = request.GET.get('page')
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    return records

@cache_page(60)
def index(request):
    paginator = Paginator(MailBag.objects.filter(display=True).order_by("-dt"), PER_PAGE)
    return render(request, "mailbag/index.html", {'mailbags': page(request, paginator),
                                                  'title': 'Mail',
                                                  'blurb': "SDG responds to readers' mail"})

def mailbag(request, slug):
    mailbag = get_object_or_404(MailBag, slug=slug)
    return render(request, "mailbag/mailbag.html", {'mailbag': mailbag,
                                                    'title': mailbag.title,
                                                    'blurb': mailbag.blurb})
