import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.conf import settings
from django.core.urlresolvers import reverse

from utils.localized import BaseLocalizedObject, BaseLocalizedContent


ARTICLE_STATUSES = (
    (0, _(u'Adding / Overview')),
    (1, _(u'Adding / Abstract')),
    (2, _(u'Adding / Authors')),
    (3, _(u'Adding / Media')),
    (11, _(u'New')),
    (12, _(u'Rejected')),
    (13, _(u'In review')),
    (14, _(u'Reviewed')),
    (15, _(u'In rework')),
    (10, _(u'Published')),
)
ARTICLE_ADDING_STATUSES = (0, 1, 2, 3)
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
ATTACH_TYPES = (
    (0, _(u'Generic')),
    (1, _(u'Image')),
    (2, _(u'Video')),
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


# Due to changes in django 1.7 `django.contrib.auth.get_user_model` no longer works in model definition time
# TODO: fire bug
def _get_user_model():
    app_name, model_name = settings.AUTH_USER_MODEL.rsplit('.', 1)
    app = models.get_app(app_name)
    return getattr(app, model_name)


class LocalizedUser(_get_user_model(), BaseLocalizedObject):
    class Meta:
        proxy = True

    def __unicode__(self):
        return self.get_full_name() or self.username

    def get_full_name(self):
        full_name = '%s %s' % (self.localized_first_name, self.localized_last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.localized_first_name

    # We can't use `first_name` as property name because it will clash with field name
    @property
    def localized_first_name(self):
        return self.get_localized('first_name') or ''

    @property
    def localized_last_name(self):
        return self.get_localized('last_name') or ''

    def unpublished_articles(self):
        return Article.objects.exclude(status=10).filter(models.Q(articleauthor__author=self) | models.Q(senders=self)).distinct()


class Section(OrderedEntry):
    name = models.CharField(max_length=100, verbose_name=_(u'Name'))
    moderators = models.ManyToManyField(LocalizedUser, verbose_name=_(u'Moderators'), blank=True)

    class Meta:
        ordering = OrderedEntry.Meta.ordering
        verbose_name = _(u'Section')
        verbose_name_plural = _(u'Sections')

    def __unicode__(self):
        return self.name


class StaffMember(models.Model):
    user = models.OneToOneField(LocalizedUser, verbose_name=_(u'User'))

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


class Organization(ModeratedObject, BaseLocalizedObject):
    short_name = models.CharField(max_length=32, verbose_name=_(u'Short name'), help_text=_(u'for admin site'), default='', blank=True)
    alt_names = models.TextField(verbose_name=_(u'Alternative names'), help_text=_(u'one per line'), default='', blank=True)

    site = models.URLField(blank=True, default='', verbose_name=_(u'Site URL'))

    obsolete = models.BooleanField(default=False, verbose_name=_(u'Obsolete'))
    previous = models.ManyToManyField('self', verbose_name=_(u'Previous versions'), blank=True)

    class Meta:
        ordering = ['short_name']
        verbose_name = _(u'Organization')
        verbose_name_plural = _(u'Organizations')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'show_organization', [self.id]

    @property
    def name(self):
        return self.get_localized('name') or ''

    @property
    def address(self):
        return self.get_localized('address') or ''

    @property
    def country(self):
        return self.get_localized('country') or ''

    @property
    def city(self):
        return self.get_localized('city') or ''


class OrganizationLocalizedContent(BaseLocalizedContent):
    org = models.ForeignKey(Organization)

    name = models.TextField(verbose_name=_(u'Name'))
    country = models.CharField(max_length=100, verbose_name=_(u'Country'), blank=True, default='')
    city = models.CharField(max_length=100, verbose_name=_(u'City'), blank=True, default='')
    address = models.TextField(verbose_name=_(u'Address'), default='', blank=True)

    class Meta:
        unique_together = [('lang', 'org')]


class Author(ModeratedObject):
    user = models.OneToOneField(LocalizedUser, verbose_name=_(u'User'))

    class Meta:
        ordering = ('user__last_name', 'user__first_name')
        verbose_name = _(u'Author')
        verbose_name_plural = _(u'Authors')

    def __unicode__(self):
        return self.user.get_full_name() or self.user.username

    def published_articles(self):
        return Article.objects.filter(status=10, articleauthor__author=self.user).distinct()

    def unpublished_articles(self):
        return Article.objects.exclude(status=10).filter(models.Q(articleauthor__author=self.user) | models.Q(senders=self.user)).distinct()

    @models.permalink
    def get_absolute_url(self):
        return 'show_author', [self.user_id]


class LocalizedName(BaseLocalizedContent):
    user = models.ForeignKey(LocalizedUser, verbose_name=_(u'User'))

    first_name = models.CharField(_('First name'), max_length=60, blank=True)
    last_name = models.CharField(_('Last name'), max_length=60, blank=True)

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
    user = models.ForeignKey(LocalizedUser, verbose_name=_(u'User'))
    organization = models.ForeignKey(Organization, verbose_name=_(u'Organization'))
    position = models.CharField(max_length=200, verbose_name=_(u'Position'), default='', blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = _(u'Position in organization')
        verbose_name_plural = _(u'Position in organizations')
        unique_together = [('user', 'organization')]

    def __unicode__(self):
        return u'%s (%s, %s)' % (self.user.get_full_name() or self.user, self.position, self.organization)


def article_upload_to(instance, filename):
    out = uuid.uuid4().hex + (filename.rsplit('.', 1)[-1][:4].lower() if '.' in filename else '')
    return 'articles/' + out


class Article(BaseLocalizedObject):
    status = models.PositiveSmallIntegerField(default=0, choices=ARTICLE_STATUSES, verbose_name=_(u'Status'))
    date_in = models.DateTimeField(default=timezone.now, verbose_name=_(u'Date in'))
    date_published = models.DateTimeField(null=True, blank=True, verbose_name=_(u'Publish date'))
    old_number = models.SmallIntegerField(null=True, blank=True, verbose_name=_(u'Old number'),
                                          help_text=_(u'to link consistency with old articles'))

    image = models.ImageField(verbose_name=_(u'Image'), upload_to=article_upload_to, blank=True, default='')
    content = models.FileField(verbose_name=_(u'Content'), upload_to='published', default='', blank=True)

    senders = models.ManyToManyField(LocalizedUser, verbose_name=_(u'Senders'), blank=True)
    issue = models.ForeignKey('Issue', null=True, blank=True)
    sections = models.ManyToManyField(Section, blank=True)

    class Meta:
        ordering = ['date_in']
        verbose_name = _(u'Article')
        verbose_name_plural = _(u'Articles')

    def __unicode__(self):
        return self.title or ((_(u'Article %s') % self.id) if self.id else _(u'New article'))
    __unicode__.short_description = _(u'Title')

    def get_absolute_url(self):
        if self.issue:
            return reverse('show_article', args=(self.issue.year, self.issue.volume, self.issue.number, self.id))
        return u''

    def get_authors(self):
        authors = []
        for aa in self.articleauthor_set.all():
            user = aa.author
            if user not in authors:
                authors.append(user)
        return authors

    @property
    def title(self):
        return self.get_localized('title') or ''

    @property
    def abstract(self):
        return self.get_localized('abstract') or ''

    @property
    def keywords(self):
        return self.get_localized('keywords') or ''

    @property
    def references(self):
        return self.get_localized('references') or ''

    def adding(self):
        return self.status in ARTICLE_ADDING_STATUSES


class LocalizedArticleContent(BaseLocalizedContent):
    article = models.ForeignKey(Article, verbose_name=Article._meta.verbose_name)

    title = models.TextField(verbose_name=_(u'Title'))
    abstract = models.TextField(verbose_name=_(u'Abstract'), default=u'', blank=True)
    keywords = models.TextField(verbose_name=_(u'Keywords'), default=u'', blank=True)
    references = models.TextField(verbose_name=_(u'References'), default='', blank=True)

    class Meta:
        ordering = ('article', 'lang')
        verbose_name = _(u'Localized article content')
        verbose_name_plural = _(u'Localized article content')
        unique_together = [('article', 'lang')]

    def __unicode__(self):
        return _(u'Loclized content for %s') % self.article


class ArticleAuthor(OrderedEntry):
    article = models.ForeignKey(Article, verbose_name=Article._meta.verbose_name)
    author = models.ForeignKey(LocalizedUser, verbose_name=_(u'Author'))
    organization = models.ForeignKey(Organization, verbose_name=_(u'Organization'))

    _order_lookup_field = 'article'

    class Meta:
        verbose_name = _(u'Article author')
        verbose_name_plural = _(u'Article authors')
        ordering = OrderedEntry.Meta.ordering
        unique_together = [('article', 'author', 'organization')]

    def __unicode__(self):
        return u'%s (%s)' % (self.author, self.organization)


class ArticleAttach(OrderedEntry):
    article = models.ForeignKey(Article, verbose_name=Article._meta.verbose_name)
    type = models.PositiveSmallIntegerField(choices=ATTACH_TYPES, verbose_name=_(u'Attach type'), default=0)
    file = models.FileField(upload_to='attaches', verbose_name=_(u'File'))
    comment = models.TextField(default='', blank=True, verbose_name=_(u'Comment'))
    date_created = models.DateTimeField(default=timezone.now, verbose_name=_(u'Date created'))

    _order_lookup_field = 'article'

    class Meta:
        verbose_name = _(u'Article attach')
        verbose_name_plural = _(u'Article attaches')
        ordering = OrderedEntry.Meta.ordering
        get_latest_by = 'date_created'

    def __unicode__(self):
        return _(u'Attach for %s') % self.article


class ArticleSource(models.Model):
    article = models.ForeignKey(Article, verbose_name=Article._meta.verbose_name)

    date_created = models.DateTimeField(default=timezone.now, verbose_name=_(u'Date created'))
    file = models.FileField(upload_to='sources', verbose_name=_(u'File'))
    comment = models.TextField(default='', blank=True, verbose_name=_(u'Staff comment'))

    class Meta:
        ordering = ['date_created']
        verbose_name = _(u'Article source')
        verbose_name_plural = _(u'Article sources')
        get_latest_by = 'date_created'

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
        get_latest_by = 'date_created'

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
    reviewer = models.ForeignKey(LocalizedUser, verbose_name=_(u'Reviewer'))
    status = models.PositiveSmallIntegerField(choices=REVIEW_STATUSES, default=0, verbose_name=_(u'Status'))
    date_created = models.DateTimeField(default=timezone.now, verbose_name=_(u'Created'))

    field_values = models.TextField(default='', editable=False, verbose_name=_(u'Field values'))

    comment_for_authors = models.TextField(default=u'', blank=True, verbose_name=_(u'Comment for authors'))
    comment_for_editors = models.TextField(default=u'', blank=True, verbose_name=_(u'Comment for editors'))
    resolution = models.PositiveSmallIntegerField(choices=RESOLUTIONS, default=0, verbose_name=_(u'Resolution'))

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


class Issue(OrderedEntry):
    number = models.CharField(max_length=100, verbose_name=_(u'Number'), blank=True, null=True)
    volume = models.PositiveIntegerField(verbose_name=_(u'Volume'))
    year = models.PositiveIntegerField(verbose_name=_(u'Year'))

    class Meta:
        verbose_name = _(u'Issue')
        verbose_name_plural = _(u'Issue')
        ordering = ['order']

    def __unicode__(self):
        if self.number:
            return ugettext(u'Volume %(volume)s, issue %(number)s, %(year)s year') % self.__dict__
        else:
            return ugettext(u'Volume %(volume)s, %(year)s year') % self.__dict__

    @models.permalink
    def get_absolute_url(self):
        return 'show_issue', [self.id]
