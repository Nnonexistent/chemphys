import urllib
from urllib2 import urlparse

from django.utils.http import is_safe_url
from django import http
from django.conf import settings
from django.utils.translation import check_for_language, LANGUAGE_SESSION_KEY


LANG_GET_KEY = 'lang'


def set_language_ex(request):
    next = request.POST.get('next', request.GET.get('next'))
    if not is_safe_url(url=next, host=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'

    # remove lang from query
    scheme, netloc, path, query, fragment = urlparse.urlsplit(next)
    parsed_query = urlparse.parse_qsl(query)
    altered = False
    for k, v in parsed_query[:]:
        if LANG_GET_KEY == k:
            parsed_query.remove((k, v))
            altered = True
    if altered:
        query = urllib.urlencode(parsed_query)
        next = urlparse.urlunsplit((scheme, netloc, path, query, fragment))

    response = http.HttpResponseRedirect(next)
    if request.method == 'POST':
        lang_code = request.POST.get('language', None)
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session[LANGUAGE_SESSION_KEY] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code,
                                    max_age=settings.LANGUAGE_COOKIE_AGE,
                                    path=settings.LANGUAGE_COOKIE_PATH,
                                    domain=settings.LANGUAGE_COOKIE_DOMAIN)
    return response
