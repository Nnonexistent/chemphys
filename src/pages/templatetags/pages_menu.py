from django import template

from pages.models import Page


register = template.Library()


@register.simple_tag(takes_context=True)
def pages_menu(context):
    out = []
    for page in Page.objects.filter(in_menu=True):
        out.append(u'<li%s><a href="%s">%s</a></li>' % (
            ' class="active"' if context.get('page') == page else '',
            page.get_absolute_url(),
            unicode(page)
        ))
    return u'\n'.join(out)
