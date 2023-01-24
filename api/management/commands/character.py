from django.core.management.base import BaseCommand
from api.management.scrapers.character import CharacterScraper
from api.models import Character, Category

class Command(BaseCommand):
    help = "Add characters to the database"
    

    def handle(self, *args, **options):
        characters = Character.objects.all()
        for character in characters:
            character.image = character.image.replace('http://localhost:8000/', '')