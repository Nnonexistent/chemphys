import json
from collections import OrderedDict

from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from journal.models import Review, ReviewField
from utils.forms import BootstrapForm


REVIEWFORM_FIELDS = ('comment_for_authors', 'comment_for_editors', 'resolution')


class ReviewForm(BootstrapForm):
    class Meta:
        model = Review
        fields = REVIEWFORM_FIELDS

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['resolution'].widget.choices[0] = (0, _(u'Undecided yet (complete review afterwards)'))
        for field in ReviewField.objects.all():
            self.fields['field_%s' % field.id] = field.formfield()

    def __unicode__(self):
        def subform(fields=None, exclude=None):
            self._all_fields = self.fields
            self.fields = OrderedDict((k, v) for k, v in self.fields.items() if (True if fields is None else k in fields)
                                                                                 and (True if exclude is None else k not in exclude))
            out = self.as_div()
            self.fields = self._all_fields
            return out

        return render_to_string(u'journal/forms/review.html', {
            'mainform': subform(REVIEWFORM_FIELDS),
            'fieldsform': subform(exclude=REVIEWFORM_FIELDS),
        })

    def save(self, commit=True):
        obj = super(ReviewForm, self).save(commit=False)
        data = []
        for field in ReviewField.objects.all():
            data.append((field.id, field.name, field.field_type, self.cleaned_data['field_%s' % field.id]))
        obj.field_values = json.dumps(data)

        if self.cleaned_data['resolution'] != 0:
            obj.status = 2
        else:
            obj.status = 1

        if commit:
            obj.save()
