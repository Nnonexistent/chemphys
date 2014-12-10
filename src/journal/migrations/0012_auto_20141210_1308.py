# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0011_auto_20141113_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='positioninorganization',
            name='position',
            field=models.CharField(default=b'', max_length=200, verbose_name='Position', blank=True),
            preserve_default=True,
        ),
    ]
