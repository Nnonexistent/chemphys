# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewfile',
            name='review',
        ),
        migrations.DeleteModel(
            name='ReviewFile',
        ),
        migrations.AlterModelOptions(
            name='organizationlocalizedcontent',
            options={'verbose_name': 'Organization localized content', 'verbose_name_plural': 'Organization localized content'},
        ),
        migrations.AlterField(
            model_name='articleattach',
            name='comment',
            field=models.TextField(default=b'', verbose_name='Comment to file', blank=True),
            preserve_default=True,
        ),
    ]
