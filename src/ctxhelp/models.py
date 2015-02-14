from django.db import models
from django.conf import settings


class HiddenHelp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    hash = models.CharField(max_length=40)

    class Meta:
        pass
        unique_together = ('user', 'hash')
