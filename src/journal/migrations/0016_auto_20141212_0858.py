# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0015_auto_20141212_0855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='title',
        ),
        migrations.AddField(
            model_name='issue',
            name='number',
            field=models.CharField(max_length=100, null=True, verbose_name='Number', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='volume',
            field=models.PositiveIntegerField(default=1, verbose_name='Volume'),
            preserve_default=False,
        ),
    ]
