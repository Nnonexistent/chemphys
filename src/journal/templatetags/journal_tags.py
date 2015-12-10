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


import itertools


class ResetCycleNode(template.Node):
    def __init__(self, variable_name, cycle_node):
        self.variable_name = variable_name
        self.cycle_node = cycle_node

    def render(self, context):
        cycle_iter = itertools.cycle(self.cycle_node.cyclevars)
        context.render_context[self.cycle_node] = cycle_iter
        context[self.variable_name] = next(cycle_iter).resolve(context)
        return ''


@register.tag
def reset_cycle(parser, token, escape=False):
    args = token.split_contents()

    if len(args) != 2:
        raise TemplateSyntaxError("'reset_cycle' tag requires exactly one argument")

    name = args[1]
    if not hasattr(parser, '_namedCycleNodes'):
        raise TemplateSyntaxError("No named cycles in template. '%s' is not defined" % name)
    if name not in parser._namedCycleNodes:
        raise TemplateSyntaxError("Named cycle '%s' does not exist" % name)

    return ResetCycleNode(name, parser._namedCycleNodes[name])
