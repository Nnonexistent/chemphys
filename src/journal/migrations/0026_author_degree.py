# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0025_auto_20150116_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='degree',
            field=models.CharField(default=b'', max_length=200, verbose_name='Degree', blank=True),
            preserve_default=True,
        ),
    ]
