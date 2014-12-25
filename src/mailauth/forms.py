from django import forms

from mailauth.models import MailAuthToken


class MailAuthForm(forms.ModelForm):
    class Meta:
        fields = ['email']
        model = MailAuthToken

    def save(self, uri_builder):
        obj = super(MailAuthForm, self).save(commit=True)
        obj.send(uri_builder)
