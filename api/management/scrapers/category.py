from .base import BaseScraper
import logging
import api


class CategoryScraper(BaseScraper):
    def __init__(self, language='en'):
        super().__init__(language)
        self.letter = 'A'
        self.language = language


    def get_categories_characters(self):
        categories = self.category.objects.all()
        for category in categories:
            self.get_soup(category.url)
            div = self.soup.find("div", class_="category-page__members")
            names = div.find_all("a", class_="category-page__member-link")
            for name in names:
                name = name.text
                try:
                    character = self.character.objects.get(fr_name=name)
                except api.models.Character.DoesNotExist:
                    logging.debug(f"---{name} n'existe pas---")
                    continue
                if category not in character.fr_categories.all():
                    category.characters.add(character)
                else:
                    logging.debug(f"---{name} est déjà dans {category.name}---")
            logging.info(f"---{category.name} est complété---")