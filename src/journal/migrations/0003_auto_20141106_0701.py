# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_auto_20141106_0545'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order', blank=True)),
                ('field_type', models.PositiveSmallIntegerField(choices=[(0, 'Header'), (1, 'Choices field'), (2, 'Text string'), (3, 'Text field'), (4, 'Checkbox')])),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(default=b'', blank=True)),
                ('choices', models.TextField(default=b'', blank=True)),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='articleresolution',
            options={'ordering': ['date_created']},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name'], 'verbose_name': 'Organization', 'verbose_name_plural': 'Organizations'},
        ),
        migrations.AlterModelOptions(
            name='staffmember',
            options={'ordering': ('chief_editor', 'editor', 'reviewer', 'user__last_name'), 'verbose_name': 'Staff member', 'verbose_name_plural': 'Staff members'},
        ),
        migrations.AddField(
            model_name='articlesource',
            name='comment',
            field=models.TextField(default=b'', verbose_name='Staff comment', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='moderation_status',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Moderation status', choices=[(0, 'New'), (1, 'Rejected'), (2, 'Approved')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='alt_names',
            field=models.TextField(default=b'', help_text='one per line', verbose_name='Alternative names', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='moderation_status',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Moderation status', choices=[(0, 'New'), (1, 'Rejected'), (2, 'Approved')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='review',
            name='field_values',
            field=models.TextField(default=b'', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='volume',
            field=models.ForeignKey(blank=True, to='journal.Volume', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articleresolution',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
