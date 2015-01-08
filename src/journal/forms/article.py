from django import forms
from django.conf import settings
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext as _

from utils.forms import BootstrapForm, NullForm
from utils.localized import BaseLocalizedForm, BaseLocalizedFormSet
from journal.models import Article, LocalizedArticleContent


class OverviewArticleForm(BootstrapForm):
    class Meta:
        model = Article
        fields = ('sections', 'image')

    def __init__(self, *args, **kwargs):
        super(OverviewArticleForm, self).__init__(*args, **kwargs)
        self.fields['sections'].help_text = ''
        self.fields['sections'].widget = forms.CheckboxSelectMultiple(choices=self.fields['sections'].widget.choices)


LocalizedArticleTitleFormSet = inlineformset_factory(Article, LocalizedArticleContent,
    fields=('lang', 'title'), extra=len(settings.LANGUAGES), max_num=len(settings.LANGUAGES),
    can_delete=False, form=BaseLocalizedForm, formset=BaseLocalizedFormSet)


LocalizedArticleAbstractFormSet = inlineformset_factory(Article, LocalizedArticleContent,
    fields=('lang', 'abstract', 'keywords', 'references'), extra=len(settings.LANGUAGES), max_num=len(settings.LANGUAGES),
    can_delete=False, form=BaseLocalizedForm, formset=BaseLocalizedFormSet)


ARTICLE_ADDING_FORMS = {
    0: (OverviewArticleForm, LocalizedArticleTitleFormSet),
    1: (NullForm, LocalizedArticleAbstractFormSet),
    2: (NullForm, NullForm),
    3: (NullForm, NullForm),
}
