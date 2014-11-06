from django import template

from journal.models import Volume


register = template.Library()


@register.simple_tag(takes_context=True)
def volumes_menu(context):
    out = []
    for vol in Volume.objects.all():
        out.append(u'<li%s><a href="%s">%s</a></li>' % (
            ' class="active"' if context.get('volume') == vol else '',
            vol.get_absolute_url(),
            vol
        ))
    return u'\n'.join(out)
