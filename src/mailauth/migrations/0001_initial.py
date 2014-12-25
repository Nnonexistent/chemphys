# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mailauth.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MailAuthToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(default=mailauth.models.default_key, unique=True, max_length=64, verbose_name='Key')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Mail auth token',
                'verbose_name_plural': 'Mail auth tokens',
            },
            bases=(models.Model,),
        ),
    ]
