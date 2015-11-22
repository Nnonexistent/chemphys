import html5lib
from lxml import cssselect, etree
from hashlib import sha1

from django import template
from django.template.loader import render_to_string
from django.db import models


DEFAULT_PLACEMENT = 'auto right'
DEFAULT_SELECTOR = 'p.helptext'

register = template.Library()


@register.simple_tag(takes_context=True)
def ctxhelp(context, text, placement=DEFAULT_PLACEMENT):
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


def ctxparse(text, context, placement, selector):
    doc = html5lib.parse(text, treebuilder='lxml', namespaceHTMLElements=False)
    css = cssselect.CSSSelector(selector)
    out = etree.tostring(doc, encoding='utf-8').decode('utf-8')

    for node in css(doc):
        old = etree.tostring(node, encoding='utf-8').decode('utf-8')
        innertext = node.text + ''.join([etree.tostring(child, encoding='utf-8').decode('utf-8') + child.tail for child in node.iterdescendants()])
        new = ctxhelp(context, innertext, placement)
        out = out.replace(old, new, 1)
    return out


@register.tag(name='ctxblock')
def do_ctxblock(parser, token):
    args = token.split_contents() or DEFAULT_SELECTOR
    if len(args) not in (1, 2, 3):
        raise template.TemplateSyntaxError("%r tag has two optional argument" % token.contents.split()[0])

    tag_name, placement, selector = (args + [None, None])[:3]
    if placement is None:
        placement = DEFAULT_PLACEMENT
    if selector is None:
        selector = DEFAULT_SELECTOR

    nodelist = parser.parse(['endctxblock'])
    parser.delete_first_token()
    return CtxBlockNode(nodelist, placement, selector)


class CtxBlockNode(template.Node):
    def __init__(self, nodelist, placement, selector):
        self.nodelist = nodelist
        self.placement = template.Variable(placement)
        self.selector = template.Variable(selector)

    def render(self, context):
        try:
            placement = self.placement.resolve(context)
        except template.VariableDoesNotExist:
            placement = DEFAULT_PLACEMENT
        try:
            selector = self.selector.resolve(context)
        except template.VariableDoesNotExist:
            selector = DEFAULT_SELECTOR
        output = self.nodelist.render(context)
        return ctxparse(output, context, placement, selector)
