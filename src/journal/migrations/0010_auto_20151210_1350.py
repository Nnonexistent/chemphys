# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0009_auto_20151105_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='old_number',
        ),
        migrations.AlterField(
            model_name='journaluser',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', to='auth.Group', verbose_name='groups', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journaluser',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Specific permissions for this user.', to='auth.Permission', verbose_name='user permissions', blank=True),
            preserve_default=True,
        ),
    ]
