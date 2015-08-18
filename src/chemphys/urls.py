from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',  # prefix

    url(r'^i18n/setlang/$', 'chemphys.views.set_language_ex'),  # override django.views.i18n.set_language
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mailauth/', include('mailauth.urls')),
    url(r'^ctxhelp/', include('ctxhelp.urls')),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^', include('journal.urls')),

    url(r'^([\w-]+)/$', 'pages.views.pages_page', name='pages_page'),
)
