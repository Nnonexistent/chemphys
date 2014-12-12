# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0012_auto_20141210_1308'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationLocalizedContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=2, verbose_name='Language', choices=[(b'ru', 'Russian'), (b'en', 'English')])),
                ('name', models.TextField(verbose_name='Name')),
                ('country', models.CharField(default=b'', max_length=100, verbose_name='Country', blank=True)),
                ('city', models.CharField(default=b'', max_length=100, verbose_name='City', blank=True)),
                ('address', models.TextField(default=b'', verbose_name='Address', blank=True)),
                ('org', models.ForeignKey(to='journal.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='organizationlocalizedcontent',
            unique_together=set([('lang', 'org')]),
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['short_name'], 'verbose_name': 'Organization', 'verbose_name_plural': 'Organizations'},
        ),
        migrations.RemoveField(
            model_name='organization',
            name='address',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='city',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='country',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='name',
        ),
    ]
