from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

class Command(BaseCommand):

    args = '<dir>'
    help = 'Manages lucene search engine'

    option_list = BaseCommand.option_list + (
        make_option(
            '--param',
            action='store_true',
            dest='param',
            default=False,
            help='param help',
        ),
    )

    def handle(self, *args, **options):
        if options['param']:
            pass
        elif options['param2']:
            pass
        else:
            raise CommandError('Bad syntax!')