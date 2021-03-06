from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.conf import settings

from pages.models import Page, LocalizedPageContent


class LocalizedPageContentInline(admin.StackedInline):
    extra = 0
    model = LocalizedPageContent
    max_num = len(settings.LANGUAGES)


class PageAdmin(admin.ModelAdmin):
    class Media:
        js = ('admin/js/jquery.init-global.js',
              'js/jquery.autosize.min.js',
              'admin/js/misc.js')

    list_display = ('__unicode__', 'in_menu', 'display_link')
    inlines = [LocalizedPageContentInline]

    def display_link(self, obj=None):
        if obj:
            return mark_safe(u'<a href="%s" target="_blank">%s</a>' % (
                obj.get_absolute_url(), obj.get_absolute_url()))
        return u''
    display_link.short_description = _(u'Link')


admin.site.register(Page, PageAdmin)
