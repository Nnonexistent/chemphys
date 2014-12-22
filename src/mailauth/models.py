import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings


class MailAuthToken(models.Model):
    key = models.CharField(max_length=64, verbose_name=_(u'Key'), unique=True, default=lambda: uuid.uuid4().hex)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u'User'))
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _(u'Mail auth token')
        verbose_name_plural = _(u'Mail auth tokens')

    def save(self, *args, **kwargs):
        if not self.id:
            while MailAuthToken.object.filter(key=self.key).exists():
                self.key = self._meta.get_field('key').default()
        super(MailAuthToken, self).save(*args, **kwargs)
