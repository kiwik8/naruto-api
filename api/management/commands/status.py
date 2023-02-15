from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Get status of the connection with the database"

    def handle(self, *args, **options):
        db_conn = connections['default']
        try:
            c = db_conn.cursor()
        except OperationalError:
            connected = False
            self.stdout.write(self.style.ERROR('Database is not connected'))
        else:
            connected = True
            self.stdout.write(self.style.SUCCESS('Database is connected'))