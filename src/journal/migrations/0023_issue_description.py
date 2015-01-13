# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0022_auto_20150113_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='description',
            field=models.TextField(default='', verbose_name='Description', blank=True),
            preserve_default=True,
        ),
    ]
