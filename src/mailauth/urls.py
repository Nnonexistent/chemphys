from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',  # prefix
    url(r'^tokens/([0-9a-f]{32})$', 'mailauth.views.auth', name='mailauth_auth'),
)
