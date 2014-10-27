from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',  # prefix

    url(r'^admin/', include(admin.site.urls)),
)
