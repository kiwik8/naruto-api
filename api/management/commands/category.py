from django.core.management.base import BaseCommand
from api.management.scrapers.category import CategoryScraper

class Command(BaseCommand):
    help = "Add characters to the database"
    

    def handle(self, *args, **options):
        scraper = CategoryScraper('fr')
        scraper.get_categories_characters()