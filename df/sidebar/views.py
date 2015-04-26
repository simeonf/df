from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .models import SidebarEntry

@cache_page(60)
def dvd(request):
    return render(request, "sidebar/dvd.html", SidebarEntry.dvd())

@cache_page(60)
def theater(request):
    return render(request, "sidebar/theater.html", SidebarEntry.theater())
    
