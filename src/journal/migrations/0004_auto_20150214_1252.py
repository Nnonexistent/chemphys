# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0003_auto_20150214_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleattach',
            name='type',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Attach type', choices=[(1, 'Image'), (2, 'Video'), (0, 'Generic')]),
            preserve_default=True,
        ),
    ]
