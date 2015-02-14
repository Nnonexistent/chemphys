# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0004_auto_20150214_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='lang',
            field=models.CharField(default=b'en', max_length=2, verbose_name='Article language', choices=[(b'ru', 'Russian'), (b'en', 'English')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='report',
            field=models.FileField(default=b'', upload_to=b'expert_reports', verbose_name='\u0410\u043a\u0442 \u044d\u043a\u0441\u043f\u0435\u0440\u0442\u0438\u0437\u044b', blank=True),
            preserve_default=True,
        ),
    ]
