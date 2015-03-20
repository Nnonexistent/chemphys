# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0005_auto_20150215_0006'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('date_published', 'id'), 'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
        migrations.AddField(
            model_name='issue',
            name='title',
            field=models.CharField(default=b'', max_length=200, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
    ]
