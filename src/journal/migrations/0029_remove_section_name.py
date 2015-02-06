# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0028_auto_20150206_0951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='name',
        ),
    ]
