# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('journal', '0003_auto_20141106_0701'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalizedName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=2, verbose_name='Language', choices=[(b'ru', 'Russian'), (b'en', 'English')])),
                ('first_name', models.CharField(max_length=60, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=60, verbose_name='last name', blank=True)),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('user', 'lang'),
                'verbose_name': 'Localized name',
                'verbose_name_plural': 'Localized names',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ('user__last_name', 'user__first_name'), 'verbose_name': 'Author', 'verbose_name_plural': 'Authors'},
        ),
        migrations.AlterModelOptions(
            name='positioninorganization',
            options={'ordering': ['id'], 'verbose_name': 'Position in organization', 'verbose_name_plural': 'Position in organizations'},
        ),
        migrations.AlterModelOptions(
            name='volume',
            options={'ordering': ['order'], 'verbose_name': 'Volume', 'verbose_name_plural': 'Volumes'},
        ),
        migrations.RemoveField(
            model_name='author',
            name='first_name_en',
        ),
        migrations.RemoveField(
            model_name='author',
            name='first_name_ru',
        ),
        migrations.RemoveField(
            model_name='author',
            name='last_name_en',
        ),
        migrations.RemoveField(
            model_name='author',
            name='last_name_ru',
        ),
        migrations.RemoveField(
            model_name='author',
            name='organizations',
        ),
        migrations.RemoveField(
            model_name='positioninorganization',
            name='author',
        ),
        migrations.AddField(
            model_name='positioninorganization',
            name='user',
            field=models.ForeignKey(default=1, verbose_name='User', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='positioninorganization',
            name='organization',
            field=models.ForeignKey(verbose_name='Organization', to='journal.Organization'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='positioninorganization',
            name='position',
            field=models.CharField(max_length=200, verbose_name='Position'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='volume',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='Order', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='volume',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='volume',
            name='year',
            field=models.PositiveIntegerField(verbose_name='Year'),
            preserve_default=True,
        ),
    ]
