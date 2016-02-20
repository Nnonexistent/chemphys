# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0012_auto_20151217_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'Adding / Overview'), (1, 'Adding / Abstract'), (2, 'Adding / Authors'), (3, 'Adding / Media'), (11, 'New'), (13, 'In review'), (15, 'In rework'), (16, 'Reworked'), (10, 'Published'), (12, 'Rejected')]),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='issue',
            unique_together=set([('number', 'volume', 'year')]),
        ),
    ]
