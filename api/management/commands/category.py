from django.core.management.base import BaseCommand
from api.management.scrapers.category import CategoryScraper
from api.models import Category

class Command(BaseCommand):
    help = "Add characters to the database"
    

    def handle(self, *args, **options):
        scraper = CategoryScraper()
        scraper.get_categories_characters()
        categories = Category.objects.all().reverse()
        for category in categories:
            if Category.objects.filter(name=category.name).count() > 1:
                category.delete()