from django.http import HttpResponse
from django.shortcuts import render, render_to_response

from ctxhelp.models import HiddenHelp


def render_js(request):
    return render_to_response('ctxhelp/ctxhelp.js', content_type='application/x-javascript')


def show_help(request, hash):
    if request.user.is_authenticated():
        HiddenHelp.objects.filter(user=request.user, hash=hash).delete()
    return HttpResponse()


def hide_help(request, hash):
    if request.user.is_authenticated():
        HiddenHelp.objects.get_or_create(user=request.user, hash=hash)
    return HttpResponse()
