from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from utils.localized import BaseLocalizedObject, BaseLocalizedContent


class Page(BaseLocalizedObject):
    order = models.PositiveIntegerField(verbose_name=_(u'Order'), blank=True, default=0)
    url = models.SlugField(db_index=True, verbose_name=_(u'URL part'), unique=True)
    in_menu = models.BooleanField(default=False, verbose_name=_(u'Visible in menu'))

    class Meta:
        ordering = ['order']
        verbose_name = _(u'Page')
        verbose_name_plural = _(u'Pages')

    def __unicode__(self):
        return self.title or self.url

    def save(self, *args, **kwargs):
        if not self.order:
            qs = self.__class__.objects.all()
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            self.order = min(2 ** 31 - 1, 1 + qs.count())
        super(Page, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return 'pages_page', [self.url]

    @property
    def title(self):
        return self.get_localized('title')

    @property
    def content(self):
        return self.get_localized('content')


class LocalizedPageContent(BaseLocalizedContent):
    page = models.ForeignKey(Page, verbose_name=Page._meta.verbose_name)

    title = models.CharField(max_length=100, verbose_name=_(u'Title'))
    content = models.TextField(default='', blank=True, verbose_name=_(u'Content'))

    class Meta:
        ordering = ['lang']
        verbose_name = _(u'Localized page content')
        verbose_name_plural = _(u'Localized page contents')
        unique_together = [('page', 'lang')]

    def __unicode__(self):
        return self.title
