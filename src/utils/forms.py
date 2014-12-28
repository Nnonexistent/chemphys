from types import MethodType
from django import forms


class BootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs['label_suffix'] = kwargs.pop('label_suffix', '')
        super(BootstrapForm, self).__init__(*args, **kwargs)
        self.required_css_class = 'form-required'

    def __getitem__(self, name):
        bf = super(BootstrapForm, self).__getitem__(name)
        if not hasattr(bf.css_classes, '_expanded'):
            old_func = bf.css_classes
            def css_classes(self, *args, **kwargs):
                out = old_func(*args, **kwargs).split()
                out.append('form-group')
                return u' '.join(set(out))
            css_classes._expanded = True
            bf.css_classes = MethodType(css_classes, 'css_classes', type(bf))
        return bf

    def __unicode__(self):
        return self.as_div()

    def as_div(self):
        for field in self.fields.itervalues():
            if isinstance(field, forms.BooleanField):
                continue
            attrs = field.widget.attrs
            css_classes = attrs.get('class', '').split()
            if 'form-control' not in css_classes:
                css_classes.append('form-control')
                attrs['class'] = u' '.join(set(css_classes))
        return self._html_output(
            normal_row='<div%(html_class_attr)s>%(errors)s %(label)s %(field)s%(help_text)s</div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <p class="helptext">%s</p>',
            errors_on_separate_row=False)
