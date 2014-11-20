from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404

from journal.models import Volume, Article


def index(request):
    return render(request, 'index.html', {})


def show_volumes(request):
    return render(request, 'journal/volumes.html', {
        'title': _('Index'),
        'volumes': Volume.objects.all(),
    })


def show_volume(request, id):
    vol = get_object_or_404(Volume, id=id)
    return render(request, 'journal/volume.html', {
        'title': unicode(vol),
        'volume': vol,
        'articles': vol.article_set.filter(status=10),
    })


def show_article(request, id):
    article = get_object_or_404(Article, id=id, status=10)
    return render(request, 'journal/article.html', {
        'title': unicode(article),
        'article': article,
        'link': request.build_absolute_uri(),
    })
