from bs4 import BeautifulSoup
import requests
import html
from api.models import Character, Category


class BaseScraper:
    def __init__(self, language='en'):
        self.soup = None
        self.BASE_URL = "https://naruto.fandom.com"
        self.character = Character
        self.category = Category

    def get_soup(self, url):
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, 'lxml')
        return self.soup

    def get_data(self):
        raise NotImplementedError

    def get_url(self, letter):
        if self.language == 'en':
            return f"https://naruto.fandom.com/wiki/Category:Characters?from={letter}"
        elif self.language == 'fr':
            return f"https://naruto.fandom.com/fr/wiki/Cat%C3%A9gorie:Personnages?from={letter}"