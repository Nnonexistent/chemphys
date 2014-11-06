from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.conf import settings
from django.contrib.auth import get_user_model

from journal import models as app_models


def override_formset_factory(get_real_instance):
    # We need to rewrite "instance" and "queryset" because they passed as args to FormSet in ModelAdmin._create_formsets
    # and we cannot override it at ModelAdmin.get_formsets_with_inlines

    class OverrideInlineFormSet(BaseInlineFormSet):
        def __init__(self, *args, **kwargs):
            super(OverrideInlineFormSet, self).__init__(*args, **kwargs)
            self.instance = get_real_instance(self.instance)
            queryset = kwargs.pop('queryset', self.model._default_manager)
            self.queryset = queryset.filter(**{self.fk.name: self.instance})

    return OverrideInlineFormSet


class SectionAdmin(admin.ModelAdmin):
    raw_id_fields = ['moderators']
    list_display = ('name', 'display_moderators', 'articles_count')
    search_fields = ['name']

    def display_moderators(self, obj=None):
        if obj:
            return u', '.join(map(unicode, obj.moderators.all()))
        return u''
    display_moderators.short_description = _(u'Moderators')

    def articles_count(self, obj=None):
        if obj:
            return obj.article_set.all().count()
        return u''
    articles_count.short_description = _(u'Articles')

    # TODO: check staff memebership for moderators, make select with only valid choices


class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('display_user', 'chief_editor', 'editor', 'reviewer', 'moderated_sections')
    list_filter = ('editor', 'reviewer')
    search_fields = ('user__username', 'user__last_name')

    def moderated_sections(self, obj=None):
        if obj:
            sections = app_models.Section.objects.filter(moderators=obj.user)
            return mark_safe(
                u'<br />'.join(u'<a href="%s">%s</a>' % (
                    reverse('admin:journal_section_change', args=[s.id]), escape(s)) for s in sections)
            )
        return u''
    moderated_sections.short_description = _(u'Moderated sections')

    def display_user(self, obj=None):
        if obj:
            return obj.user.get_full_name() or obj.user.username
        return u''
    display_user.short_description = _(u'Name')
    display_user.admin_order_field = 'user__last_name'

    # TODO: make user field read-only for editing
    # TODO: display users names instead of usernames in select widget


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'moderation_status', 'country', 'city', 'obsolete', 'display_site')
    list_filter = ('moderation_status', 'obsolete')
    search_fields = ('name', 'alt_names', 'previous__name', 'previous__alt_names')
    raw_id_fields = ['previous']

    def display_site(self, obj=None):
        if obj and obj.site:
            return mark_safe(u'<a href="%s" target="_blank">%s</a>' % (escape(obj.site), escape(obj.site)))
        return u''
    display_site.short_description = _(u'Site')
    display_site.admin_order_field = 'site'

    # TODO: filter previous orgs by obsolete flag


class PositionInOrganizationInline(admin.TabularInline):
    extra = 0
    model = app_models.PositionInOrganization


class LocalizedNameInline(admin.TabularInline):
    extra = 0
    model = app_models.LocalizedName


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('display_user', 'moderation_status')
    list_filter = ['moderation_status']

    def display_user(self, obj=None):
        if obj:
            return obj.user.get_full_name() or obj.user.username
        return u''
    display_user.short_description = _(u'Name')
    display_user.admin_order_field = 'user__last_name'

    def get_formsets_with_inlines(self, request, obj=None):
        formset_class = override_formset_factory(lambda x: x.user if x.user_id else None)

        formset = inlineformset_factory(get_user_model(), app_models.LocalizedName, extra=0, formset=formset_class)
        yield formset, LocalizedNameInline(get_user_model(), admin.site)

        formset = inlineformset_factory(get_user_model(), app_models.PositionInOrganization, extra=0, formset=formset_class)
        yield formset, PositionInOrganizationInline(get_user_model(), admin.site)
        
        for formset, inline in super(AuthorAdmin, self).get_formsets_with_inlines(request, obj):
            yield formset, inline

    # TODO: make user field read-only for editing
    # TODO: display users names instead of usernames in select widget


class ArticleSourceInline(admin.TabularInline):
    model = app_models.ArticleSource
    extra = 0


class ArticleResolutionInline(admin.TabularInline):
    model = app_models.ArticleResolution
    extra = 0


class OrderedAuthorsInline(admin.TabularInline):
    model = app_models.OrderedAuthors
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    inlines = (OrderedAuthorsInline, ArticleSourceInline, ArticleResolutionInline)


class ReviewFileInline(admin.TabularInline):
    model = app_models.ReviewFile
    extra = 0


class ReviewAdmin(admin.ModelAdmin):
    inlines = [ReviewFileInline]


class VolumeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'articles_count')

    def articles_count(self, obj=None):
        if obj:
            return obj.article_set.all().count()
        return u''
    articles_count.short_description = _(u'Articles')


admin.site.register(app_models.Organization, OrganizationAdmin)
admin.site.register(app_models.Section, SectionAdmin)
admin.site.register(app_models.StaffMember, StaffMemberAdmin)
admin.site.register(app_models.Author, AuthorAdmin)
admin.site.register(app_models.Article, ArticleAdmin)
admin.site.register(app_models.Review, ReviewAdmin)
admin.site.register(app_models.Volume, VolumeAdmin)
