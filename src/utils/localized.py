from django.db import models
from django.core.exceptions import FieldError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.models import BaseInlineFormSet
from django.template.loader import render_to_string

from utils.forms import BootstrapForm


class BaseLocalizedObject(models.Model):
    class Meta:
        abstract = True

    def get_localized(self, field_name):
        from django.utils import translation

        for relobj in self._meta.get_all_related_objects():
            if issubclass(relobj.model, BaseLocalizedContent):
                qs = relobj.model.objects.filter(**{relobj.field.name: self})
                break
        else:
            raise FieldError(u'Localized content related model not found for "%s"' % self._meta.model)

        try:
            content = qs.get(lang=translation.get_language())
        except relobj.model.DoesNotExist:
            try:
                content = qs.get(lang=settings.LANGUAGE_CODE)
            except relobj.model.DoesNotExist:
                try:
                    content = qs[0]
                except IndexError:
                    return

        return getattr(content, field_name, None)


class BaseLocalizedContent(models.Model):
    lang = models.CharField(max_length=2, choices=settings.LANGUAGES, verbose_name=_(u'Language'))

    class Meta:
        abstract = True


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
