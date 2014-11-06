# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0005_auto_20141106_0841'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleAuthors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order', blank=True)),
                ('article', models.ForeignKey(verbose_name='Article', to='journal.Article')),
                ('position', models.ForeignKey(verbose_name='Author', to='journal.PositionInOrganization')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Article author',
                'verbose_name_plural': 'Article authors',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='orderedauthors',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='orderedauthors',
            name='article',
        ),
        migrations.RemoveField(
            model_name='orderedauthors',
            name='person_in_org',
        ),
        migrations.AlterUniqueTogether(
            name='orderedorganizations',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='orderedorganizations',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='orderedorganizations',
            name='person',
        ),
        migrations.RemoveField(
            model_name='personinorganizations',
            name='organizations',
        ),
        migrations.DeleteModel(
            name='OrderedOrganizations',
        ),
        migrations.RemoveField(
            model_name='personinorganizations',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['date_in'], 'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
        migrations.AlterModelOptions(
            name='articleresolution',
            options={'ordering': ['date_created'], 'verbose_name': 'Article resolution', 'verbose_name_plural': 'Article resolutions'},
        ),
        migrations.AlterModelOptions(
            name='articlesource',
            options={'ordering': ['date_created'], 'verbose_name': 'Article source', 'verbose_name_plural': 'Article sources'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='authors',
        ),
        migrations.DeleteModel(
            name='PersonInOrganizations',
        ),
        migrations.DeleteModel(
            name='OrderedAuthors',
        ),
        migrations.RemoveField(
            model_name='article',
            name='date_out',
        ),
        migrations.AddField(
            model_name='article',
            name='date_published',
            field=models.DateTimeField(null=True, verbose_name='Publish date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articlesource',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='abstract',
            field=models.TextField(verbose_name='Abstract'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.FileField(upload_to=b'published', verbose_name='Content'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='date_in',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date in'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='old_number',
            field=models.SmallIntegerField(help_text='to link consistency with old articles', null=True, verbose_name='Old number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='sections',
            field=models.ManyToManyField(to='journal.Section', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'New'), (1, 'Rejected'), (2, 'In review'), (3, 'Reviewed'), (4, 'Published'), (5, 'In rework')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.TextField(verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articleresolution',
            name='article',
            field=models.ForeignKey(verbose_name='Article', to='journal.Article'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articleresolution',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articleresolution',
            name='reviews',
            field=models.ManyToManyField(to='journal.Review', verbose_name='Reviews'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articleresolution',
            name='status',
            field=models.PositiveSmallIntegerField(verbose_name='Status', choices=[(0, 'None'), (1, 'Reject'), (2, 'Correct'), (3, 'Publish')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articleresolution',
            name='text',
            field=models.TextField(verbose_name='Text'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articlesource',
            name='article',
            field=models.ForeignKey(verbose_name='Article', to='journal.Article'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articlesource',
            name='file',
            field=models.FileField(upload_to=b'sources', verbose_name='File'),
            preserve_default=True,
        ),
    ]
