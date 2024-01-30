from django.shortcuts import render
from utility import cache_page_for_guests as cache_page

from .models import SidebarEntry

@cache_page(60)
def dvd(request):
    return render(request, "sidebar/dvd.html", SidebarEntry.dvd())

@cache_page(60)
def theater(request):
    return render(request, "sidebar/theater.html", SidebarEntry.theater())
