# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import journal.models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0023_issue_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='issue',
            options={'ordering': ['order'], 'verbose_name': 'Issue', 'verbose_name_plural': 'Issues'},
        ),
        migrations.AddField(
            model_name='review',
            name='key',
            field=models.CharField(default=journal.models.default_key, unique=True, max_length=32, verbose_name='Key'),
            preserve_default=True,
        ),
    ]
