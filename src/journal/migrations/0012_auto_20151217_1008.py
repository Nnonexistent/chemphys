# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0011_article_old_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journaluser',
            name='email',
            field=models.EmailField(max_length=75, verbose_name='email address'),
            preserve_default=True,
        ),
    ]
