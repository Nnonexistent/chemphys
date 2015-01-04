# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0020_auto_20150104_1502'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='positioninorganization',
            unique_together=set([('user', 'organization')]),
        ),
    ]
