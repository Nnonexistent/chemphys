# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0010_auto_20151210_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='old_number',
            field=models.CharField(default=b'', help_text='to link consistently with old articles', max_length=20, verbose_name='Old number', blank=True),
            preserve_default=True,
        ),
    ]
