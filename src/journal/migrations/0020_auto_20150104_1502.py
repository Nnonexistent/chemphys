# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0019_auto_20141229_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleauthor',
            name='author',
            field=models.ForeignKey(default=1, verbose_name='Author', to='journal.LocalizedUser'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articleauthor',
            name='organization',
            field=models.ForeignKey(default=1, verbose_name='Organization', to='journal.Organization'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='articleauthor',
            unique_together=set([('article', 'author', 'organization')]),
        ),
        migrations.RemoveField(
            model_name='articleauthor',
            name='position',
        ),
    ]
