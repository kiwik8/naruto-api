from .base import BaseScraper
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
                    character = self.character.objects.get(name=name)
                except api.models.Character.DoesNotExist:
                    print(f"---{name} n'existe pas---")
                    continue
                category.characters.add(character)
                print(f"---{character.name} ajouté à {category.name}---")