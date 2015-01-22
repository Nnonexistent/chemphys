from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib import messages

from mailauth.forms import MailAuthForm


def auth(request, key):
    user = authenticate(mail_key=key)
    if user is not None and user.is_active:
        login(request, user)
    return HttpResponseRedirect('/')


def auth_form(request):
    if request.method == 'POST':
        form = MailAuthForm(request.POST)
        if form.is_valid():
            form.save(uri_builder=request.build_absolute_uri)
            messages.info(request, _(u'The authentication link was sent on your e-mail "%s"') % form.cleaned_data['email'])
            return HttpResponseRedirect('/')
    else:
        form = MailAuthForm()

    return render(request, 'mailauth/auth.html', {
        'title': _('Authentication'),
        'form': form,
    })
