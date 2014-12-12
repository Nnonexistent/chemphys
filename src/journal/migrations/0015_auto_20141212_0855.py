# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0014_auto_20141212_0846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order', blank=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('year', models.PositiveIntegerField(verbose_name='Year')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Issue',
                'verbose_name_plural': 'Issue',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='article',
            name='volume',
        ),
        migrations.DeleteModel(
            name='Volume',
        ),
        migrations.AddField(
            model_name='article',
            name='issue',
            field=models.ForeignKey(blank=True, to='journal.Issue', null=True),
            preserve_default=True,
        ),
    ]
