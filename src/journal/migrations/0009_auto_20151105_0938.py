# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0008_remove_issue_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-date_published', 'id'), 'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
        migrations.AlterField(
            model_name='article',
            name='lang',
            field=models.CharField(default=b'ru', max_length=2, verbose_name='Article language', choices=[(b'ru', 'Russian'), (b'en', 'English')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='old_number',
            field=models.SmallIntegerField(help_text='to link consistency with old articles', null=True, verbose_name='Old number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journaluser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journaluser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='localizedarticlecontent',
            name='title',
            field=models.TextField(default=b'', verbose_name='Title', blank=True),
            preserve_default=True,
        ),
    ]
