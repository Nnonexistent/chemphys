from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404

from journal.models import Issue, Article


def index(request):
    return render(request, 'index.html', {})


def show_issues(request):
    return render(request, 'journal/issues.html', {
        'title': _('Index'),
        'issues': Issue.objects.all(),
    })


def show_issue(request, id):
    issue = get_object_or_404(Issue, id=id)
    return render(request, 'journal/issue.html', {
        'title': unicode(issue),
        'issue': issue,
        'articles': issue.article_set.filter(status=10),
    })


def show_article(request, iss_year, iss_volume, iss_number, id):
    article = get_object_or_404(Article, status=10, id=id,
                                issue__year=iss_year,
                                issue__volume=iss_volume,
                                issue__number=iss_number)
    return render(request, 'journal/article.html', {
        'title': unicode(article),
        'article': article,
        'link': request.build_absolute_uri(),
        'issue': article.issue,
    })
