from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext


ARTICLE_STATUS = ()

RESOLUTIONS = (
    (0, _(u'None')),
    (1, _(u'Reject')),
    (2, _(u'Correct')),
    (3, _(u'Publish')),
)


class BaseOrderedEntry(models.Model):
    order = models.PositiveIntegerField()

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


class Section(models.Model):
    name = models.CharField(max_length=100)
    moderators = models.ManyToManyField(get_user_model())


class StaffMember(models.Model):
    user = models.OneToOneField(get_user_model())

    chief_editor = models.BooleanField()
    reviewer = models.BooleanField()

    def save(self, *args, **kwargs):
        if self.chief_editor:
            StaffMember.objects.filter(chief_editor=True).update(chief_editor=False)
        super(StaffMember, self).save(*args, **kwargs)


class Organization(models.Model):
    name = models.TextField()
    site = models.URLField()
    address = models.TextField()

    obsolete = models.BooleanField()
    previous = models.ManyToManyField('self')


class Author(models.Model):
    user = models.OneToOneField(get_user_model())
    organizations = models.ManyToManyField(Organization)  # all possible user's organizations

    first_name_ru = models.CharField(_('first name'), max_length=60, blank=True)
    last_name_ru = models.CharField(_('last name'), max_length=30, blank=True)
    first_name_en = models.CharField(_('first name'), max_length=30, blank=True)
    last_name_en = models.CharField(_('last name'), max_length=30, blank=True)


class PersonInOrganizations(models.Model):
    user = models.ForeignKey(get_user_model())
    organizations = models.ManyToManyField(Organization, through='OrderedOrganizations')


class OrderedOrganizations(BaseOrderedEntry):
    person = models.ForeignKey(PersonInOrganizations)
    organization = models.ForeignKey(Organization)

    class Meta:
        unique_together = [('person', 'organization')]
        ordering = BaseOrderedEntry.Meta.ordering


class Article(models.Model):
    authors = models.ManyToManyField(PersonInOrganizations, through='OrderedAuthors')
    
    status = models.SmallIntegerField(default=0, choices=ARTICLE_STATUS)
    date_in = models.DateField(default=timezone.now)
    date_out = models.DateField(null=True, blank=True)
    old_number = models.SmallIntegerField(null=True, blank=True)

    title = models.TextField()
    abstract = models.TextField()
    content = models.TextField()


class ArticleSource(models.Model):
    article = models.ForeignKey(Article)
    file = models.FileField(upload_to='sources')


class OrderedAuthors(BaseOrderedEntry):
    article = models.ForeignKey(Article)
    person_in_org = models.ForeignKey(PersonInOrganizations)

    class Meta:
        unique_together = [('article', 'person_in_org')]
        ordering = BaseOrderedEntry.Meta.ordering


class Review(models.Model):
    article = models.ForeignKey(Article)
    reviewer = models.ForeignKey(get_user_model())
    date_created = models.DateTimeField(default=timezone.now)

    text = models.TextField(default=u'', blank=True)
    resolution = models.PositiveSmallIntegerField(choices=RESOLUTIONS, default=0)


class Volume(models.Model):
    #articles - m2m -?
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField()

    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return ugettext(u'%(title)s, %(year)s year') % self.__dict__
