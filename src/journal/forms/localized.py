from django import forms
from django.conf import settings
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string

from utils.forms import BootstrapForm


class BaseLocalizedForm(BootstrapForm):
    def __init__(self, *args, **kwargs):
        super(BaseLocalizedForm, self).__init__(*args, **kwargs)
        self.fields['lang'].widget = forms.HiddenInput()


class BaseLocalizedFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        kwargs['initial'] = kwargs.pop('initial', None) or [dict(lang=k) for k, v in settings.LANGUAGES]
        super(BaseLocalizedFormSet, self).__init__(*args, **kwargs)

    def col_md(self):
        return 12 / len(settings.LANGUAGES)

    def __unicode__(self):
        return render_to_string('journal/forms/localized.html', {
            'formset': self,
            'LANGUAGES': settings.LANGUAGES,
        })
