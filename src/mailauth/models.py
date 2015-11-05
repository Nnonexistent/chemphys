import uuid

from django.db import models
from django.db.utils import OperationalError
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.checks import register, Error
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string


def default_key():
    return uuid.uuid4().hex


class MailAuthToken(models.Model):
    key = models.CharField(max_length=32, verbose_name=_(u'Key'), unique=True, default=default_key)
    email = models.EmailField(verbose_name=_('E-mail'))
    created = models.DateTimeField(verbose_name=_(u'Created'), default=timezone.now)

    class Meta:
        verbose_name = _(u'Mail auth token')
        verbose_name_plural = _(u'Mail auth tokens')

    @models.permalink
    def get_absolute_url(self):
        return 'mailauth_auth', [self.key]

    def save(self, *args, **kwargs):
        if not self.id:
            while MailAuthToken.objects.filter(key=self.key).exists():
                self.key = self._meta.get_field('key').default()
        super(MailAuthToken, self).save(*args, **kwargs)

    def send(self, uri_builder):
        msg = render_to_string('journal/mail/auth.txt', {'link': uri_builder(self.get_absolute_url())})
        send_mail(_('Journal authentication'), msg, settings.DEFAULT_FROM_EMAIL, [self.email], fail_silently=False)


@register()
def email_uniqueness_check(app_configs, **kwargs):
    errors = []
    try:
        emails = list(get_user_model().objects.all().exclude(email='').values_list('email'))
    except OperationalError:
        return []  # Database not ready - skip checking
    unique_emails = []
    for email in emails:
        if email in unique_emails:
            errors.append(Error('Duplicated emails', obj=email, id='mailauth.E001'))
        unique_emails.append(email)
    return errors

# TODO: tokens expiration, cleanup
