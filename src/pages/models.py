from django.db import models
from django.utils.translation import ugettext as _


class Page(models.Model):
    order = models.PositiveIntegerField(verbose_name=_(u'Order'), blank=True, default=0)
    title = models.CharField(max_length=100, verbose_name=_(u'Title'))
    url = models.SlugField(db_index=True, verbose_name=_(u'URL part'), unique=True)
    content = models.TextField(default='', blank=True, verbose_name=_(u'Content'))
    in_menu = models.BooleanField(default=False, verbose_name=_(u'Visible in menu'))

    class Meta:
        ordering = ['order']
        verbose_name = _(u'Page')
        verbose_name_plural = _(u'Pages')

    def __unicode__(self):
        return self.title

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
