# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0018_article_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='senders',
            field=models.ManyToManyField(to='journal.LocalizedUser', verbose_name='Senders', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'Adding / Overview'), (1, 'Adding / Abstract'), (2, 'Adding / Authors'), (3, 'Adding / Media'), (11, 'New'), (12, 'Rejected'), (13, 'In review'), (14, 'Reviewed'), (15, 'In rework'), (10, 'Published')]),
            preserve_default=True,
        ),
    ]
