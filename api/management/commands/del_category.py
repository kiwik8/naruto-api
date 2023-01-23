from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Delete categories from the database"

    def handle(self, *args, **options):
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted categories'))