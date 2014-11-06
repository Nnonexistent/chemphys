# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0004_auto_20141106_0746'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='localizedname',
            unique_together=set([('user', 'lang')]),
        ),
    ]
