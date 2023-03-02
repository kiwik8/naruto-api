from bs4 import BeautifulSoup
import requests
import html
from api.models import Character, Category
import logging


class BaseScraper:
    def __init__(self, language='en'):
        self.soup = None
        self.BASE_URL = "https://naruto.fandom.com"
        self.character = Character
        self.category = Category
        self.language = language
        self.session = requests.Session()
        logging.basicConfig(level=logging.INFO)

    def get_soup(self, url):
        response = self.session.get(url)
        self.soup = BeautifulSoup(response.text, 'lxml')
        return self.soup


    def get_url(self, letter):
        if self.language == 'en':
            return f"https://naruto.fandom.com/wiki/Category:Characters?from={letter}"
        elif self.language == 'fr':
            return f"https://naruto.fandom.com/fr/wiki/Cat%C3%A9gorie:Personnages?from={letter}"