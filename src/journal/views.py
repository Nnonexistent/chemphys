from collections import OrderedDict

from django.db.models import Q
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

from journal.models import Issue, Article, Organization, ARTICLE_ADDING_STATUSES, Review, JournalUser
from journal.forms import AuthorEditForm, LocalizedNameFormSet, PIOFormSet, ARTICLE_ADDING_FORMS, ReviewForm


def index(request):
    return render(request, 'index.html', {})


def show_issues(request):
    if request.user.is_authenticated() and request.user.is_staff:
        qs = Issue.objects.all()
    else:
        qs = Issue.objects.filter(is_active=True)

    return render(request, 'journal/issues.html', {
        'title': _('Index'),
        'issues': qs,
    })


def show_issue(request, id):
    kwargs = {'id': id}
    if not (request.user.is_authenticated() and request.user.is_staff):
        kwargs['is_active'] = True
    issue = get_object_or_404(Issue, **kwargs)
    return render(request, 'journal/issue.html', {
        'title': unicode(issue),
        'subtitle': u'' if issue.is_active else _(u'(Inactive)'),
        'issue': issue,
        'articles': issue.article_set.filter(status=10),
    })


def show_article(request, iss_year, iss_volume, iss_number, id):
    kwargs = {'id': id, 'status':10, 'issue__year':iss_year,
              'issue__volume': iss_volume, 'issue__number': iss_number}
    if not (request.user.is_authenticated() and request.user.is_staff):
        kwargs['issue__is_active'] = True

    article = get_object_or_404(Article, **kwargs)
    return render(request, 'journal/article.html', {
        'title': unicode(article),
        'article': article,
        'link': request.build_absolute_uri(),
        'issue': article.issue,
    })


def show_organization(request, id):
    org = get_object_or_404(Organization, id=id, moderation_status=2)
    authors = JournalUser.objects.filter(moderation_status=2, positioninorganization__organization=org).distinct()
    articles = Article.objects.filter(articleauthor__organization=org, status=10, issue__is_active=True).distinct()

    return render(request, 'journal/org.html', {
        'title': unicode(org),
        'org': org,
        'link': request.build_absolute_uri(),
        'articles': articles,
        'authors': authors,
    })


def show_author(request, id):
    author = get_object_or_404(JournalUser, id=id, moderation_status=2)
    orgs = Organization.objects.filter(moderation_status=2, positioninorganization__user=author).distinct()
    articles = Article.objects.filter(articleauthor__user=author, status=10, issue__is_active=True).distinct()

    return render(request, 'journal/author.html', {
        'title': unicode(author),
        'author': author,
        'articles': articles,
        'orgs': orgs,
        'link': request.build_absolute_uri(),
    })


def edit_author(request):
    if request.user.is_authenticated() and request.user.is_active:
        user = JournalUser.objects.get(id=request.user.id)
    else:
        return HttpResponseForbidden()

    if request.method == 'POST':
        name_formset = LocalizedNameFormSet(request.POST, instance=user, prefix='name')
        org_formset = PIOFormSet(request.POST, instance=user, prefix='org')
        form = AuthorEditForm(request.POST, instance=user)
        if form.is_valid() and name_formset.is_valid() and org_formset.is_valid():
            form.save()
            name_formset.save()
            org_formset.save()
            messages.info(request, _(u'Profile was updated'))
            return HttpResponseRedirect(reverse('index'))
    else:
        form = AuthorEditForm(instance=user)
        name_formset = LocalizedNameFormSet(instance=user, prefix='name')
        org_formset = PIOFormSet(instance=user, prefix='org')

    return render(request, 'journal/edit_author.html', {
        'title': _(u'Edit profile'),
        'form': form,
        'name_formset': name_formset,
        'org_formset': org_formset,
    })


def search_organizations(request):
    query = request.POST.get('q') or request.GET.get('q') or ''
    query = query.strip()
    if len(query) >= 3:
        query_qobjs = []
        for q in query.split():
            for arg in ('organizationlocalizedcontent__name', 'alt_names',
                        'previous__organizationlocalizedcontent__name', 'previous__alt_names'):
                query_qobjs.append(Q(**{'%s__icontains' % arg: q}))
        query_qobj = reduce(lambda x, y: x | y, query_qobjs)

        qs_qobj = Q(moderation_status=2)
        if request.user.is_authenticated():
            qs_qobj = (qs_qobj
                      | Q(moderation_status=0, positioninorganization__user=request.user)
                      | Q(moderation_status=0, articleauthor__article__senders=request.user))
        qs = Organization.objects.filter(qs_qobj & query_qobj).distinct()[:50]

        items = [{'id': item.id, 'text': unicode(item)} for item in qs]
    else:
        items = []
    return JsonResponse({'items': items})


def search_authors(request):
    query = request.POST.get('q') or request.GET.get('q') or ''
    query = query.strip()
    if len(query) >= 3:
        query_qobjs = []
        for q in query.split():
            for arg in ('localizedname__first_name', 'localizedname__last_name', 'email'):
                query_qobjs.append(Q(**{'%s__icontains' % arg: q}))
        query_qobj = reduce(lambda x, y: x | y, query_qobjs)

        qs_qobj = Q(moderation_status=2)
        if request.user.is_authenticated():
            qs_qobj = qs_qobj | Q(moderation_status=0, articleauthor__article__senders=request.user)
        qs = JournalUser.objects.filter(qs_qobj & query_qobj).distinct()[:50]

        items = [{'id': item.id, 'text': unicode(item)} for item in qs]
    else:
        items = []
    return JsonResponse({'items': items})


def search_articles(request):
    # TODO: switch to haystack or similar
    query = request.POST.get('q') or request.GET.get('q') or ''
    query = query.strip()
    if len(query) >= 3:
        qobjs = []
        for arg in ('localizedarticlecontent__title', 'localizedarticlecontent__abstract', 'localizedarticlecontent__keywords',
                    'articleauthor__user__localizedname__last_name'):
            qobjs.append(Q(**{'%s__icontains' % arg: query}))
        qobj = reduce(lambda x, y: x | y, qobjs)
        items = Article.objects.filter(status=10).filter(qobj).distinct()[:50]
    else:
        items = []
    return render(request, 'journal/articles.html', {'articles': items, 'title': _(u'Articles found')})


def add_article(request):
    if not request.user.is_authenticated() or not request.user.is_active:
        return HttpResponseForbidden()

    if request.method == 'POST':
        article = Article.objects.create()
        article.senders = JournalUser.objects.filter(id=request.user.id)
        return HttpResponseRedirect(reverse('adding_article', args=(article.id, article.status)))

    return render(request, 'journal/add_article.html', {
        'title': _(u'Add article'),
    })


ARTICLE_ADDING_TITLES = OrderedDict((
    (0, _(u'Overview')),
    (1, _(u'Abstract')),
    (2, _(u'Authors')),
    (3, _(u'Media')),
))


def adding_article(request, article_id, step):
    step = int(step)
    final = (step == 3)
    article = get_object_or_404(Article, id=article_id, senders=request.user, status__in=ARTICLE_ADDING_STATUSES, status__gte=step)
    Form, FormSet = ARTICLE_ADDING_FORMS[step]

    if request.method == 'POST':
        form = Form(request.POST, request.FILES, instance=article)
        formset = FormSet(request.POST, request.FILES, instance=article)
        if form.is_valid() and formset.is_valid():
            formset.save()
            article = form.save(commit=False)
            messages.info(request, _(u'Article draft was updated.'))
            if final:
                continue_url = reverse('send_article', args=[article_id])
            else:
                article.status = step + 1
                continue_url = reverse('adding_article', args=(article_id, article.status))
            form.save_m2m()
            article.save()
            return HttpResponseRedirect(continue_url)
    else:
        form = Form(instance=article)
        formset = FormSet(instance=article)

    return render(request, 'journal/adding_article.html', {
        'title': u'%s: %s' % (_(u'Add article'), ARTICLE_ADDING_TITLES[step]),
        'subtitle': mark_safe(u'%s%s' % (u'<img src="%s" width="100" class="pull-left" />' % article.image.url if article.image else '', article.title)),
        'ARTICLE_ADDING_TITLES': ARTICLE_ADDING_TITLES,
        'step': step,
        'article': article,
        'form': form,
        'formset': formset,
        'final': final,
    })


def send_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, senders=request.user, status=3)
    if request.method == 'POST':
        article.status = 11
        article.save()
        messages.success(request, _(u'Thank you for submission. Your article will be reviewed by our staff. We will notify you soon about progress.'))
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'journal/send_article.html', {
        'title': _(u'Send article'),
        'subtitle': mark_safe(u'%s%s' % (u'<img src="%s" width="100" class="pull-left" />' % article.image.url if article.image else '', article.title)),
        'ARTICLE_ADDING_TITLES': ARTICLE_ADDING_TITLES,
        'article': article,
    })


def edit_review_login(request, key):
    return edit_review(request, key, do_login=True)


def edit_review(request, key, do_login=False):
    from django.contrib.auth import authenticate, login

    review = get_object_or_404(Review, status__in=(0, 1), key=key)
    reviewer_user = get_user_model().objects.get(id=review.reviewer_id) # FIXME: don't call DB for proxy model

    if do_login and request.user.is_anonymous():
        reviewer_user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, reviewer_user)

    if request.user != reviewer_user:
        if do_login:
            messages.warning(request, _(u'You cannot view view this review because you already logged in as different user. Log out and try again.'))
            return HttpResponseRedirect(reverse('index'))
        else:
            raise Http404

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid() and formset.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ReviewForm(instance=review)

    return render(request, 'journal/review.html', {
        'title': _(u'Review for article'),
        'article': review.article,
        'subtitle': unicode(review.article),
        'form': form,
        'review': review,
    })
