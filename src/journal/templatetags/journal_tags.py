from django import template

from journal.models import Issue


register = template.Library()


@register.simple_tag(takes_context=True)
def issues_menu(context):
    if context.get('user') and context['user'].is_authenticated() and context['user'].is_staff:
        qs = Issue.objects.all()
    else:
        qs = Issue.objects.filter(is_active=True)
    out = []
    ctx_issue = context.get('issue')
    for issue in qs:
        css_classes = []
        if issue == ctx_issue:
            css_classes.append('active')
        if not issue.is_active:
            css_classes.append('text-muted')
        out.append(u'<li%s><a href="%s">%s</a></li>' % (
            (' class="%s"' % ' '.join(css_classes)) if css_classes else '',
            issue.get_absolute_url(),
            issue
        ))
    return u'\n'.join(out)
