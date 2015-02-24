from django.core.management.base import BaseCommand, CommandError

from udc.models import Concept


class Command(BaseCommand):
    args = '<filename>'
    help = 'Updates UDC concepts'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError(u'Please specify udc.rdf file path')
        source_file = args[0]

        try:
            Concept.load(source_file)
        except (IOError, ), e:
            raise CommandError(e)
