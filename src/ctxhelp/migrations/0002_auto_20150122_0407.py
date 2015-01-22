# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ctxhelp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hiddenhelp',
            name='hash',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hiddenhelp',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='hiddenhelp',
            unique_together=set([('user', 'hash')]),
        ),
        migrations.RemoveField(
            model_name='hiddenhelp',
            name='key',
        ),
    ]
