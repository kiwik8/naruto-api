from django.core.management.base import BaseCommand
from api.management.scrapers.character import CharacterScraper

class Command(BaseCommand):
    help = "Add characters to the database"
    

    def handle(self, *args, **options):
        scraper = CharacterScraper('fr')
        scraper.get_characters()