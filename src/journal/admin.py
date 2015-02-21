from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from journal import models as app_models

# User admin:
# TODO: organization list in list_display
# TODO: article count (published, new etc)


if Group in admin.site._registry:
    admin.site.unregister(Group)


class JournalAdmin(admin.ModelAdmin):
    class Media:
        js = ('admin/js/jquery.init-global.js',
              'js/jquery.autosize.min.js',
              'admin/js/misc.js')


class SectionNameInline(admin.TabularInline):
    model = app_models.SectionName
    extra = len(settings.LANGUAGES)
    max_num = len(settings.LANGUAGES)


class SectionAdmin(JournalAdmin):
    raw_id_fields = ['moderators']
    list_display = ('__unicode__', 'display_moderators', 'articles_count')
    search_fields = ['sectionname__name']
    inlines = [SectionNameInline]

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


class OrganizationLocalizedContentInline(admin.StackedInline):
    model = app_models.OrganizationLocalizedContent
    extra = len(settings.LANGUAGES)
    max_num = len(settings.LANGUAGES)


class OrganizationAdmin(JournalAdmin):
    inlines = [OrganizationLocalizedContentInline]
    list_display = ('__unicode__', 'short_name', 'moderation_status', 'obsolete', 'display_site')
    list_filter = ('moderation_status', 'obsolete')
    search_fields = ('organizationlocalizedcontent__name', 'alt_names', 'short_name',
                     'previous__organizationlocalizedcontent__name', 'previous__alt_names')
    raw_id_fields = ['previous']

    def display_site(self, obj=None):
        if obj and obj.site:
            return mark_safe(u'<a href="%s" target="_blank">%s</a>' % (escape(obj.site), escape(obj.site)))
        return u''
    display_site.short_description = _(u'Site')
    display_site.admin_order_field = 'site'


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
    raw_id_fields = ('user', 'organization')


class ArticleAttachInline(admin.TabularInline):
    model = app_models.ArticleAttach
    extra = 0


class LocalizedArticleContentInline(admin.StackedInline):
    model = app_models.LocalizedArticleContent
    extra = len(settings.LANGUAGES)
    max_num = len(settings.LANGUAGES)


class ReviewInline(admin.StackedInline):
    model = app_models.Review
    extra = 0
    fields = ('reviewer', 'status', 'date_created', 'comment_for_authors', 'comment_for_editors', 'resolution', 'render')
    readonly_fields = ('render', 'date_created')


class ArticleAdmin(JournalAdmin):
    search_fields = ('title', 'abstract', 'references')
    list_filter = ('status', 'type', 'issue', 'sections')
    list_display = ('display_title', 'status', 'type', 'issue', 'display_authors', 'display_reviews')
    inlines = (LocalizedArticleContentInline, ArticleAuthorInline, ArticleSourceInline, ArticleAttachInline, ReviewInline, ArticleResolutionInline)
    raw_id_fields = ['senders']

    # TODO: search by author names

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "sections":
            kwargs['widget'] = forms.CheckboxSelectMultiple
        return super(ArticleAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def save_formset(self, request, form, formset, change):
        if formset.form._meta.model == app_models.Review:
            new_forms = []
            for form in formset:
                if not form.instance.id:
                    new_forms.append(form)
            formset.save()

            for form in new_forms:
                form.instance.send(request.build_absolute_uri)
        else:
            formset.save()

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
                reverse('admin:journal_journaluser_change', args=[user.id]), user))
        return mark_safe(u', '.join(out))
    display_authors.short_description = _(u'Authors')

    def display_reviews(self, obj=None):
        if not obj:
            return u''
        out = []
        for review in obj.review_set.all():
            out.append(u'%s: %s' % (
                review.reviewer.get_full_name() or review.reviewer.username,
                u'%s - %s' % (review.get_status_display(),
                              review.get_resolution_display()) if review.resolution else review.get_status_display()))
        return mark_safe(u'<br />'.join(out))
    display_reviews.short_description = _(u'Reviews')

    # TODO: display review links in article edit page


class ReviewFieldAdmin(JournalAdmin):
    list_display = ('name', 'field_type')


class LocalizedIssueContentInline(admin.StackedInline):
    model = app_models.LocalizedIssueContent
    max_num = len(settings.LANGUAGES)
    extra = len(settings.LANGUAGES)


class IssueAdmin(JournalAdmin):
    inlines = (LocalizedIssueContentInline, )
    list_display = ('__unicode__', 'is_active', 'articles_count')

    def articles_count(self, obj=None):
        if obj:
            return obj.article_set.all().count()
        return u''
    articles_count.short_description = _(u'Articles')


class LocalizedNameInline(admin.TabularInline):
    model = app_models.LocalizedName
    extra = len(settings.LANGUAGES)
    max_num = len(settings.LANGUAGES)


class StaffMemberInline(admin.StackedInline):
    extra = 0
    model = app_models.StaffMember
    max_num = 1



class JournalUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = app_models.JournalUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(JournalUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]


class PositionInOrganizationInline(admin.TabularInline):
    model = app_models.PositionInOrganization
    extra = 0
    raw_id_fields = ('organization', )


class JournalUserAdmin(UserAdmin):
    form = JournalUserChangeForm
    add_form = forms.ModelForm
    inlines = (StaffMemberInline, LocalizedNameInline, PositionInOrganizationInline)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('moderation_status', 'is_active', 'is_staff', 'is_superuser')}),
        (_('Profile'), {'fields': ('degree', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email',),
        }),
    )
    readonly_fields = ('last_login', 'date_joined')
    list_display = ('__unicode__', 'email', 'is_active', 'moderation_status', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'moderation_status')
    search_fields = ('localizedname__first_name', 'localizedname__last_name', 'email')
    ordering = None  # handled inside get_queryset

    def get_formsets_with_inlines(self, request, obj=None):
        if obj is None:
            return ()
        return super(JournalUserAdmin, self).get_formsets_with_inlines(request, obj)

    def get_queryset(self, request):
        from django.db import models

        qs = self.model._default_manager.get_queryset()
        # For ordering by localizedname__last_name
        ordering = self.get_ordering(request) + ('localizedname__last_name__max', )
        qs = qs.annotate(models.Max('localizedname__last_name')).order_by(*ordering)
        return qs


admin.site.register(app_models.Organization, OrganizationAdmin)
admin.site.register(app_models.Section, SectionAdmin)
admin.site.register(app_models.Article, ArticleAdmin)
admin.site.register(app_models.ReviewField, ReviewFieldAdmin)
admin.site.register(app_models.Issue, IssueAdmin)
admin.site.register(app_models.JournalUser, JournalUserAdmin)
