from .base import BaseScraper
import re
from urllib.parse import unquote
import concurrent.futures
import random
import logging
from time import sleep
from unicodedata import normalize



class CharacterScraper(BaseScraper):
    def __init__(self, language='en'):
        super().__init__(language)
        self.letter = 'A'
        self.language = language
        logging.basicConfig(level=logging.INFO)

    
    def get_url(self, letter):
        if self.language == 'en':
            return f"https://naruto.fandom.com/wiki/Category:Characters?from={letter}"
        elif self.language == 'fr':
            return f"https://naruto.fandom.com/fr/wiki/Catégorie:Personnages?from={letter}"


    def scrape_info(self, soup):
        name = soup.find("meta", property="og:title")["content"]
        description = soup.find("meta", property="og:description")["content"]
        image = soup.find("meta", property="og:image")["content"]
        if self.language == 'fr':
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
        elif self.language == 'en':
            def find_header(tag):
                return tag.name == 'th' and 'mainheader' in tag.get('class', []) and 'Personal' in tag.text
            # submenu_title = soup.find('th', class_="mainheader", text="Personal")
            submenu_title = soup.find(find_header)
            if submenu_title is None:
                print("No submenu finded")
                return name, description, image, {}
            tr = submenu_title.find_parent()
            tbody = tr.find_parent()
            submenus = tbody.find_all("tr")
            i = 0
            general_infos = {}
            for menu in submenus:
                submenu_title = menu.find(find_header)
                if i == 1:
                    next_submenu = menu.find('th', class_="mainheader")
                    if next_submenu is not None:
                        i = 0
                        continue
                    key = menu.find('th').get_text()
                    value = menu.find("td").get_text()
                    key = key.strip().capitalize().replace("\n", "").replace("\t", "")
                    value = value.strip().capitalize().replace("\n", "").replace("\t", "").replace("<br />", " ")
                    general_infos[key] = value
                if submenu_title is not None:
                    i = 1
        return name, description, image, general_infos

    def next_letter(self, letter):
        if letter == 'Z':
            return '¡'
        return chr(ord(letter) + 1)

    def create_category(self, url):
        match = re.search(r"Cat%C3%A9gorie:(.*)$", url).group(1)
        match = unquote(match)
        self.category.objects.create(name=match, url=url)
        logging.info("---Categorie crée: {} ---".format(match))

    def get_character(self, character):
        link = character.find("a", class_="category-page__member-link")['href']
        url = self.BASE_URL + link
        if 'Cat' in url:
            self.create_category(url)
            return None
        self.get_soup(url)
        name, description, image, general_infos = self.scrape_info(self.soup)
        for key, value in general_infos.items():
            if isinstance(value, str):
                general_infos[key] = value.replace('\xa0', ' ')
        if self.language == 'fr':
            self.character.objects.create(fr_name=name, fr_description=description, image=image, fr_general_infos=general_infos)
        elif self.language == 'en':
            self.character.objects.create(en_name=name, en_description=description, image=image, en_general_infos=general_infos)
        logging.info(msg=f"---Personnage crée: {name} ---")

    def get_characters(self):
        for i in range(27):
            logging.debug(msg=f"---Lettre: {self.letter}---")
            self.soup = self.get_soup(self.get_url(letter=self.letter))
            characters = self.soup.find_all("li", class_="category-page__member")
            # partie qui permet de sérialiser les requêtes
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(self.get_character, character) for character in characters]
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                    except Exception as e:
                        logging.error(msg=f"---Erreur: {e}---")
            self.letter = self.next_letter(self.letter)
    