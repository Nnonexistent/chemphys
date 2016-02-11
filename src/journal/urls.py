from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',  # prefix

    url(r'^$', 'journal.views.index', name='index'),
    url(r'^issues/$', 'journal.views.show_issues', name='show_issues'),
    url(r'^issues/(?P<year>\d{4})-(?P<volume>\d+)-(?P<number>\d+)/$', 'journal.views.show_issue', name='show_issue'),
    url(r'^issues/(?P<year>\d{4})-(?P<volume>\d+)/$', 'journal.views.show_issue', name='show_issue'),
    url(r'^issues/(?P<year>\d{4})-(?P<volume>\d+)-(?P<number>\d+)/articles/(?P<id>\d+)/$', 'journal.views.show_article', name='show_article'),
    url(r'^issues/(?P<year>\d{4})-(?P<volume>\d+)/articles/(?P<id>\d+)/$', 'journal.views.show_article', name='show_article'),
    url(r'^pdf/([\d_.-]+).pdf$', 'journal.views.redirect_old_article', name='redirect_old_article'),
    url(r'^organizations/(\d+)/$', 'journal.views.show_organization', name='show_organization'),
    url(r'^organizations/search/$', 'journal.views.search_organizations', name='search_organizations'),
    url(r'^authors/(\d+)/$', 'journal.views.show_author', name='show_author'),
    url(r'^authors/search/$', 'journal.views.search_authors', name='search_authors'),

    url(r'^authors/edit/$', 'journal.views.edit_author', name='edit_author'),
    url(r'^articles/add/$', 'journal.views.add_article', name='add_article'),
    url(r'^articles/(\d+)/adding/(\d)/$', 'journal.views.adding_article', name='adding_article'),
    url(r'^articles/(\d+)/rework/(\d)/$', 'journal.views.adding_article', name='rework_article'),
    url(r'^articles/(\d+)/send/$', 'journal.views.send_article', name='send_article'),
    url(r'^articles/search/$', 'journal.views.search_articles', name='search_articles'),

    url(r'^reviews/([0-9a-f]{32})$', 'journal.views.edit_review', name='edit_review'),
    url(r'^reviews/([0-9a-f]{32})/login$', 'journal.views.edit_review_login', name='edit_review_login'),
)
