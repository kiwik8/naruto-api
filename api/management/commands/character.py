from django.core.management.base import BaseCommand
from api.management.scrapers.character import CharacterScraper
from api.models import Character, Category
import logging

class Command(BaseCommand):
    help = "Add characters to the database"


    def handle(self, *args, **options):
        character = CharacterScraper(language='en')
        character.get_characters()
        logging.info("DELETE ALL DOUBLES...")
        i = 0
        all = Character.objects.all().reverse()
        for row in all:
            if Character.objects.filter(en_name=row.en_name).count() > 1 and row.en_name is not None:
                logging.info(f"---Character deleted: {row.en_name} ---")
                row.delete()
                i+=1
        logging.info(f"---{i} characters deleted ---")
        self.stdout.write(self.style.SUCCESS('Successfully added en characters'))
        character = CharacterScraper(language='fr')
        character.get_characters()
        logging.info("DELETE ALL DOUBLES...")
        all = Character.objects.all().reverse()
        i = 0
        for row in all:
            if Character.objects.filter(fr_name=row.fr_name).count() > 1 and row.fr_name is not None:
                logging.info(f"---Character deleted: {row.fr_name} ---")
                row.delete()
                i+=1
        logging.info(f"---{i} characters deleted ---")
        self.stdout.write(self.style.SUCCESS('Successfully added fr characters'))
