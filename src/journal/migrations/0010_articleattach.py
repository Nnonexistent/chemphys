# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0009_auto_20141106_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleAttach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order', blank=True)),
                ('type', models.PositiveSmallIntegerField(default=0, verbose_name='Attach type', choices=[(0, 'Generic'), (1, 'Image'), (2, 'Video')])),
                ('file', models.FileField(upload_to=b'attaches', verbose_name='File')),
                ('comment', models.TextField(default=b'', verbose_name='Comment', blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('article', models.ForeignKey(verbose_name='Article', to='journal.Article')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Article attach',
                'verbose_name_plural': 'Article attaches',
            },
            bases=(models.Model,),
        ),
    ]
