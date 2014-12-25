from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',  # prefix

    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mailauth/', include('mailauth.urls')),

    url(r'^$', 'journal.views.index', name='index'),
    url(r'^issues/$', 'journal.views.show_issues', name='show_issues'),
    url(r'^issues/(\d+)/$', 'journal.views.show_issue', name='show_issue'),
    url(r'^issues/(\d{4})-(\d+)-(\d+)/articles/(\d+)/$', 'journal.views.show_article', name='show_article'),
    url(r'^organizations/(\d+)/$', 'journal.views.show_organization', name='show_organization'),
    url(r'^authors/(\d+)/$', 'journal.views.show_author', name='show_author'),

    url(r'^authors/auth/$', 'journal.views.auth_as_author', name='auth_as_author'),
    url(r'^articles/add/$', 'journal.views.add_article', name='add_article'),

    url(r'^([\w-]+)/$', 'pages.views.pages_page', name='pages_page'),
)
