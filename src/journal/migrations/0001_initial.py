# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import journal.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0002_auto_20150212_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('moderation_status', models.PositiveSmallIntegerField(default=0, verbose_name='Moderation status', choices=[(0, 'New'), (1, 'Rejected'), (2, 'Approved')])),
                ('email', models.EmailField(unique=True, max_length=75, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('degree', models.CharField(default=b'', max_length=200, verbose_name='Degree', blank=True)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', to='auth.Group', verbose_name='groups', blank=True)),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', to='auth.Permission', verbose_name='user permissions', blank=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.PositiveSmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'Adding / Overview'), (1, 'Adding / Abstract'), (2, 'Adding / Authors'), (3, 'Adding / Media'), (11, 'New'), (12, 'Rejected'), (13, 'In review'), (14, 'Reviewed'), (15, 'In rework'), (10, 'Published')])),
                ('date_in', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date in')),
                ('date_published', models.DateTimeField(null=True, verbose_name='Publish date', blank=True)),
                ('old_number', models.SmallIntegerField(help_text='to link consistently with old articles', null=True, verbose_name='Old number', blank=True)),
                ('image', models.ImageField(default=b'', upload_to=journal.models.article_upload_to, verbose_name='Image', blank=True)),
                ('type', models.PositiveSmallIntegerField(default=1, verbose_name='Article type', choices=[(1, 'Article'), (2, 'Short message'), (3, 'Presentation'), (4, 'Data')])),
                ('content', models.FileField(default=b'', upload_to=b'published', verbose_name='Content', blank=True)),
            ],
            options={
                'ordering': ['date_in'],
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleAttach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order', blank=True)),
                ('type', models.PositiveSmallIntegerField(default=0, verbose_name='Attach type', choices=[(0, 'Generic'), (1, 'Image'), (2, 'Video')])),
                ('file', models.FileField(upload_to=b'attaches', verbose_name='File')),
                ('comment', models.TextField(default=b'', verbose_name='Comment', blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('article', models.ForeignKey(verbose_name='Article', to='journal.Article')),
            ],
            options={
                'ordering': ['order'],
                'get_latest_by': 'date_created',
                'verbose_name': 'Article attach',
                'verbose_name_plural': 'Article attaches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order', blank=True)),
                ('article', models.ForeignKey(verbose_name='Article', to='journal.Article')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Article author',
                'verbose_name_plural': 'Article authors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleResolution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('status', models.PositiveSmallIntegerField(verbose_name='Status', choices=[(0, 'None'), (1, 'Rejected'), (2, 'Rework required'), (3, 'Approved')])),
                ('text', models.TextField(verbose_name='Text')),
                ('article', models.ForeignKey(verbose_name='Article', to='journal.Article')),
            ],
            options={
                'ordering': ['date_created'],
                'get_latest_by': 'date_created',
                'verbose_name': 'Article resolution',
                'verbose_name_plural': 'Article resolutions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('file', models.FileField(upload_to=b'sources', verbose_name='File')),
                ('comment', models.TextField(default=b'', verbose_name='Staff comment', blank=True)),
                ('article', models.ForeignKey(verbose_name='Article', to='journal.Article')),
            ],
            options={
                'ordering': ['date_created'],
                'get_latest_by': 'date_created',
                'verbose_name': 'Article source',
                'verbose_name_plural': 'Article sources',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order', blank=True)),
                ('is_active', models.BooleanField(default=False, verbose_name='Active')),
                ('number', models.CharField(max_length=100, null=True, verbose_name='Number', blank=True)),
                ('volume', models.PositiveIntegerField(verbose_name='Volume')),
                ('year', models.PositiveIntegerField(verbose_name='Year')),
                ('description', models.TextField(default='', verbose_name='Description', blank=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Issue',
                'verbose_name_plural': 'Issues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocalizedArticleContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=2, verbose_name='Language', choices=[(b'ru', 'Russian'), (b'en', 'English')])),
                ('title', models.TextField(verbose_name='Title')),
                ('abstract', models.TextField(default='', verbose_name='Abstract', blank=True)),
                ('keywords', models.TextField(default='', verbose_name='Keywords', blank=True)),
                ('references', models.TextField(default=b'', verbose_name='References', blank=True)),
                ('article', models.ForeignKey(verbose_name='Article', to='journal.Article')),
            ],
            options={
                'ordering': ('article', 'lang'),
                'verbose_name': 'Localized article content',
                'verbose_name_plural': 'Localized article content',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocalizedName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=2, verbose_name='Language', choices=[(b'ru', 'Russian'), (b'en', 'English')])),
                ('first_name', models.CharField(max_length=60, verbose_name='First name', blank=True)),
                ('last_name', models.CharField(max_length=60, verbose_name='Last name', blank=True)),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('user', 'lang'),
                'verbose_name': 'Localized name',
                'verbose_name_plural': 'Localized names',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('moderation_status', models.PositiveSmallIntegerField(default=0, verbose_name='Moderation status', choices=[(0, 'New'), (1, 'Rejected'), (2, 'Approved')])),
                ('short_name', models.CharField(default=b'', help_text='for admin site', max_length=32, verbose_name='Short name', blank=True)),
                ('alt_names', models.TextField(default=b'', help_text='one per line', verbose_name='Alternative names', blank=True)),
                ('site', models.URLField(default=b'', verbose_name='Site URL', blank=True)),
                ('obsolete', models.BooleanField(default=False, verbose_name='Obsolete')),
                ('previous', models.ManyToManyField(related_name='previous_rel_+', verbose_name='Previous versions', to='journal.Organization', blank=True)),
            ],
            options={
                'ordering': ['short_name'],
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationLocalizedContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=2, verbose_name='Language', choices=[(b'ru', 'Russian'), (b'en', 'English')])),
                ('name', models.TextField(verbose_name='Name')),
                ('country', models.CharField(default=b'', max_length=100, verbose_name='Country', blank=True)),
                ('city', models.CharField(default=b'', max_length=100, verbose_name='City', blank=True)),
                ('address', models.TextField(default=b'', verbose_name='Address', blank=True)),
                ('org', models.ForeignKey(to='journal.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PositionInOrganization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.CharField(default=b'', max_length=200, verbose_name='Position', blank=True)),
                ('organization', models.ForeignKey(verbose_name='Organization', to='journal.Organization')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Position in organization',
                'verbose_name_plural': 'Position in organizations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(default=journal.models.default_key, verbose_name='Key', unique=True, max_length=32, editable=False)),
                ('status', models.PositiveSmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'Pending'), (1, 'Unfinished'), (2, 'Done')])),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created')),
                ('field_values', models.TextField(default=b'', verbose_name='Field values', editable=False)),
                ('comment_for_authors', models.TextField(default='', verbose_name='Comment for authors', blank=True)),
                ('comment_for_editors', models.TextField(default='', verbose_name='Comment for editors', blank=True)),
                ('resolution', models.PositiveSmallIntegerField(default=0, verbose_name='Resolution', choices=[(0, 'None'), (1, 'Rejected'), (2, 'Rework required'), (3, 'Approved')])),
                ('article', models.ForeignKey(verbose_name='Article', to='journal.Article')),
                ('reviewer', models.ForeignKey(verbose_name='Reviewer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_created'],
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReviewField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order', blank=True)),
                ('field_type', models.PositiveSmallIntegerField(verbose_name='Field type', choices=[(0, 'Header'), (1, 'Choices field'), (2, 'Text string'), (3, 'Text field'), (4, 'Checkbox')])),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('description', models.TextField(default=b'', verbose_name='Description', blank=True)),
                ('choices', models.TextField(default=b'', verbose_name='Choices', blank=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Review field',
                'verbose_name_plural': 'Review fields',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReviewFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'reviews', verbose_name='File')),
                ('comment', models.TextField(default=b'', verbose_name='Comment', blank=True)),
                ('review', models.ForeignKey(verbose_name='Review', to='journal.Review')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Review file',
                'verbose_name_plural': 'Review files',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order', blank=True)),
                ('moderators', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Moderators', blank=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SectionName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=2, verbose_name='Language', choices=[(b'ru', 'Russian'), (b'en', 'English')])),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('section', models.ForeignKey(verbose_name='Section', to='journal.Section')),
            ],
            options={
                'verbose_name': 'Section name',
                'verbose_name_plural': 'Section names',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chief_editor', models.BooleanField(default=False, verbose_name='Chief editor')),
                ('editor', models.BooleanField(default=False, verbose_name='Editor')),
                ('reviewer', models.BooleanField(default=False, verbose_name='Reviewer')),
                ('user', models.OneToOneField(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('chief_editor', 'editor', 'reviewer', 'user__localizedname__last_name'),
                'verbose_name': 'Staff member',
                'verbose_name_plural': 'Staff members',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='sectionname',
            unique_together=set([('lang', 'section')]),
        ),
        migrations.AlterUniqueTogether(
            name='positioninorganization',
            unique_together=set([('user', 'organization')]),
        ),
        migrations.AlterUniqueTogether(
            name='organizationlocalizedcontent',
            unique_together=set([('lang', 'org')]),
        ),
        migrations.AlterUniqueTogether(
            name='localizedname',
            unique_together=set([('user', 'lang')]),
        ),
        migrations.AlterUniqueTogether(
            name='localizedarticlecontent',
            unique_together=set([('article', 'lang')]),
        ),
        migrations.AddField(
            model_name='articleresolution',
            name='reviews',
            field=models.ManyToManyField(to='journal.Review', verbose_name='Reviews'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articleauthor',
            name='organization',
            field=models.ForeignKey(verbose_name='Organization', to='journal.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articleauthor',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='articleauthor',
            unique_together=set([('article', 'user', 'organization')]),
        ),
        migrations.AddField(
            model_name='article',
            name='issue',
            field=models.ForeignKey(verbose_name='Issue', blank=True, to='journal.Issue', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='sections',
            field=models.ManyToManyField(to='journal.Section', verbose_name='Sections', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='senders',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Senders', blank=True),
            preserve_default=True,
        ),
    ]
