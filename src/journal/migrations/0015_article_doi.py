# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0014_auto_20160311_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='doi',
            field=models.URLField(null=True, verbose_name=b'DOI', blank=True),
            preserve_default=True,
        ),
    ]
