from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


def auth(request, key):
    user = authenticate(mail_key=key)
    if user is not None and user.is_active:
        login(request, user)
    return HttpResponseRedirect('/')
