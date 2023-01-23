from .base import BaseScraper
import re
from urllib.parse import unquote



class CharacterScraper(BaseScraper):
    def __init__(self, language='en'):
        super().__init__(language)
        self.letter = 'A'
        self.language = language

    
    def get_url(self, letter):
        if self.language == 'en':
            return f"https://naruto.fandom.com/wiki/Category:Characters?from={letter}"
        elif self.language == 'fr':
            return f"https://naruto.fandom.com/fr/wiki/Catégorie:Personnages?from={letter}"


    def scrape_info(self, soup):
        name = soup.find("meta", property="og:title")["content"]
        description = soup.find("meta", property="og:description")["content"]
        image = soup.find("meta", property="og:image")["content"]
        submenu_title = soup.find('h2', class_="pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background", text="Informations")
        if submenu_title is None:
            return name, description, image, {}
        infos = submenu_title.find_parent()
        submenus = infos.find_all("div", class_="pi-item pi-data pi-item-spacing pi-border-color")
        general_infos = {}
        for menu in submenus:
            key = menu["data-source"]
            value = menu.find("div", class_="pi-data-value pi-font").text
            general_infos[key] = value
        return name, description, image, general_infos

    def next_letter(self, letter):
        if letter == 'Z':
            return '¡'
        return chr(ord(letter) + 1)

    def create_category(self, url, list):
        match = re.search(r"Cat%C3%A9gorie:(.*)$", url).group(1)
        match = unquote(match)
        self.category.objects.create(name=match, url=url)
        print("---Categorie crée: ", match + "---")

    def get_characters(self):
        for i in range(26):
            self.get_soup(self.get_url(letter=self.letter))
            characters = self.soup.find_all("li", class_="category-page__member")
            for character in characters:
                link = character.find("a", class_="category-page__member-link")['href']
                url = self.BASE_URL + link
                if 'Cat' in url:
                    self.create_category(url, categories)
                    continue
                self.get_soup(url)
                name, description, image, general_infos = self.scrape_info(self.soup)
                character = self.character.objects.create(name=name, description=description, image=image, general_infos=general_infos)
                print(name)
            self.letter = self.next_letter(self.letter)
    