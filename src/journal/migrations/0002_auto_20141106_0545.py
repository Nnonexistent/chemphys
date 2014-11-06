# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['order'], 'verbose_name': 'Section', 'verbose_name_plural': 'Sections'},
        ),
        migrations.AddField(
            model_name='section',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='Order', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='author',
            name='user',
            field=models.OneToOneField(verbose_name='User', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderedauthors',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='Order', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderedorganizations',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='Order', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='address',
            field=models.TextField(default=b'', verbose_name='Address', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='city',
            field=models.CharField(default=b'', max_length=100, verbose_name='City', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='country',
            field=models.CharField(default=b'', max_length=100, verbose_name='Country', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.TextField(verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='obsolete',
            field=models.BooleanField(default=False, verbose_name='Obsolete'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='previous',
            field=models.ManyToManyField(related_name='previous_rel_+', verbose_name='Previous versions', to='journal.Organization', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='site',
            field=models.URLField(default=b'', verbose_name='Site URL', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='section',
            name='moderators',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Moderators', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staffmember',
            name='chief_editor',
            field=models.BooleanField(default=False, verbose_name='Chief editor'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staffmember',
            name='editor',
            field=models.BooleanField(default=False, verbose_name='Editor'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staffmember',
            name='reviewer',
            field=models.BooleanField(default=False, verbose_name='Reviewer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staffmember',
            name='user',
            field=models.OneToOneField(verbose_name='User', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
