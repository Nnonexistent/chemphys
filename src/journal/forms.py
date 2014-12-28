from collections import OrderedDict

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.translation import ugettext as _

from utils.forms import BootstrapForm
from journal.models import Author, LocalizedName, LocalizedUser, PositionInOrganization, Organization


class AuthorEditForm(BootstrapForm):
    class Meta:
        model = get_user_model()
        fields = ['email']


class LocalizedNameForm(BootstrapForm):
    class Meta:
        model = LocalizedName

    def __init__(self, *args, **kwargs):
        kwargs['label_suffix'] = kwargs.pop('label_suffix', '')
        super(LocalizedNameForm, self).__init__(*args, **kwargs)
        self.fields['lang'].widget = forms.HiddenInput()


class BaseLocalizedNameFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        kwargs['initial'] = kwargs.pop('initial', None) or [dict(lang=k) for k, v in settings.LANGUAGES]
        super(BaseLocalizedNameFormSet, self).__init__(*args, **kwargs)

    def col_lg(self):
        return 8 / len(settings.LANGUAGES)

    def col_md(self):
        return 12 / len(settings.LANGUAGES)


LocalizedNameFormSet = inlineformset_factory(LocalizedUser, LocalizedName,
    extra=len(settings.LANGUAGES), max_num=len(settings.LANGUAGES), can_delete=False,
    form=LocalizedNameForm, formset=BaseLocalizedNameFormSet)


class PIOForm(BootstrapForm):
    def __init__(self, *args, **kwargs):
        super(PIOForm, self).__init__(*args, **kwargs)
        self.fields = OrderedDict([('new_org', forms.CharField(label=_(u'Organization title'), required=False))] + self.fields.items())
        self.fields['organization'].queryset = Organization.objects.filter(moderation_status=2, obsolete=False)
        self.fields['organization'].widget = forms.TextInput()


PIOFormSet = inlineformset_factory(LocalizedUser, PositionInOrganization,
    extra=0, can_delete=True, form=PIOForm)
