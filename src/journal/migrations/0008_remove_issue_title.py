# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0007_localizedissuecontent_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='title',
        ),
    ]
