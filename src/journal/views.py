from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404

from journal.models import Volume


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