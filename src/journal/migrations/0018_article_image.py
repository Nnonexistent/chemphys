# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import journal.models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0017_auto_20141225_0314'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(default=b'', upload_to=journal.models.article_upload_to, verbose_name='Image', blank=True),
            preserve_default=True,
        ),
    ]
