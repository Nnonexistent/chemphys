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


class JournalAdmin(admin.ModelAdmin):
    class Media:
        js = ('admin/js/jquery.init-global.js',
              'js/jquery.autosize.min.js',
              'admin/js/misc.js')


class SectionAdmin(JournalAdmin):
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
    # TODO: count all published, all in moderation separately
    # TODO: pending reviews


class StaffMemberAdmin(JournalAdmin):
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
    # TODO: pending reviews


class OrganizationLocalizedContentInline(admin.StackedInline):
    extra = 0
    model = app_models.OrganizationLocalizedContent
    max_num = len(settings.LANGUAGES)


class OrganizationAdmin(JournalAdmin):
    inlines = [OrganizationLocalizedContentInline]
    list_display = ('__unicode__', 'moderation_status', 'obsolete', 'display_site')
    list_filter = ('moderation_status', 'obsolete')
    search_fields = ('organizationlocalizedcontent__name', 'alt_names',
                     'previous__organizationlocalizedcontent__name', 'previous__alt_names')
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
    max_num = len(settings.LANGUAGES)


class AuthorAdmin(JournalAdmin):
    list_display = ('display_user', 'moderation_status')
    list_filter = ['moderation_status']
    search_fields = ('user__username', 'user__last_name', 'user__localizedname__last_name')

    def display_user(self, obj=None):
        if obj:
            return obj.user.get_full_name() or obj.user.username
        return u''
    display_user.short_description = _(u'Name')
    display_user.admin_order_field = 'user__last_name'

    def get_formsets_with_inlines(self, request, obj=None):
        formset_class = override_formset_factory(lambda x: x.user if x.user_id else None)

        formset = inlineformset_factory(
            app_models.LocalizedUser, app_models.LocalizedName,
            extra=LocalizedNameInline.extra, formset=formset_class, max_num=LocalizedNameInline.max_num)
        yield formset, LocalizedNameInline(app_models.LocalizedUser, admin.site)

        formset = inlineformset_factory(
            app_models.LocalizedUser, app_models.PositionInOrganization,
            extra=PositionInOrganizationInline.extra, formset=formset_class)
        yield formset, PositionInOrganizationInline(app_models.LocalizedUser, admin.site)

        for formset, inline in super(AuthorAdmin, self).get_formsets_with_inlines(request, obj):
            yield formset, inline

    # TODO: organization list in list_display
    # TODO: article count (published, new etc)

    # TODO: make user field read-only for editing
    # TODO: display users names instead of usernames in select widget


class ArticleSourceInline(admin.TabularInline):
    model = app_models.ArticleSource
    extra = 0


class ArticleResolutionInline(admin.TabularInline):
    model = app_models.ArticleResolution
    extra = 0
    raw_id_fields = ['reviews']


class ArticleAuthorInline(admin.TabularInline):
    model = app_models.ArticleAuthor
    extra = 0


class ArticleAttachInline(admin.TabularInline):
    model = app_models.ArticleAttach
    extra = 0


class LocalizedArticleContentInline(admin.StackedInline):
    model = app_models.LocalizedArticleContent
    extra = 0
    max_num = len(settings.LANGUAGES)


class ArticleAdmin(JournalAdmin):
    search_fields = ('title', 'abstract', 'references')
    list_filter = ('status', 'type', 'issue', 'sections')
    list_display = ('display_title', 'type', 'issue', 'display_authors', 'display_reviews')
    inlines = (LocalizedArticleContentInline, ArticleAuthorInline, ArticleSourceInline, ArticleAttachInline, ArticleResolutionInline)
    filter_horizontal = ['senders']  # TODO: raw_id_field

    # TODO: search by author names

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "sections":
            kwargs['widget'] = forms.CheckboxSelectMultiple
        return super(ArticleAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def display_title(self, obj=None, max_length=64):
        if not obj:
            return u''
        if len(obj.title) > max_length:
            return unicode(obj)[:max_length-4].rstrip() + '...'
        return unicode(obj)
    display_title.short_description = _(u'Title')

    def display_authors(self, obj=None):
        if not obj:
            return u''
        out = []
        for user in obj.get_authors():
            out.append(u'<a href="%s" target="_blank">%s</a>' % (
                reverse('admin:journal_author_change', args=[user.author.id]), user.get_full_name() or user.username))
        return mark_safe(u', '.join(out))
    display_authors.short_description = _(u'Authors')

    def display_reviews(self, obj=None):
        if not obj:
            return u''
        out = []
        for review in obj.review_set.all():
            out.append(u'<a href="%s" target="_blank">%s: %s</a>' % (
                reverse('admin:journal_review_change', args=[review.id]),
                review.reviewer.get_full_name() or review.reviewer.username,
                u'%s - %s' % (review.get_status_display(),
                              review.get_resolution_display()) if review.resolution else review.get_status_display()))
        return mark_safe(u'<br />'.join(out))
    display_reviews.short_description = _(u'Reviews')

    # TODO:display review links in article edit page


class ReviewFieldAdmin(JournalAdmin):
    list_display = ('name', 'field_type')


class ReviewFileInline(admin.TabularInline):
    model = app_models.ReviewFile
    extra = 0


class ReviewAdmin(JournalAdmin):
    inlines = [ReviewFileInline]
    list_display = ('__unicode__', 'reviewer', 'status', 'resolution', 'date_created')
    list_filter = ('status', 'resolution')


class IssueAdmin(JournalAdmin):
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
admin.site.register(app_models.ReviewField, ReviewFieldAdmin)
admin.site.register(app_models.Review, ReviewAdmin)
admin.site.register(app_models.Issue, IssueAdmin)
