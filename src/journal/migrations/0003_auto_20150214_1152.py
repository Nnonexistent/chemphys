# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_auto_20150214_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalizedIssueContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=2, verbose_name='Language', choices=[(b'ru', 'Russian'), (b'en', 'English')])),
                ('description', models.TextField(default='', verbose_name='Description', blank=True)),
                ('issue', models.ForeignKey(verbose_name='Issue', to='journal.Issue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='localizedissuecontent',
            unique_together=set([('lang', 'issue')]),
        ),
        migrations.RemoveField(
            model_name='issue',
            name='description',
        ),
    ]
