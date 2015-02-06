# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0026_author_degree'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=2, verbose_name='Language', choices=[(b'ru', 'Russian'), (b'en', 'English')])),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('section', models.ForeignKey(verbose_name='Section', to='journal.Section')),
            ],
            options={
                'verbose_name': 'Section name',
                'verbose_name_plural': 'Section names',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='sectionname',
            unique_together=set([('lang', 'section')]),
        ),
    ]
