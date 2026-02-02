from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin

def OldUrlsMiddleware(get_response):
    def process_response(request):
        response = get_response(request)
        # No need to check for a redirect for non-404 responses.
        if response.status_code != 404:
            return response

        full_path = request.get_full_path()
        for old, new in settings.OLD_URLS:
            if full_path.startswith(old):
                return HttpResponsePermanentRedirect(full_path.replace(old, new))
        return response
    return process_response

def DjangoResponseMiddleware(get_response):
    def process_response(request):
        response = get_response(request)
        response['X-ServedBy'] = "django"
        return response
    return process_response
