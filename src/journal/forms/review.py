from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from journal.models import Review, ReviewFile, ReviewField
from utils.forms import BootstrapForm


class ReviewForm(BootstrapForm):
    class Meta:
        model = Review
        fields = ('comment_for_authors', 'comment_for_editors', 'resolution')


ReviewFileFormSet = inlineformset_factory(Review, ReviewFile, fields=('file', 'comment'),
    form=BootstrapForm, extra=0, can_delete=True)
