from django import forms

from mailauth.models import MailAuthToken
from utils.forms import BootstrapForm


class MailAuthForm(BootstrapForm):
    class Meta:
        fields = ['email']
        model = MailAuthToken

    def save(self, uri_builder):
        obj = super(MailAuthForm, self).save(commit=True)
        obj.send(uri_builder)
