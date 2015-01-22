from hashlib import sha1

from django import template
from django.template.loader import render_to_string
from django.db import models


register = template.Library()


@register.simple_tag(takes_context=True)
def ctxhelp(context, text, placement='auto right'):
    user = context.get('user')
    if not user and context.get('request'):
        user = context['request'].user

    if user.is_authenticated():
        hash = sha1(unicode(text).encode('utf-8')).hexdigest()
        HiddenHelp = models.get_model('ctxhelp.HiddenHelp')  # not using import because tag library and app name clashes
        show = not HiddenHelp.objects.filter(user=user, hash=hash).exists()
    else:
        show = True
        hash = ''

    return render_to_string('ctxhelp/ctxhelp.html', {
        'show': show,
        'text': text,
        'hash': hash,
        'placement': placement,
    })