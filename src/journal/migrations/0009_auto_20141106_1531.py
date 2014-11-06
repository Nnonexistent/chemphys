# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0008_auto_20141106_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='short_name',
            field=models.CharField(default=b'', help_text='for admin site', max_length=32, verbose_name='Short name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'New'), (1, 'Rejected'), (2, 'In review'), (3, 'Reviewed'), (10, 'Published'), (5, 'In rework')]),
            preserve_default=True,
        ),
    ]
