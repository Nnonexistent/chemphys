# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0007_auto_20141106_1022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['date_created'], 'verbose_name': 'Review', 'verbose_name_plural': 'Reviews'},
        ),
        migrations.AlterModelOptions(
            name='reviewfield',
            options={'ordering': ['order'], 'verbose_name': 'Review field', 'verbose_name_plural': 'Review fields'},
        ),
        migrations.AlterModelOptions(
            name='reviewfile',
            options={'ordering': ['id'], 'verbose_name': 'Review file', 'verbose_name_plural': 'Review files'},
        ),
        migrations.AddField(
            model_name='reviewfile',
            name='comment',
            field=models.TextField(default=b'', verbose_name='Comment', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articleresolution',
            name='status',
            field=models.PositiveSmallIntegerField(verbose_name='Status', choices=[(0, 'None'), (1, 'Rejected'), (2, 'Rework required'), (3, 'Approved')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='article',
            field=models.ForeignKey(verbose_name='Article', to='journal.Article'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='comment_for_authors',
            field=models.TextField(default='', verbose_name='Comment for authors', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='comment_for_editors',
            field=models.TextField(default='', verbose_name='Comment for editors', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='field_values',
            field=models.TextField(default=b'', verbose_name='Field values', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='resolution',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Resolution', choices=[(0, 'None'), (1, 'Rejected'), (2, 'Rework required'), (3, 'Approved')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(verbose_name='Reviewer', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'Pending'), (1, 'Unfinished'), (2, 'Done')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reviewfield',
            name='choices',
            field=models.TextField(default=b'', verbose_name='Choices', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reviewfield',
            name='description',
            field=models.TextField(default=b'', verbose_name='Description', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reviewfield',
            name='field_type',
            field=models.PositiveSmallIntegerField(verbose_name='Field type', choices=[(0, 'Header'), (1, 'Choices field'), (2, 'Text string'), (3, 'Text field'), (4, 'Checkbox')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reviewfield',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reviewfile',
            name='file',
            field=models.FileField(upload_to=b'reviews', verbose_name='File'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reviewfile',
            name='review',
            field=models.ForeignKey(verbose_name='Review', to='journal.Review'),
            preserve_default=True,
        ),
    ]
