# -*- coding:utf-8 -*-

from collections import OrderedDict
from itertools import chain

from django import forms
from django.conf import settings
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.translation import ugettext as _
from django.db import transaction
from django.template.loader import render_to_string

from utils.forms import BootstrapForm, NullForm
from utils.localized import BaseLocalizedForm, BaseLocalizedFormSet
from journal.models import Article, LocalizedArticleContent, ArticleSource, ArticleAuthor, JournalUser, LocalizedName, Organization, OrganizationLocalizedContent, ArticleAttach


class OverviewArticleForm(BootstrapForm):
    class Meta:
        model = Article
        fields = ('lang', 'type', 'sections', 'image', 'report')

    def __init__(self, *args, **kwargs):
        super(OverviewArticleForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget = forms.RadioSelect(choices=self.fields['type'].choices)
        self.fields['sections'].help_text = ''
        self.fields['sections'].widget = forms.CheckboxSelectMultiple(choices=self.fields['sections'].widget.choices)
        self.fields['image'].help_text = _(u'Файл иллюстрации, отражающей главный результат вашей работы. Он будет размещен на странице статьи и в содержании выпуска.')
        try:
            initial_file = self.instance.articlesource_set.latest().file
        except ArticleSource.DoesNotExist:
            initial_file = None
        self.fields = OrderedDict([('file',
            forms.FileField(
                label=_(u'Article file'), required=True, initial=initial_file,
                help_text=_(u'Укажите файл статьи, подготовленный на основе шаблона в формате MS Word.')
        ))] + self.fields.items())

    def save(self, commit=True):
        obj = super(OverviewArticleForm, self).save(commit)
        # We assume article is already has an id
        if self.files.get('file'):
            obj.articlesource_set.add(ArticleSource.objects.create(article=obj, file=self.files['file']))
        return obj


class BaseLocalizedArticleTitleFormSet(BaseLocalizedFormSet):
    def clean(self):
        super(BaseLocalizedFormSet, self).clean()
        titles = [form.cleaned_data.get('title') for form in self]
        if not any(titles):
            raise forms.ValidationError(_(u'Title must be filled at least at one language'))


LocalizedArticleTitleFormSet = inlineformset_factory(Article, LocalizedArticleContent,
    fields=('lang', 'title'), extra=len(settings.LANGUAGES), max_num=len(settings.LANGUAGES),
    can_delete=False, form=BaseLocalizedForm, formset=BaseLocalizedArticleTitleFormSet)


LocalizedArticleAbstractFormSet = inlineformset_factory(Article, LocalizedArticleContent,
    fields=('lang', 'abstract', 'keywords', 'references'), extra=len(settings.LANGUAGES), max_num=len(settings.LANGUAGES),
    can_delete=False, form=BaseLocalizedForm, formset=BaseLocalizedFormSet)


class AuthorForm(BootstrapForm):
    _org_fields = ('site', )
    _org_loc_fields = ('name', 'country', 'city', 'address')
    _user_fields = ('email', )
    _user_loc_fields = ('first_name', 'last_name')

    author = ArticleAuthor._meta.get_field('user').formfield(required=False, widget=forms.Select)
    organization = ArticleAuthor._meta.get_field('organization').formfield(required=False, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)

        # user
        user = None
        choices = [('', _(u'Add new author to Journal'))]
        if self.instance.id:
            user = self.instance.user
            self.fields['author'].initial = user
            choices.append((user.id, unicode(user)))

        key = self.add_prefix(u'author')
        if self.data.get(key):
            try:
                user = JournalUser.objects.get(id=int(self.data[key]))
            except ValueError:
                pass
            else:
                choices.append((user.id, unicode(user)))

        self.fields['author'].widget.choices = choices

        for key, field in chain(self.iter_user_fields(), self.iter_user_loc_fields()):
            self.fields[key] = field.formfield(required=False)

        # organization
        org = None
        choices = [('', _(u'Add new organization to Journal'))]
        if self.instance.id:
            org = self.instance.organization
            self.fields['organization'].initial = org
            choices.append((org.id, unicode(org)))

        key = self.add_prefix(u'organization')
        if self.data.get(key):
            try:
                org = Organization.objects.get(id=int(self.data[key]))
            except ValueError:
                pass
            else:
                choices.append((org.id, unicode(org)))

        self.fields['organization'].widget.choices = choices

        for key, field in chain(self.iter_org_fields(), self.iter_org_loc_fields()):
            self.fields[key] = field.formfield(required=False)

        self._all_fields = self.fields

    def iter_org_fields(self):
        for field in Organization._meta.fields:
            if field.name in self._org_fields:
                key = u'org_%s' % field.name
                yield key, field

    def iter_org_loc_fields(self, lang_code=None):
        if lang_code == None:
            langs = settings.LANGUAGES
        else:
            langs = [(lang_code, u'')]

        for lang_code, lang_name in langs:
            for field in OrganizationLocalizedContent._meta.fields:
                if field.name in self._org_loc_fields:
                    key = u'org_%s_%s' % (lang_code, field.name)
                    yield key, field

    def iter_user_fields(self):
        for field in JournalUser._meta.fields:
            if field.name in self._user_fields:
                key = u'author_%s' % field.name
                yield key, field

    def iter_user_loc_fields(self, lang_code=None):
        if lang_code == None:
            langs = settings.LANGUAGES
        else:
            langs = [(lang_code, u'')]

        for lang_code, lang_name in langs:
            for field in LocalizedName._meta.fields:
                if field.name in self._user_loc_fields:
                    key = u'author_%s_%s' % (lang_code, field.name)
                    yield key, field

    # TODO: restrict self deletion
    # TODO: fetch organization initial choices from user's profile

    def has_changed(self):
        return (super(AuthorForm, self).has_changed()
                or not self.cleaned_data.get('author')
                or not self.cleaned_data.get('organization'))

    def clean_author_email(self):
        email = self.cleaned_data.get('author_email')
        if email and JournalUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_(u'User with this e-mail is already registered in Journal. Find him by typing his last name in selection field above.'))
        return email

    def clean(self):
        if not self.cleaned_data.get('author') and not self._errors.get('author'):  # new author
            for key, field in self.iter_user_fields():
                if not field.blank and not self.cleaned_data.get(key):
                    self._errors.setdefault(key, []).append(_(u'This field is required if new author specified.'))

            all_empty = True
            for lang_code, lang_name in settings.LANGUAGES:
                empty = True
                errors = []
                for key, field in self.iter_user_loc_fields(lang_code=lang_code):
                    value = self.cleaned_data.get(key)
                    if value:
                        empty = False
                    elif not field.blank:
                        errors.append((key, _(u'This field is required if new author specified.')))

                if not empty:
                    for key, error in errors:
                        self._errors.setdefault(key, []).append(error)
                    all_empty = False
            if all_empty:
                self._errors.setdefault('author', []).append(_(u'Author data must be filled at least for one language'))

        if not self.cleaned_data.get('organization') and not self._errors.get('organization'):  # new organization
            for key, field in self.iter_org_fields():
                if not field.blank and not self.cleaned_data.get(key):
                    self._errors.setdefault(key, []).append(_(u'This field is required if new organization specified.'))

            all_empty = True
            for lang_code, lang_name in settings.LANGUAGES:
                empty = True
                errors = []
                for key, field in self.iter_org_loc_fields(lang_code=lang_code):
                    value = self.cleaned_data.get(key)
                    if value:
                        empty = False
                    elif not field.blank:
                        errors.append((key, _(u'This field is required if new organization specified.')))

                if not empty:
                    for key, error in errors:
                        self._errors.setdefault(key, []).append(error)
                    all_empty = False
            if all_empty:
                self._errors.setdefault('organization', []).append(_(u'Organization data must be filled at least for one language'))

        return self.cleaned_data

    @transaction.atomic
    def save(self, commit=True):  # commit will be True in formset.save()
        # user
        if self.cleaned_data.get('author'):
            author = self.cleaned_data.get('author')
        else:
            kwargs = {}
            for key, field in self.iter_user_fields():
                kwargs[field.name] = self.cleaned_data[key]
            author = JournalUser.objects.create(**kwargs)

            for lang_code, lang_name in settings.LANGUAGES:
                kwargs = {}
                for key, field in self.iter_user_loc_fields(lang_code=lang_code):
                    kwargs[field.name] = self.cleaned_data[key]
                if any(kwargs.values()):  # dont't save empty localized data
                    LocalizedName.objects.create(user=author, lang=lang_code, **kwargs)

        # organization
        if self.cleaned_data.get('organization'):
            org = self.cleaned_data.get('organization')
        else:
            kwargs = {}
            for key, field in self.iter_org_fields():
                kwargs[field.name] = self.cleaned_data[key]
            org = Organization.objects.create(**kwargs)

            for lang_code, lang_name in settings.LANGUAGES:
                kwargs = {}
                for key, field in self.iter_org_loc_fields(lang_code=lang_code):
                    kwargs[field.name] = self.cleaned_data[key]
                if any(kwargs.values()):  # don't save empty localized data
                    OrganizationLocalizedContent.objects.create(org=org, lang=lang_code, **kwargs)

        aa = super(AuthorForm, self).save(commit=False)
        aa.organization = org
        aa.user = author
        try:
            order = int(self.cleaned_data.get('ORDER') or '')
        except ValueError:
            pass
        else:
            if order > 0:
                aa.order = order
        aa.save()
        return aa

    def __unicode__(self):
        def subform(*fields):
            self.fields = OrderedDict((k, v) for k, v in self.fields.items() if k in dict(fields))
            out = self.as_div()
            self.fields = self._all_fields
            return out

        user_subforms = []
        org_subforms = []
        for lang_code, lang_name in settings.LANGUAGES:
            user_subforms.append({'render': subform(*self.iter_user_loc_fields(lang_code)),
                                  'lang': lang_code, 'col_md': 12 / len(settings.LANGUAGES)})
            org_subforms.append({'render': subform(*self.iter_org_loc_fields(lang_code)),
                                 'lang': lang_code, 'col_md': 12 / len(settings.LANGUAGES)})

        return render_to_string(u'journal/forms/article_author.html', {
            'form': self,
            'LANGUAGES': settings.LANGUAGES,
            'common_mainform': subform(('DELETE', ''), ('ORDER', ''), ('id', ''), ('article', '')),
            'user_mainform': subform(('author', '')),
            'user_subform': subform(*self.iter_user_fields()),
            'org_mainform': subform(('organization', '')),
            'org_subform': subform(*self.iter_org_fields()),
            'user_subforms': user_subforms,
            'org_subforms': org_subforms,
        })


class BaseAuthorsFormSet(BaseInlineFormSet):
    def __unicode__(self):
        return render_to_string(u'journal/forms/article_author_formset.html', {'formset': self})

    def add_fields(self, form, index):
        super(BaseAuthorsFormSet, self).add_fields(form, index)
        form.fields['ORDER'].widget = forms.HiddenInput()

    def clean(self):
        emails = []
        for form in self.forms:
            email = form.cleaned_data.get('author_email')
            if email:
                if email in emails:
                    form._errors.setdefault('author_email', []).append(_(u'Duplicate e-mails. Each author must have unique e-mail.'))
                emails.append(email)

#        if not any(form.is_valid() for form in self.forms) or len(self.forms) == 0:
        if self.total_form_count() - len(self.deleted_forms) < 1:
            raise forms.ValidationError(_(u'Please specify at least one author. Use "Add author to article" button below.'))


AuthorsFormSet = inlineformset_factory(Article, ArticleAuthor, exclude=('user', 'organization', 'order'),
    extra=0, can_delete=True, can_order=True, form=AuthorForm, formset=BaseAuthorsFormSet)


class AttachForm(BootstrapForm):
    def __unicode__(self):
        def subform(fields=None, exclude=None):
            self._all_fields = self.fields
            self.fields = OrderedDict((k, v) for k, v in self.fields.items() if (True if fields is None else k in fields)
                                                                                 and (True if exclude is None else k not in exclude))
            out = self.as_div()
            self.fields = self._all_fields
            return out

        return render_to_string(u'journal/forms/article_attach.html', {
            'mainform': subform(exclude=['DELETE']),
            'subform': subform(('DELETE', 'ORDER')),
        })


class BaseAttachFormSet(BaseInlineFormSet):
    def __unicode__(self):
        return render_to_string(u'journal/forms/article_attach_formset.html', {'formset': self})

    def add_fields(self, form, index):
        super(BaseAttachFormSet, self).add_fields(form, index)
        form.fields['ORDER'].widget = forms.HiddenInput()


AttachFormSet = inlineformset_factory(Article, ArticleAttach, fields=('type', 'file', 'comment'),
    extra=0, can_delete=True, can_order=True, form=AttachForm, formset=BaseAttachFormSet)

ARTICLE_ADDING_FORMS = {
    0: (OverviewArticleForm, LocalizedArticleTitleFormSet),
    1: (NullForm, LocalizedArticleAbstractFormSet),
    2: (NullForm, AuthorsFormSet),
    3: (NullForm, AttachFormSet),
}
