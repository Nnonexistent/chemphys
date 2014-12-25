# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('journal', '0016_auto_20141212_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalizedUser',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user', models.Model),
        ),
        migrations.AddField(
            model_name='localizedarticlecontent',
            name='references',
            field=models.TextField(default=b'', verbose_name='References', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='author',
            name='user',
            field=models.OneToOneField(verbose_name='User', to='journal.LocalizedUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='localizedname',
            name='user',
            field=models.ForeignKey(verbose_name='User', to='journal.LocalizedUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='positioninorganization',
            name='user',
            field=models.ForeignKey(verbose_name='User', to='journal.LocalizedUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(verbose_name='Reviewer', to='journal.LocalizedUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='section',
            name='moderators',
            field=models.ManyToManyField(to='journal.LocalizedUser', verbose_name='Moderators', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staffmember',
            name='user',
            field=models.OneToOneField(verbose_name='User', to='journal.LocalizedUser'),
            preserve_default=True,
        ),
    ]
