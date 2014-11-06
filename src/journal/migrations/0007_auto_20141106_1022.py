# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0006_auto_20141106_0939'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ArticleAuthors',
            new_name='ArticleAuthor',
        ),
        migrations.AddField(
            model_name='review',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'Pending'), (1, 'Unfinished'), (2, 'Done')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.FileField(default=b'', upload_to=b'published', verbose_name='Content', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='articleauthor',
            unique_together=set([('article', 'position')]),
        ),
    ]
