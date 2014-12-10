# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalizedPageContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=2, verbose_name='Language', choices=[(b'ru', 'Russian'), (b'en', 'English')])),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('content', models.TextField(default=b'', verbose_name='Content', blank=True)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
            ],
            options={
                'ordering': ['lang'],
                'verbose_name': 'Localized page content',
                'verbose_name_plural': 'Localized page contents',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='localizedpagecontent',
            unique_together=set([('page', 'lang')]),
        ),
        migrations.RemoveField(
            model_name='page',
            name='content',
        ),
        migrations.RemoveField(
            model_name='page',
            name='title',
        ),
    ]
