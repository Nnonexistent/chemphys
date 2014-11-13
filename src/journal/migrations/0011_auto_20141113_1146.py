# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0010_articleattach'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalizedArticleContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=2, verbose_name='Language', choices=[(b'ru', 'Russian'), (b'en', 'English')])),
                ('title', models.TextField(verbose_name='Title')),
                ('abstract', models.TextField(verbose_name='Abstract')),
                ('article', models.ForeignKey(verbose_name='Article', to='journal.Article')),
            ],
            options={
                'ordering': ('article', 'lang'),
                'verbose_name': 'Localized article content',
                'verbose_name_plural': 'Localized article content',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='localizedarticlecontent',
            unique_together=set([('article', 'lang')]),
        ),
        migrations.RemoveField(
            model_name='article',
            name='abstract',
        ),
        migrations.RemoveField(
            model_name='article',
            name='title',
        ),
        migrations.AlterField(
            model_name='localizedname',
            name='first_name',
            field=models.CharField(max_length=60, verbose_name='First name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='localizedname',
            name='last_name',
            field=models.CharField(max_length=60, verbose_name='Last name', blank=True),
            preserve_default=True,
        ),
    ]
