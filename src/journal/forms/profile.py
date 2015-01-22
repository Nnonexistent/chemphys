from collections import OrderedDict
from itertools import chain

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.translation import ugettext as _
from django.db import transaction

from utils.forms import BootstrapForm
from utils.localized import BaseLocalizedForm, BaseLocalizedFormSet
from journal.models import Author, LocalizedName, LocalizedUser, PositionInOrganization, Organization, OrganizationLocalizedContent


class AuthorEditForm(BootstrapForm):
    degree = Author._meta.get_field('degree').formfield()

    class Meta:
        model = LocalizedUser
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(AuthorEditForm, self).__init__(*args, **kwargs)
        try:
            self.fields['degree'].initial = self.instance.author.degree
        except Author.DoesNotExist:
            pass

    def save(self, commit=True):
        obj = super(AuthorEditForm, self).save(commit)
        author, new = Author.objects.get_or_create(user=obj)
        author.degree = self.cleaned_data.get('degree')
        author.save()
        return obj


LocalizedNameFormSet = inlineformset_factory(LocalizedUser, LocalizedName,
    extra=len(settings.LANGUAGES), max_num=len(settings.LANGUAGES), can_delete=False,
    form=BaseLocalizedForm, formset=BaseLocalizedFormSet)


class PIOForm(BootstrapForm):
    _org_loc_fields = ('name', 'country', 'city', 'address')
    _org_fields = ('site', )

    organization = PositionInOrganization._meta.get_field('organization').formfield(required=False, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(PIOForm, self).__init__(*args, **kwargs)
        choices = [('', _(u'Add new organization'))]

        org = None
        if self.instance.id:
            org = self.instance.organization
            self.fields['organization'].initial = org
            choices.append((org.id, unicode(org)))

        key = u'%s-organization' % self.prefix
        if self.data.get(key):
            try:
                org = Organization.objects.get(id=int(self.data[key]))
            except ValueError:
                pass
            else:
                choices.append((org.id, unicode(org)))

        self.fields['organization'].widget.choices = choices

        for key, field in chain(self.iter_org_fields(), self.iter_loc_fields()):
            self.fields[key] = field.formfield(required=False)

        self._all_fields = self.fields

    def clean(self):
        if not self.cleaned_data.get('organization') and not self._errors.get('organization'):  # new organization
            for key, field in self.iter_org_fields():
                if not field.blank and not self.cleaned_data.get(key):
                    self._errors.setdefault(key, []).append(_(u'This field is required if new organization specified.'))

            all_empty = True
            for lang_code, lang_name in settings.LANGUAGES:
                empty = True
                errors = []
                for key, field in self.iter_loc_fields(lang_code=lang_code):
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
        if self.cleaned_data.get('organization'):
            org = self.cleaned_data.get('organization')
        else:
            kwargs = {}
            for key, field in self.iter_org_fields():
                kwargs[field.name] = self.cleaned_data[key]
            org = Organization.objects.create(**kwargs)

            for lang_code, lang_name in settings.LANGUAGES:
                kwargs = {}
                for key, field in self.iter_loc_fields(lang_code=lang_code):
                    kwargs[field.name] = self.cleaned_data[key]
                if any(kwargs.values()):  # don't save empty localized data
                    OrganizationLocalizedContent.objects.create(org=org, lang=lang_code, **kwargs)

        pio = super(PIOForm, self).save(commit=False)
        pio.organization = org
        pio.save()
        return pio

    def iter_org_fields(self):
        for field in Organization._meta.fields:
            if field.name in self._org_fields:
                key = u'org_%s' % field.name
                yield key, field

    def iter_loc_fields(self, lang_code=None):
        if lang_code == None:
            langs = settings.LANGUAGES
        else:
            langs = [(lang_code, u'')]

        for lang_code, lang_name in langs:
            for field in OrganizationLocalizedContent._meta.fields:
                if field.name in self._org_loc_fields:
                    key = u'%s_%s' % (lang_code, field.name)
                    yield key, field

    def as_div_common(self):
        self.fields = OrderedDict((k, v) for k, v in self.fields.items() if k not in dict(chain(self.iter_loc_fields(), self.iter_org_fields())))

        # make delete field first
        n = len(self._org_fields) + len(set(self._meta.fields))
        self.fields = OrderedDict(self.fields.items()[n:] + self.fields.items()[:n])
        self.fields['DELETE'].extra_classes = ['pull-right']

        out = self.as_div()
        self.fields = self._all_fields
        return out

    def as_div_org(self):
        self.fields = OrderedDict((k, v) for k, v in self.fields.items() if k in dict(self.iter_org_fields()))
        out = self.as_div()
        self.fields = self._all_fields
        return out

    def as_div_lang(self):
        # FIXME: simplify, see article authors formset form
        def factory(lang_code):
            def inner():
                self.fields = OrderedDict((k, v) for k, v in self.fields.items() if k in dict(self.iter_loc_fields(lang_code=lang_code)))
                out = self.as_div()
                self.fields = self._all_fields
                return out
            return inner

        out = []
        for lang_code, lang_name in settings.LANGUAGES:
            out.append({'render': factory(lang_code), 'lang': lang_code, 'col_md': 12 / len(settings.LANGUAGES)})
        return out


class BasePIOFormSet(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        orgs = []
        for form in self.forms:
            org = form.cleaned_data.get('organization')
            if org is not None and org in orgs:
                form._errors.setdefault('organization', []).append(_(u'This organization is already used.'))
            orgs.append(org)


PIOFormSet = inlineformset_factory(LocalizedUser, PositionInOrganization, fields=['position'],
    extra=0, can_delete=True, form=PIOForm, formset=BasePIOFormSet)


