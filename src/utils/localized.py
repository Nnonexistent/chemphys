from django.db import models
from django.core.exceptions import FieldError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


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
