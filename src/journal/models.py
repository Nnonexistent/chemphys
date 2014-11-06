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
    (4, _(u'Published')),
    (5, _(u'In rework')),
)
RESOLUTIONS = (
    (0, _(u'None')),
    (1, _(u'Reject')),
    (2, _(u'Correct')),
    (3, _(u'Publish')),
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

    class Meta:
        abstract = True
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.order:
            # FIXME: check if we really need to construct lookup from all fk's
            lookups = {}
            for field in self._meta.fields:
                if isinstance(field, models.ForeignKey):
                    lookups[field.name, getattr(self, field.name)]
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
        return u'%s (%s)' % (self.position, self.organization)


class PersonInOrganizations(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    organizations = models.ManyToManyField(Organization, through='OrderedOrganizations')


class OrderedOrganizations(OrderedEntry):
    person = models.ForeignKey(PersonInOrganizations)
    organization = models.ForeignKey(Organization)

    class Meta:
        unique_together = [('person', 'organization')]
        ordering = OrderedEntry.Meta.ordering


class Article(models.Model):
    authors = models.ManyToManyField(PersonInOrganizations, through='OrderedAuthors')

    status = models.PositiveSmallIntegerField(default=0, choices=ARTICLE_STATUSES)
    date_in = models.DateField(default=timezone.now)
    date_out = models.DateField(null=True, blank=True)
    old_number = models.SmallIntegerField(null=True, blank=True)

    title = models.TextField()
    abstract = models.TextField()
    content = models.TextField()
    volume = models.ForeignKey('Volume', null=True, blank=True)
    sections = models.ManyToManyField('Section')


class ArticleSource(models.Model):
    article = models.ForeignKey(Article)
    file = models.FileField(upload_to='sources')
    comment = models.TextField(default='', blank=True, verbose_name=_(u'Staff comment'))


class ArticleResolution(models.Model):
    article = models.ForeignKey(Article)
    reviews = models.ManyToManyField('Review')

    date_created = models.DateTimeField(default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=RESOLUTIONS)
    text = models.TextField()

    class Meta:
        ordering = ['date_created', ]
    

class OrderedAuthors(OrderedEntry):
    article = models.ForeignKey(Article)
    person_in_org = models.ForeignKey(PersonInOrganizations)

    class Meta:
        unique_together = [('article', 'person_in_org')]
        ordering = OrderedEntry.Meta.ordering


class ReviewField(OrderedEntry):
    field_type = models.PositiveSmallIntegerField(choices=REVIEW_FIELD_TYPES)
    name = models.CharField(max_length=64)
    description = models.TextField(default='', blank=True)
    choices = models.TextField(default='', blank=True)


class Review(models.Model):
    article = models.ForeignKey(Article)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_created = models.DateTimeField(default=timezone.now)

    field_values = models.TextField(default='', editable=False)

    comment_for_authors = models.TextField(default=u'', blank=True)
    comment_for_editors = models.TextField(default=u'', blank=True)
    resolution = models.PositiveSmallIntegerField(choices=RESOLUTIONS, default=0)


class ReviewFile(models.Model):
    review = models.ForeignKey(Review)
    file = models.FileField(upload_to='reviews')


class Volume(OrderedEntry):
    title = models.CharField(max_length=100, verbose_name=_(u'Title'))
    year = models.PositiveIntegerField(verbose_name=_(u'Year'))

    class Meta:
        verbose_name = _(u'Volume')
        verbose_name_plural = _(u'Volumes')
        ordering = ['order']

    def __unicode__(self):
        return ugettext(u'%(title)s, %(year)s year') % self.__dict__
