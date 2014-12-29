from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',  # prefix

    url(r'^$', 'journal.views.index', name='index'),
    url(r'^issues/$', 'journal.views.show_issues', name='show_issues'),
    url(r'^issues/(\d+)/$', 'journal.views.show_issue', name='show_issue'),
    url(r'^issues/(\d{4})-(\d+)-(\d+)/articles/(\d+)/$', 'journal.views.show_article', name='show_article'),
    url(r'^organizations/(\d+)/$', 'journal.views.show_organization', name='show_organization'),
    url(r'^organizations/search/$', 'journal.views.search_organizations', name='search_organizations'),
    url(r'^authors/(\d+)/$', 'journal.views.show_author', name='show_author'),

    url(r'^authors/edit/$', 'journal.views.edit_author', name='edit_author'),
    url(r'^articles/add/$', 'journal.views.add_article', name='add_article'),
)
