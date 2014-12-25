from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect


def auth(request, key):
    authenticate(mail_key=key)
    return HttpResponseRedirect('/')
