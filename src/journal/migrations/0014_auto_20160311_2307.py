# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import journal.models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0013_auto_20160220_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='report',
            field=models.FileField(default=b'', upload_to=journal.models.report_upload_to, verbose_name='\u0410\u043a\u0442 \u044d\u043a\u0441\u043f\u0435\u0440\u0442\u0438\u0437\u044b', blank=True),
            preserve_default=True,
        ),
    ]
