# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(db_index=True, max_length=2, verbose_name='Language', choices=[(b'ru', 'Russian'), (b'en', 'English')])),
                ('about', models.URLField()),
                ('notation', models.CharField(max_length=32)),
                ('broader', models.URLField()),
                ('related', models.TextField(default=b'')),
                ('label', models.TextField()),
                ('notes', models.TextField(default=b'')),
            ],
            options={
                'ordering': ['notation'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='concept',
            unique_together=set([('lang', 'notation'), ('lang', 'about')]),
        ),
    ]
