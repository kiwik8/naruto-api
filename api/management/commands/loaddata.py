from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Loads data from base data'

    def add_arguments(self, parser):
        parser.add_argument('fixture', nargs='+', type=str)

    def handle(self, *args, **options):
        from django.core.management import call_command
        for fixture in options['fixture']:
            call_command('loaddata', fixture)