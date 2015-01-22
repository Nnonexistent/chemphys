from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',  # prefix

    url(r'^ctxhelp.js$', 'ctxhelp.views.render_js', name='ctxhelp_js'),
    url(r'^([a-f0-9]{40})/show/$', 'ctxhelp.views.show_help', name='ctxhelp_show'),
    url(r'^([a-f0-9]{40})/hide/$', 'ctxhelp.views.hide_help', name='ctxhelp_hide'),
)
