from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.conf import settings


ARTICLE_STATUS = (
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


class BaseOrderedEntry(models.Model):
    order = models.PositiveIntegerField(verbose_name=_(u'Order'), blank=True)

    class Meta:
        abstract = True
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.order:
            lookups = {}
            for field in self._meta.fields:
                if isinstance(field, models.ForeignKey):
                    lookups[field.name, getattr(self, field.name)]
            self.order = max(2 ** 31 - 1,
                             1 + self.__class__.objects.filter(**lookups).count())
        super(BaseOrderedEntry, self).save(*args, **kwargs)


class Section(BaseOrderedEntry):
    name = models.CharField(max_length=100, verbose_name=_(u'Name'))
    moderators = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_(u'Moderators'), blank=True)

    class Meta:
        ordering = BaseOrderedEntry.Meta.ordering
        verbose_name = _(u'Section')
        verbose_name_plural = _(u'Sections')


class StaffMember(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_(u'User'))

    chief_editor = models.BooleanField(default=False, verbose_name=_(u'Chief editor'))
    editor = models.BooleanField(default=False, verbose_name=_(u'Editor'))
    reviewer = models.BooleanField(default=False, verbose_name=_(u'Reviewer'))

    def save(self, *args, **kwargs):
        if self.chief_editor:
            StaffMember.objects.filter(chief_editor=True).update(chief_editor=False)
        super(StaffMember, self).save(*args, **kwargs)


class Organization(models.Model):
    name = models.TextField(verbose_name=_(u'Name'))
    site = models.URLField(blank=True, default='', verbose_name=_(u'Site URL'))

    country = models.CharField(max_length=100, verbose_name=_(u'Country'), blank=True, default='')
    city = models.CharField(max_length=100, verbose_name=_(u'City'), blank=True, default='')
    address = models.TextField(verbose_name=_(u'Address'), default='', blank=True)

    obsolete = models.BooleanField(default=False, verbose_name=_(u'Obsolete'))
    previous = models.ManyToManyField('self', verbose_name=_(u'Previous versions'), blank=True)


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_(u'User'))
    organizations = models.ManyToManyField(Organization, through='PositionInOrganization')  # all possible user's organizations

    first_name_ru = models.CharField(_('first name'), max_length=60, blank=True)
    last_name_ru = models.CharField(_('last name'), max_length=30, blank=True)
    first_name_en = models.CharField(_('first name'), max_length=30, blank=True)
    last_name_en = models.CharField(_('last name'), max_length=30, blank=True)


class PositionInOrganization(models.Model):
    author = models.ForeignKey(Author)
    organization = models.ForeignKey(Organization)
    position = models.CharField(max_length=200)


class PersonInOrganizations(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    organizations = models.ManyToManyField(Organization, through='OrderedOrganizations')


class OrderedOrganizations(BaseOrderedEntry):
    person = models.ForeignKey(PersonInOrganizations)
    organization = models.ForeignKey(Organization)

    class Meta:
        unique_together = [('person', 'organization')]
        ordering = BaseOrderedEntry.Meta.ordering


class Article(models.Model):
    authors = models.ManyToManyField(PersonInOrganizations, through='OrderedAuthors')

    status = models.PositiveSmallIntegerField(default=0, choices=ARTICLE_STATUS)
    date_in = models.DateField(default=timezone.now)
    date_out = models.DateField(null=True, blank=True)
    old_number = models.SmallIntegerField(null=True, blank=True)

    title = models.TextField()
    abstract = models.TextField()
    content = models.TextField()
    volume = models.ForeignKey('Volume')
    sections = models.ManyToManyField('Section')


class ArticleSource(models.Model):
    article = models.ForeignKey(Article)
    file = models.FileField(upload_to='sources')


class ArticleResolution(models.Model):
    article = models.ForeignKey(Article)
    reviews = models.ManyToManyField('Review')

    status = models.PositiveSmallIntegerField(choices=RESOLUTIONS)
    text = models.TextField()
    date_created = models.DateTimeField()


class OrderedAuthors(BaseOrderedEntry):
    article = models.ForeignKey(Article)
    person_in_org = models.ForeignKey(PersonInOrganizations)

    class Meta:
        unique_together = [('article', 'person_in_org')]
        ordering = BaseOrderedEntry.Meta.ordering


class Review(models.Model):
    article = models.ForeignKey(Article)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_created = models.DateTimeField(default=timezone.now)

    comment_for_authors = models.TextField(default=u'', blank=True)
    comment_for_editors = models.TextField(default=u'', blank=True)
    resolution = models.PositiveSmallIntegerField(choices=RESOLUTIONS, default=0)

#TODO: Qualification Fields
#TODO: Organization & author moderation

class ReviewFile(models.Model):
    review = models.ForeignKey(Review)
    file = models.FileField(upload_to='reviews')


class Volume(models.Model):
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField()

    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return ugettext(u'%(title)s, %(year)s year') % self.__dict__
