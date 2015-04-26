from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponsePermanentRedirect

class OldUrlsMiddleware(object):
    def process_response(self, request, response):
        # No need to check for a redirect for non-404 responses.
        if response.status_code != 404:
            return response

        full_path = request.get_full_path()
        for old, new in settings.OLD_URLS:
            if full_path.startswith(old):
                return http.HttpResponsePermanentRedirect(full_path.replace(old, new))
        return response
