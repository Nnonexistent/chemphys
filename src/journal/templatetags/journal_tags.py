from django import template

from journal.models import Issue


register = template.Library()


@register.simple_tag(takes_context=True)
def issues_menu(context):
    out = []
    for issue in Issue.objects.all():
        out.append(u'<li%s><a href="%s">%s</a></li>' % (
            ' class="active"' if context.get('issue') == issue else '',
            issue.get_absolute_url(),
            issue
        ))
    return u'\n'.join(out)
