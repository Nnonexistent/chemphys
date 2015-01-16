# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import journal.models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0024_auto_20150113_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Active'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='key',
            field=models.CharField(default=journal.models.default_key, verbose_name='Key', unique=True, max_length=32, editable=False),
            preserve_default=True,
        ),
    ]
