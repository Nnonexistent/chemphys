# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.PositiveSmallIntegerField(default=0, choices=[(0, 'New'), (1, 'Rejected'), (2, 'In review'), (3, 'Reviewed'), (4, 'Published'), (5, 'In rework')])),
                ('date_in', models.DateField(default=django.utils.timezone.now)),
                ('date_out', models.DateField(null=True, blank=True)),
                ('old_number', models.SmallIntegerField(null=True, blank=True)),
                ('title', models.TextField()),
                ('abstract', models.TextField()),
                ('content', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleResolution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'None'), (1, 'Reject'), (2, 'Correct'), (3, 'Publish')])),
                ('text', models.TextField()),
                ('date_created', models.DateTimeField()),
                ('article', models.ForeignKey(to='journal.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'sources')),
                ('article', models.ForeignKey(to='journal.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name_ru', models.CharField(max_length=60, verbose_name='first name', blank=True)),
                ('last_name_ru', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('first_name_en', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name_en', models.CharField(max_length=30, verbose_name='last name', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderedAuthors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField()),
                ('article', models.ForeignKey(to='journal.Article')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderedOrganizations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('site', models.URLField()),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('address', models.TextField(default=b'', blank=True)),
                ('obsolete', models.BooleanField(default=False)),
                ('previous', models.ManyToManyField(related_name='previous_rel_+', to='journal.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonInOrganizations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organizations', models.ManyToManyField(to='journal.Organization', through='journal.OrderedOrganizations')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PositionInOrganization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.CharField(max_length=200)),
                ('author', models.ForeignKey(to='journal.Author')),
                ('organization', models.ForeignKey(to='journal.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment_for_authors', models.TextField(default='', blank=True)),
                ('comment_for_editors', models.TextField(default='', blank=True)),
                ('resolution', models.PositiveSmallIntegerField(default=0, choices=[(0, 'None'), (1, 'Reject'), (2, 'Correct'), (3, 'Publish')])),
                ('article', models.ForeignKey(to='journal.Article')),
                ('reviewer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReviewFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'reviews')),
                ('review', models.ForeignKey(to='journal.Review')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('moderators', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chief_editor', models.BooleanField(default=False)),
                ('editor', models.BooleanField(default=False)),
                ('reviewer', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('year', models.PositiveIntegerField()),
                ('order', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='orderedorganizations',
            name='organization',
            field=models.ForeignKey(to='journal.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderedorganizations',
            name='person',
            field=models.ForeignKey(to='journal.PersonInOrganizations'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='orderedorganizations',
            unique_together=set([('person', 'organization')]),
        ),
        migrations.AddField(
            model_name='orderedauthors',
            name='person_in_org',
            field=models.ForeignKey(to='journal.PersonInOrganizations'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='orderedauthors',
            unique_together=set([('article', 'person_in_org')]),
        ),
        migrations.AddField(
            model_name='author',
            name='organizations',
            field=models.ManyToManyField(to='journal.Organization', through='journal.PositionInOrganization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articleresolution',
            name='reviews',
            field=models.ManyToManyField(to='journal.Review'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='authors',
            field=models.ManyToManyField(to='journal.PersonInOrganizations', through='journal.OrderedAuthors'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='sections',
            field=models.ManyToManyField(to='journal.Section'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='volume',
            field=models.ForeignKey(to='journal.Volume'),
            preserve_default=True,
        ),
    ]
