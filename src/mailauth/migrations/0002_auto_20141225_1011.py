# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import mailauth.models


class Migration(migrations.Migration):

    dependencies = [
        ('mailauth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailauthtoken',
            name='user',
        ),
        migrations.AddField(
            model_name='mailauthtoken',
            name='email',
            field=models.EmailField(default='', max_length=75, verbose_name='E-mail'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mailauthtoken',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mailauthtoken',
            name='key',
            field=models.CharField(default=mailauth.models.default_key, unique=True, max_length=32, verbose_name='Key'),
            preserve_default=True,
        ),
    ]
