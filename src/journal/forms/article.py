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
from journal.models import Article, LocalizedArticleContent, ArticleSource, ArticleAuthor, LocalizedUser, LocalizedName, Organization, OrganizationLocalizedContent, Author, ArticleAttach


class OverviewArticleForm(BootstrapForm):
    class Meta:
        model = Article
        fields = ('type', 'sections', 'image')

    def __init__(self, *args, **kwargs):
        super(OverviewArticleForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget = forms.RadioSelect(choices=self.fields['type'].choices)
        self.fields['sections'].help_text = ''
        self.fields['sections'].widget = forms.CheckboxSelectMultiple(choices=self.fields['sections'].widget.choices)
        try:
            initial_file = self.instance.articlesource_set.latest().file
        except ArticleSource.DoesNotExist:
            initial_file = None
        self.fields['file'] = forms.FileField(label=_(u'Article file'), required=True, initial=initial_file)

    def save(self, commit=True):
        obj = super(OverviewArticleForm, self).save(commit)
        # We believe article is already has an id
        if self.files.get('file'):
            obj.articlesource_set.add(ArticleSource.objects.create(article=obj, file=self.files['file']))
        return obj


LocalizedArticleTitleFormSet = inlineformset_factory(Article, LocalizedArticleContent,
    fields=('lang', 'title'), extra=len(settings.LANGUAGES), max_num=len(settings.LANGUAGES),
    can_delete=False, form=BaseLocalizedForm, formset=BaseLocalizedFormSet)


LocalizedArticleAbstractFormSet = inlineformset_factory(Article, LocalizedArticleContent,
    fields=('lang', 'abstract', 'keywords', 'references'), extra=len(settings.LANGUAGES), max_num=len(settings.LANGUAGES),
    can_delete=False, form=BaseLocalizedForm, formset=BaseLocalizedFormSet)


class AuthorForm(BootstrapForm):
    _org_fields = ('site', )
    _org_loc_fields = ('name', 'country', 'city', 'address')
    _user_fields = ('email', )
    _user_loc_fields = ('first_name', 'last_name')

    author = ArticleAuthor._meta.get_field('author').formfield(required=False, widget=forms.Select)
    organization = ArticleAuthor._meta.get_field('organization').formfield(required=False, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)

        # user
        user = None
        if self.instance.id:
            user = self.instance.author
            self.fields['author'].initial = user
        else:
            key = self.add_prefix(u'author')
            if self.data.get(key):
                try:
                    user = LocalizedUser.objects.get(id=int(self.data[key]))
                except ValueError:
                    pass
        if user:
            choices = [(user.id, unicode(user))]
        else:
            choices = [('', _(u'Add new author'))]

        self.fields['author'].widget.choices = choices

        for key, field in chain(self.iter_user_fields(), self.iter_user_loc_fields()):
            self.fields[key] = field.formfield(required=False)

        # organization
        org = None
        if self.instance.id:
            org = self.instance.organization
            self.fields['organization'].initial = org
        else:
            key = self.add_prefix(u'organization')
            if self.data.get(key):
                try:
                    org = Organization.objects.get(id=int(self.data[key]))
                except ValueError:
                    pass

        if org:
            choices = [(org.id, unicode(org))]
        else:
            choices = [('', _(u'Add new organization'))]

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
        for field in LocalizedUser._meta.fields:
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

    # TODO: e-mail duplication check

    # TODO: restrict self deletion

    # TODO: fetch organization initial choices from user's profile

    # TODO: check users uniqueness

    def clean(self):
        # TODO: only one of all lang fields is required, not all
        if not self.cleaned_data.get('author') and not self._errors.get('author'):
            for key, field in chain(self.iter_user_fields(), self.iter_user_loc_fields()):
                # email is explicitly required because LocalizedUser is just a proxy model
                # but user e-mail required for authentication in our project
                if (not field.blank or field.name == 'email') and not self.cleaned_data.get(key):
                    self._errors.setdefault(key, []).append(_(u'This field is required if new author specified.'))

        if not self.cleaned_data.get('organization') and not self._errors.get('organization'):
            for key, field in chain(self.iter_org_fields(), self.iter_org_loc_fields()):
                if not field.blank and not self.cleaned_data.get(key):
                    self._errors.setdefault(key, []).append(_(u'This field is required if new organization specified.'))
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
            # TODO: re-check e-mail duplication
            # TODO: improve username (len(User.username) <= 30 and len(User.email) <= 75)
            author = LocalizedUser.objects.create(username=kwargs['email'], **kwargs)
            Author.objects.create(user=author)

            for lang_code, lang_name in settings.LANGUAGES:
                kwargs = {'user': author, 'lang': lang_code}
                for key, field in self.iter_user_loc_fields(lang_code=lang_code):
                    kwargs[field.name] = self.cleaned_data[key]
                LocalizedName.objects.create(**kwargs)

        # organization
        if self.cleaned_data.get('organization'):
            org = self.cleaned_data.get('organization')
        else:
            kwargs = {}
            for key, field in self.iter_org_fields():
                kwargs[field.name] = self.cleaned_data[key]
            org = Organization.objects.create(**kwargs)

            for lang_code, lang_name in settings.LANGUAGES:
                kwargs = {'org': org, 'lang': lang_code}
                for key, field in self.iter_org_loc_fields(lang_code=lang_code):
                    kwargs[field.name] = self.cleaned_data[key]
                OrganizationLocalizedContent.objects.create(**kwargs)

        aa = super(AuthorForm, self).save(commit=False)
        aa.organization = org
        aa.author = author
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
            'user_mainform': subform(('author', '')) + subform(*self.iter_user_fields()),
            'org_mainform': subform(('organization', '')) + subform(*self.iter_org_fields()),
            'user_subforms': user_subforms,
            'org_subforms': org_subforms,
        })


class BaseAuthorsFormSet(BaseInlineFormSet):
    def __unicode__(self):
        return render_to_string(u'journal/forms/article_author_formset.html', {'formset': self})

    def add_fields(self, form, index):
        super(BaseAuthorsFormSet, self).add_fields(form, index)
        form.fields['ORDER'].widget = forms.HiddenInput()


AuthorsFormSet = inlineformset_factory(Article, ArticleAuthor, exclude=('author', 'organization', 'order'),
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
