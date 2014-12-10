from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',  # prefix

    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'journal.views.index', name='index'),
    url(r'^volumes/$', 'journal.views.show_volumes', name='show_volumes'),
    url(r'^volumes/(\d+)/$', 'journal.views.show_volume', name='show_volume'),
    url(r'^articles/(\d+)/$', 'journal.views.show_article', name='show_article'),

    url(r'^([\w-]+)/$', 'pages.views.pages_page', name='pages_page'),
)
