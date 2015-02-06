# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def localize_sections(apps, schema_editor):
    Section = apps.get_model("journal", "Section")
    SectionName = apps.get_model("journal", "SectionName")

    # we can't invoke Section.name because it will use
    # BaseLocalizedObject._get_localized method via corresponding property
    names = dict(Section.objects.all().values_list('id', 'name'))

    for section in Section.objects.all():
        SectionName.objects.get_or_create(section=section, lang=settings.LANGUAGE_CODE,
                                          defaults={'name': names[section.id]})


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0027_auto_20150206_0950'),
    ]

    operations = [
        migrations.RunPython(localize_sections)
    ]
