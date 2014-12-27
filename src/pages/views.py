from django.shortcuts import render
from django.shortcuts import get_object_or_404

from pages.models import Page


def pages_page(request, url):
    page = get_object_or_404(Page, url=url)
    return render(request, 'pages/page.html', {
        'title': page.title,
        'page': page,
    })
