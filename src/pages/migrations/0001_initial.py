# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order', blank=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('url', models.SlugField(unique=True, verbose_name='URL part')),
                ('content', models.TextField(default=b'', verbose_name='Content', blank=True)),
                ('in_menu', models.BooleanField(default=False, verbose_name='Visible in menu')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
            bases=(models.Model,),
        ),
    ]
