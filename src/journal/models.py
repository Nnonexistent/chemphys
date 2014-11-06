from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.conf import settings


ARTICLE_STATUSES = (
    (0, _(u'New')),
    (1, _(u'Rejected')),
    (2, _(u'In review')),
    (3, _(u'Reviewed')),
    (10, _(u'Published')),
    (5, _(u'In rework')),
)
REVIEW_STATUSES = (
    (0, _(u'Pending')),
    (1, _(u'Unfinished')),
    (2, _(u'Done')),
)
RESOLUTIONS = (
    (0, _(u'None')),
    (1, _(u'Rejected')),
    (2, _(u'Rework required')),
    (3, _(u'Approved')),
)
MODERATION_STATUSES = (
    (0, _(u'New')),
    (1, _(u'Rejected')),
    (2, _(u'Approved')),
)
REVIEW_FIELD_TYPES = (
    (0, _(u'Header')),
    (1, _(u'Choices field')),
    (2, _(u'Text string')),
    (3, _(u'Text field')),
    (4, _(u'Checkbox')),
)
LANG_CODES = (
    ('ru', _('Russian')),
    ('en', _('English')),
)

class ModeratedObject(models.Model):
    moderation_status = models.PositiveSmallIntegerField(choices=MODERATION_STATUSES, default=0, verbose_name=_(u'Moderation status'))

    class Meta:
        abstract = True


class OrderedEntry(models.Model):
    order = models.PositiveIntegerField(verbose_name=_(u'Order'), blank=True, default=0)
    _order_lookup_field = None

    class Meta:
        abstract = True
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.order:
            if self._order_lookup_field:
                lookups = {self._order_lookup_field: getattr(self, self._order_lookup_field)}
            else:
                lookups = {}
            qs = self.__class__.objects.filter(**lookups)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            self.order = min(2 ** 31 - 1, 1 + qs.count())
        super(OrderedEntry, self).save(*args, **kwargs)


class Section(OrderedEntry):
    name = models.CharField(max_length=100, verbose_name=_(u'Name'))
    moderators = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_(u'Moderators'), blank=True)

    class Meta:
        ordering = OrderedEntry.Meta.ordering
        verbose_name = _(u'Section')
        verbose_name_plural = _(u'Sections')

    def __unicode__(self):
        return self.name


class StaffMember(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_(u'User'))

    chief_editor = models.BooleanField(default=False, verbose_name=_(u'Chief editor'))
    editor = models.BooleanField(default=False, verbose_name=_(u'Editor'))
    reviewer = models.BooleanField(default=False, verbose_name=_(u'Reviewer'))

    class Meta:
        ordering = ('chief_editor', 'editor', 'reviewer', 'user__last_name')
        verbose_name = _(u'Staff member')
        verbose_name_plural = _(u'Staff members')

    def save(self, *args, **kwargs):
        if self.chief_editor:
            StaffMember.objects.filter(chief_editor=True).update(chief_editor=False)
        super(StaffMember, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.get_full_name() or self.user.username


class Organization(ModeratedObject):
    name = models.TextField(verbose_name=_(u'Name'))
    alt_names = models.TextField(verbose_name=_(u'Alternative names'), help_text=_(u'one per line'), default='', blank=True)

    site = models.URLField(blank=True, default='', verbose_name=_(u'Site URL'))
    country = models.CharField(max_length=100, verbose_name=_(u'Country'), blank=True, default='')
    city = models.CharField(max_length=100, verbose_name=_(u'City'), blank=True, default='')
    address = models.TextField(verbose_name=_(u'Address'), default='', blank=True)

    obsolete = models.BooleanField(default=False, verbose_name=_(u'Obsolete'))
    previous = models.ManyToManyField('self', verbose_name=_(u'Previous versions'), blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Organization')
        verbose_name_plural = _(u'Organizations')

    def __unicode__(self):
        return self.name


class Author(ModeratedObject):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_(u'User'))

    class Meta:
        ordering = ('user__last_name', 'user__first_name')
        verbose_name = _(u'Author')
        verbose_name_plural = _(u'Authors')

    def __unicode__(self):
        return self.user.get_full_name() or self.user.username


class LocalizedName(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u'User'))
    lang = models.CharField(max_length=2, choices=LANG_CODES, verbose_name=_(u'Language'))
    first_name = models.CharField(_('first name'), max_length=60, blank=True)
    last_name = models.CharField(_('last name'), max_length=60, blank=True)

    class Meta:
        ordering = ('user', 'lang')
        verbose_name = _(u'Localized name')
        verbose_name_plural = _(u'Localized names')
        unique_together = [('user', 'lang')]

    def __unicode__(self):
        return (u'%s %s' % (self.last_name, self.first_name)) or self.user.username

    def save(self, *args, **kwargs):
        super(LocalizedName, self).save(*args, **kwargs)
        if self.lang == settings.LANGUAGE_CODE:
            self.user.last_name = self.last_name
            self.user.first_name = self.first_name
            self.user.save(update_fields=('last_name', 'first_name'))


class PositionInOrganization(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u'User'))
    position = models.CharField(max_length=200, verbose_name=_(u'Position'))
    organization = models.ForeignKey(Organization, verbose_name=_(u'Organization'))

    class Meta:
        ordering = ['id']
        verbose_name = _(u'Position in organization')
        verbose_name_plural = _(u'Position in organizations')

    def __unicode__(self):
        return u'%s (%s, %s)' % (self.user.get_full_name() or self.user, self.position, self.organization)


class Article(models.Model):
    status = models.PositiveSmallIntegerField(default=0, choices=ARTICLE_STATUSES, verbose_name=_(u'Status'))
    date_in = models.DateTimeField(default=timezone.now, verbose_name=_(u'Date in'))
    date_published = models.DateTimeField(null=True, blank=True, verbose_name=_(u'Publish date'))
    old_number = models.SmallIntegerField(null=True, blank=True, verbose_name=_(u'Old number'), help_text=_(u'to link consistency with old articles'))

    title = models.TextField(verbose_name=_(u'Title'))
    abstract = models.TextField(verbose_name=_(u'Abstract'))
    content = models.FileField(verbose_name=_(u'Content'), upload_to='published', default='', blank=True)

    volume = models.ForeignKey('Volume', null=True, blank=True)
    sections = models.ManyToManyField('Section', blank=True)

    class Meta:
        ordering = ['date_in']
        verbose_name = _(u'Article')
        verbose_name_plural = _(u'Articles')

    def __unicode__(self):
        return self.title

    def get_authors(self):
        authors = []
        for aa in self.articleauthor_set.all():
            user = aa.position.user
            if user not in authors:
                authors.append(user)
        return authors


class ArticleAuthor(OrderedEntry):
    article = models.ForeignKey(Article, verbose_name=Article._meta.verbose_name)
    position = models.ForeignKey(PositionInOrganization, verbose_name=_(u'Author'))

    _order_lookup_field = 'article'

    class Meta:
        verbose_name = _(u'Article author')
        verbose_name_plural = _(u'Article authors')
        ordering = OrderedEntry.Meta.ordering
        unique_together = [('article', 'position')]

    def __unicode__(self):
        return unicode(self.position)
    

class ArticleSource(models.Model):
    article = models.ForeignKey(Article, verbose_name=Article._meta.verbose_name)

    date_created = models.DateTimeField(default=timezone.now, verbose_name=_(u'Date created'))
    file = models.FileField(upload_to='sources', verbose_name=_(u'File'))
    comment = models.TextField(default='', blank=True, verbose_name=_(u'Staff comment'))

    class Meta:
        ordering = ['date_created']
        verbose_name = _(u'Article source')
        verbose_name_plural = _(u'Article sources')

    def __unicode__(self):
        return _(u'Source of %s') % self.article


class ArticleResolution(models.Model):
    article = models.ForeignKey(Article, verbose_name=Article._meta.verbose_name)

    date_created = models.DateTimeField(default=timezone.now, verbose_name=_(u'Date created'))
    reviews = models.ManyToManyField('Review', verbose_name=_(u'Reviews'))
    status = models.PositiveSmallIntegerField(choices=RESOLUTIONS, verbose_name=_(u'Status'))
    text = models.TextField(verbose_name=_(u'Text'))

    class Meta:
        ordering = ['date_created']
        verbose_name = _(u'Article resolution')
        verbose_name_plural = _(u'Article resolutions')

    def __unicode__(self):
        return _(u'Resolution for %s') % self.article


class ReviewField(OrderedEntry):
    field_type = models.PositiveSmallIntegerField(choices=REVIEW_FIELD_TYPES, verbose_name=_(u'Field type'))
    name = models.CharField(max_length=64, verbose_name=_(u'Name'))
    description = models.TextField(default='', blank=True, verbose_name=_(u'Description'))
    choices = models.TextField(default='', blank=True, verbose_name=_(u'Choices'))

    class Meta:
        ordering = OrderedEntry.Meta.ordering
        verbose_name = _(u'Review field')
        verbose_name_plural = _(u'Review fields')

    def __unicode__(self):
        return self.name


class Review(models.Model):
    article = models.ForeignKey(Article, verbose_name=Article._meta.verbose_name)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u'Reviewer'))
    status = models.PositiveSmallIntegerField(choices=REVIEW_STATUSES, default=0, verbose_name=_(u'Status'))
    date_created = models.DateTimeField(default=timezone.now, verbose_name=_(u'Created'))

    field_values = models.TextField(default='', editable=False, verbose_name=_(u'Field values'))

    comment_for_authors = models.TextField(default=u'', blank=True, verbose_name=_(u'Comment for authors'))
    comment_for_editors = models.TextField(default=u'', blank=True, verbose_name=_(u'Comment for editors'))
    resolution = models.PositiveSmallIntegerField(choices=RESOLUTIONS, default=0, verbose_name=_(u'Resolution'))

    # TODO: review - article versioning?

    class Meta:
        ordering = ['date_created']
        verbose_name = _(u'Review')
        verbose_name_plural = _(u'Reviews')

    def __unicode__(self):
        return _(u'Review for %s') % self.article


class ReviewFile(models.Model):
    review = models.ForeignKey(Review, verbose_name=Review._meta.verbose_name)
    file = models.FileField(upload_to='reviews', verbose_name=_(u'File'))
    comment = models.TextField(default='', blank=True, verbose_name=_(u'Comment'))

    class Meta:
        ordering = ['id']
        verbose_name = _(u'Review file')
        verbose_name_plural = _(u'Review files')

    def unicode(self):
        return _(u'File for review for %s') % self.review.article


class Volume(OrderedEntry):
    title = models.CharField(max_length=100, verbose_name=_(u'Title'))
    year = models.PositiveIntegerField(verbose_name=_(u'Year'))

    class Meta:
        verbose_name = _(u'Volume')
        verbose_name_plural = _(u'Volumes')
        ordering = ['order']

    def __unicode__(self):
        return ugettext(u'%(title)s, %(year)s year') % self.__dict__

    @models.permalink
    def get_absolute_url(self):
        return 'show_volume', [self.id]
