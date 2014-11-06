from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',  # prefix

    url(r'^$', 'journal.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^([\w-]+)/$', 'pages.views.pages_page', name='pages_page'),
)
