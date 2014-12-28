from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from utils.forms import BootstrapForm
from journal.models import Author, LocalizedName, LocalizedUser


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

    def col_n(self):
        return 12 / len(settings.LANGUAGES)


LocalizedNameFormSet = inlineformset_factory(LocalizedUser, LocalizedName,
    extra=len(settings.LANGUAGES), max_num=len(settings.LANGUAGES), can_delete=False,
    form=LocalizedNameForm, formset=BaseLocalizedNameFormSet)

