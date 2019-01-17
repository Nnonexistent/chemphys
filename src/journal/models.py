# -*- coding: utf-8 -*-

import json
import uuid
import mimetypes
from collections import OrderedDict

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.template.loader import render_to_string
from django.contrib.auth.models import BaseUserManager

from utils.localized import BaseLocalizedObject, BaseLocalizedContent


ARTICLE_STATUSES = (
    (0, _(u'Adding / Overview')),
    (1, _(u'Adding / Abstract')),
    (2, _(u'Adding / Authors')),
    (3, _(u'Adding / Media')),
    (11, _(u'New')),
    (13, _(u'In review')),
    (15, _(u'In rework')),
    (16, _(u'Reworked')),
    (10, _(u'Published')),
    (12, _(u'Rejected')),
)
ARTICLE_ADDING_STATUSES = (0, 1, 2, 3)
ARTICLE_TYPES = (
    (1, _(u'Article')),
    (2, _(u'Short message')),
    (3, _(u'Presentation')),
    (4, _(u'Data')),
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
ATTACH_TYPES = (
    (1, _(u'Image')),
    (2, _(u'Video')),
    (0, _(u'Generic')),
)


def default_key():
    return uuid.uuid4().hex


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


# TODO: multiple emails for user

class JournalUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class JournalUser(AbstractBaseUser, PermissionsMixin, ModeratedObject, BaseLocalizedObject):  # Moderation only applied to author role
    email = models.EmailField(_('email address'))
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    degree = models.CharField(max_length=200, verbose_name=_(u'Degree'), blank=True, default='')

    objects = JournalUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.get_full_name() or self.email

    @models.permalink
    def get_absolute_url(self):
        return 'show_author', [self.id]

    def clean(self):
        if self.moderation_status == 2:
            qs = self.__class__.objects.filter(email=self.email)
            if self.id:
                qs = qs.exclude(id=self.id)
            if qs.exists():
                raise ValidationError(_(u'Duplicated email for approved users'))

    def get_full_name(self):
        return (u'%s %s' % (self.first_name, self.last_name)).strip()
    get_full_name.short_description = _(u'Full name')

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def str_compact(self):
        return u'%s %s' % (self.last_name, u' '.join(u'%s.' % i[0] for i in self.first_name.split() if i))

    @property
    def first_name(self):
        return self.get_localized('first_name') or ''

    @property
    def last_name(self):
        return self.get_localized('last_name') or ''

    def published_articles(self):
        return Article.objects.filter(status=10, articleauthor__user=self).distinct()

    def unpublished_articles(self):
        return Article.objects.exclude(status=10).filter(models.Q(articleauthor__user=self) | models.Q(senders=self)).distinct()

    def pending_reviews(self):
        return self.review_set.filter(status__in=(0, 1)).distinct()

    def has_journal_profile(self):
        return bool(self.is_active and self.moderation_status == 2 and self.published_articles())

# override user default moderation status
JournalUser._meta.get_field('moderation_status').default = 2


class Section(OrderedEntry, BaseLocalizedObject):
    moderators = models.ManyToManyField(JournalUser, verbose_name=_(u'Moderators'), blank=True)

    class Meta:
        ordering = OrderedEntry.Meta.ordering
        verbose_name = _(u'Section')
        verbose_name_plural = _(u'Sections')

    def __unicode__(self):
        return self.name

    @property
    def name(self):
        return self.get_localized('name') or ''


class SectionName(BaseLocalizedContent):
    section = models.ForeignKey(Section, verbose_name=Section._meta.verbose_name)

    name = models.CharField(max_length=100, verbose_name=_(u'Name'))

    class Meta:
        verbose_name = _(u'Section name')
        verbose_name_plural = _(u'Section names')
        unique_together = [('lang', 'section')]


class StaffMember(models.Model):
    user = models.OneToOneField(JournalUser, verbose_name=_(u'User'))

    chief_editor = models.BooleanField(default=False, verbose_name=_(u'Chief editor'))
    editor = models.BooleanField(default=False, verbose_name=_(u'Editor'))
    reviewer = models.BooleanField(default=False, verbose_name=_(u'Reviewer'))

    class Meta:
        ordering = ('chief_editor', 'editor', 'reviewer', 'user__localizedname__last_name')
        verbose_name = _(u'Staff member')
        verbose_name_plural = _(u'Staff members')

    def save(self, *args, **kwargs):
        if self.chief_editor:
            StaffMember.objects.filter(chief_editor=True).update(chief_editor=False)
        super(StaffMember, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.get_full_name() or self.user.email


class Organization(ModeratedObject, BaseLocalizedObject):
    short_name = models.CharField(max_length=32, verbose_name=_(u'Short name'), help_text=_(u'for admin site'), default='', blank=True)
    alt_names = models.TextField(verbose_name=_(u'Alternative names'), help_text=_(u'one per line'), default='', blank=True)

    site = models.URLField(blank=True, default='', verbose_name=_(u'Site URL'))

    obsolete = models.BooleanField(default=False, verbose_name=_(u'Obsolete'))
    previous = models.ManyToManyField('self', verbose_name=_(u'Previous versions'), blank=True, limit_choices_to={'obsolete': True})

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
        verbose_name = _(u'Organization localized content')
        verbose_name_plural = _(u'Organization localized content')

    def __unicode__(self):
        return self.name


class LocalizedName(BaseLocalizedContent):
    user = models.ForeignKey(JournalUser, verbose_name=_(u'User'))

    first_name = models.CharField(_('First name'), max_length=60, blank=True)
    last_name = models.CharField(_('Last name'), max_length=60, blank=True)

    class Meta:
        ordering = ('user', 'lang')
        verbose_name = _(u'Localized name')
        verbose_name_plural = _(u'Localized names')
        unique_together = [('user', 'lang')]

    def __unicode__(self):
        return (u'%s %s' % (self.last_name, self.first_name)) or self.user.username


class PositionInOrganization(models.Model):
    user = models.ForeignKey(JournalUser, verbose_name=_(u'User'))
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
    out = uuid.uuid4().hex
    if '.' in filename:
        out += '.' + filename.rsplit('.', 1)[-1][:16].lower()
    return 'articles/' + out


def report_upload_to(instance, filename):
    out = uuid.uuid4().hex
    if '.' in filename:
        out += '.' + filename.rsplit('.', 1)[-1][:16].lower()
    return 'reports/' + out


class Article(BaseLocalizedObject):
    status = models.PositiveSmallIntegerField(default=0, choices=ARTICLE_STATUSES, verbose_name=_(u'Status'))
    date_in = models.DateTimeField(default=timezone.now, verbose_name=_(u'Date in'))
    date_published = models.DateTimeField(null=True, blank=True, verbose_name=_(u'Publish date'))
    old_number = models.CharField(default='', blank=True, verbose_name=_(u'Old number'), max_length=20,
                                  help_text=_(u'to link consistency with old articles'))

    image = models.ImageField(verbose_name=_(u'Image'), upload_to=article_upload_to, blank=True, default='')
    doi = models.URLField(verbose_name='DOI', blank=True, null=True)
    type = models.PositiveSmallIntegerField(verbose_name=_(u'Article type'), choices=ARTICLE_TYPES, default=1)
    lang = models.CharField(max_length=2, choices=settings.LANGUAGES, verbose_name=_(u'Article language'), default=settings.LANGUAGE_CODE)
    report = models.FileField(verbose_name=_(u'Акт экспертизы'), upload_to=report_upload_to, default='', blank=True)
    content = models.FileField(verbose_name=_(u'Content'), upload_to='published', default='', blank=True)

    senders = models.ManyToManyField(JournalUser, verbose_name=_(u'Senders'), blank=True)
    issue = models.ForeignKey('Issue', null=True, blank=True, verbose_name=_(u'Issue'))
    sections = models.ManyToManyField(Section, blank=True, verbose_name=_(u'Sections'))

    class Meta:
        ordering = ('-date_published', 'id')
        verbose_name = _(u'Article')
        verbose_name_plural = _(u'Articles')

    def __unicode__(self):
        return self.title or ((_(u'Article %s') % self.id) if self.id else _(u'New article'))
    __unicode__.short_description = _(u'Title')

    def get_absolute_url(self):
        if self.issue:
            kwargs = {'year': self.issue.year, 'volume': self.issue.volume, 'id': self.id}
            if self.issue.number:
                kwargs['number'] = self.issue.number
            return reverse('show_article', kwargs=kwargs)
        return u''

    def clean(self):
        if self.status == 10:
            if not self.content:
                raise ValidationError(_(u'Published article must have content file'))
            if not self.date_published:
                raise ValidationError(_(u'Published article must have published date'))
        if self.date_published and self.date_published < self.date_in:
            raise ValidationError(_(u'Published date must be after date in'))

        if self.old_number:
            qs = self.__class__.objects.filter(old_number=self.old_number)
            if self.id:
                qs = qs.exclude(id=self.id)
            if qs.exists():
                raise ValidationError(_(u'Duplicated %s field') % self._meta.get_field('old_number').verbose_name)


    def get_authors(self):
        authors = OrderedDict()
        for aa in self.articleauthor_set.all():
            authors.setdefault(aa.user, []).append(aa.organization)
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

    def str_authors(self):
        return u', '.join(a.str_compact() for a in self.get_authors().keys())

    def has_video(self):
        return self.articleattach_set.filter(type=2).exists()


class LocalizedArticleContent(BaseLocalizedContent):
    article = models.ForeignKey(Article, verbose_name=Article._meta.verbose_name)

    title = models.TextField(verbose_name=_(u'Title'), default='', blank=True)
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

    def is_filled(self):
        return any((self.title, self.abstract, self.keywords))


class ArticleAuthor(OrderedEntry):
    article = models.ForeignKey(Article, verbose_name=Article._meta.verbose_name)
    user = models.ForeignKey(JournalUser, verbose_name=_(u'User'))
    organization = models.ForeignKey(Organization, verbose_name=_(u'Organization'))

    _order_lookup_field = 'article'

    class Meta:
        verbose_name = _(u'Article author')
        verbose_name_plural = _(u'Article authors')
        ordering = OrderedEntry.Meta.ordering
        unique_together = [('article', 'user', 'organization')]

    def __unicode__(self):
        return u'%s (%s)' % (self.user, self.organization)


class ArticleAttach(OrderedEntry):
    article = models.ForeignKey(Article, verbose_name=Article._meta.verbose_name)
    type = models.PositiveSmallIntegerField(choices=ATTACH_TYPES, verbose_name=_(u'Attach type'), default=1)
    file = models.FileField(upload_to='attaches', verbose_name=_(u'File'))
    comment = models.TextField(default='', blank=True, verbose_name=_(u'Comment to file'))
    date_created = models.DateTimeField(default=timezone.now, verbose_name=_(u'Date created'))

    _order_lookup_field = 'article'

    class Meta:
        verbose_name = _(u'Article attach')
        verbose_name_plural = _(u'Article attaches')
        ordering = OrderedEntry.Meta.ordering
        get_latest_by = 'date_created'

    def __unicode__(self):
        return _(u'Attach for %s') % self.article

    def icon_url(self):
        mt = mimetypes.guess_type(self.file.path)[0]
        if mt:
            path = u'img/mimetypes/%s.png' % mt.replace('/', '-')
            if staticfiles_storage.exists(path):
                return staticfiles_storage.url(path)

            path = u'img/mimetypes/%s.png' % self.file.path.rsplit('.', 1)[-1]
            if staticfiles_storage.exists(path):
                return staticfiles_storage.url(path)
        return staticfiles_storage.url(u'img/mimetypes/unknown.png')


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

    def formfield(self):
        from django import forms
        from django.utils.html import escape

        class HeaderField(forms.Field):
            def __init__(self, *args, **kwargs):
                label = kwargs.get('label')
                kwargs['label'] = ''

                class HeaderWidget(forms.Widget):
                    def render(self, name, value, attrs=None):
                        return '<h4>%s</h4>' % escape(label)
                kwargs['widget'] = HeaderWidget

                super(HeaderField, self).__init__(*args, **kwargs)

        kwargs = {'label': self.name,
                  'help_text': self.description,
                  'required': False}

        if self.field_type == 0:  # Header
            return HeaderField(**kwargs)

        elif self.field_type == 1:  # Choice field
            choices = filter(None, self.choices.strip().splitlines())
            choices = map(unicode.strip, choices)
            choices = zip(choices, choices)
            choices.insert(0, ('', '-' * 8))
            kwargs['choices'] = choices
            return forms.ChoiceField(**kwargs)

        elif self.field_type == 2:  # Text string
            return forms.CharField(**kwargs)

        elif self.field_type == 3:  # Text field
            kwargs['widget'] = forms.Textarea
            return forms.CharField(**kwargs)

        elif self.field_type == 4:  # Checkbox
            return forms.BooleanField(**kwargs)


class Review(models.Model):
    key = models.CharField(max_length=32, verbose_name=_(u'Key'), unique=True, default=default_key, editable=False)
    article = models.ForeignKey(Article, verbose_name=Article._meta.verbose_name)
    reviewer = models.ForeignKey(JournalUser, verbose_name=_(u'Reviewer'), limit_choices_to={'staffmember__reviewer': True})
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

    def save(self, *args, **kwargs):
        new = not self.id

        super(Review, self).save(*args, **kwargs)

        if new:
            self.send()

    def send(self):
        msg = render_to_string('journal/mail/review.txt', {
            'link': settings.SITE_URL + reverse('edit_review_login', args=[self.key]),
            'review': self,
            'user': self.reviewer,
            'article': self.article,
        })
        self.reviewer.email_user(u'Review request', msg)

    @models.permalink
    def get_absolute_url(self):
        return 'edit_review', [self.key]

    @property
    def values(self):
        if self.field_values:
            return json.loads(self.field_values)
        return []

    @values.setter
    def values(self, value):
        # beware: if you change value after assignement changes will not be saved
        self.field_values = json.dumps(value)

    def render(self):
        from django.utils.html import strip_spaces_between_tags

        return strip_spaces_between_tags(render_to_string('journal/review_result.html', {'data': self.values}))
    render.short_description = _(u'Data')


class Issue(OrderedEntry, BaseLocalizedObject):
    is_active = models.BooleanField(verbose_name=_(u'Active'), default=False, blank=True)

    number = models.CharField(max_length=100, verbose_name=_(u'Number'), blank=True, null=True)
    volume = models.PositiveIntegerField(verbose_name=_(u'Volume'))
    year = models.PositiveIntegerField(verbose_name=_(u'Year'))

    class Meta:
        verbose_name = _(u'Issue')
        verbose_name_plural = _(u'Issues')
        ordering = ['order']
        unique_together = ('number', 'volume', 'year')

    def __unicode__(self):
        if self.number:
            return ugettext(u'Volume %(volume)s, issue %(number)s, %(year)s year') % self.__dict__
        else:
            return ugettext(u'Volume %(volume)s, %(year)s year') % self.__dict__

    def to_str_no_year(self):
        if self.number:
            return ugettext(u'Volume %(volume)s, issue %(number)s') % self.__dict__
        else:
            return ugettext(u'Volume %(volume)s') % self.__dict__

    def str_compact(self):
        if self.number:
            return ugettext(u'%(year)s. V.%(volume)s, iss. %(number)s') % self.__dict__
        else:
            return ugettext(u'%(year)s. V.%(volume)s') % self.__dict__

    @property
    def description(self):
        return self.get_localized('description') or ''

    @property
    def title(self):
        return self.get_localized('title') or ''

    def get_absolute_url(self):
        kwargs = {'year': self.year, 'volume': self.volume}
        if self.number:
            kwargs['number'] = self.number
        return reverse('show_issue', kwargs=kwargs)

    def published_count(self):
        return self.article_set.filter(status=10).count()


class LocalizedIssueContent(BaseLocalizedContent):
    issue = models.ForeignKey(Issue, verbose_name=Issue._meta.verbose_name)
    description = models.TextField(verbose_name=_(u'Description'), default=u'', blank=True)
    title = models.CharField(max_length=200, default='', blank=True, verbose_name=_(u'Title'))

    class Meta:
        unique_together = ('lang', 'issue')

    def __unicode__(self):
        return unicode(self.issue)

# TODO: article and profile user input escaping
