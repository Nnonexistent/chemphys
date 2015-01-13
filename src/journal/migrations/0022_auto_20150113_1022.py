# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0021_auto_20150104_1510'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articleattach',
            options={'ordering': ['order'], 'get_latest_by': 'date_created', 'verbose_name': 'Article attach', 'verbose_name_plural': 'Article attaches'},
        ),
        migrations.AlterModelOptions(
            name='articleresolution',
            options={'ordering': ['date_created'], 'get_latest_by': 'date_created', 'verbose_name': 'Article resolution', 'verbose_name_plural': 'Article resolutions'},
        ),
        migrations.AlterModelOptions(
            name='articlesource',
            options={'ordering': ['date_created'], 'get_latest_by': 'date_created', 'verbose_name': 'Article source', 'verbose_name_plural': 'Article sources'},
        ),
        migrations.AddField(
            model_name='article',
            name='type',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Article type', choices=[(1, 'Article'), (2, 'Short message'), (3, 'Presentation'), (4, 'Data')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='issue',
            field=models.ForeignKey(verbose_name='Issue', blank=True, to='journal.Issue', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='old_number',
            field=models.SmallIntegerField(help_text='to link consistently with old articles', null=True, verbose_name='Old number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='sections',
            field=models.ManyToManyField(to='journal.Section', verbose_name='Sections', blank=True),
            preserve_default=True,
        ),
    ]
