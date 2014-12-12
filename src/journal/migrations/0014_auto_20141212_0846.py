# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0013_auto_20141212_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='localizedarticlecontent',
            name='keywords',
            field=models.TextField(default='', verbose_name='Keywords', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='localizedarticlecontent',
            name='abstract',
            field=models.TextField(default='', verbose_name='Abstract', blank=True),
            preserve_default=True,
        ),
    ]
