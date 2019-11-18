import requests
from bs4 import BeautifulSoup


class Website:
    SEARCH_ENDPOINT = 'http://yalerecord.org/?s='

    def url_safe(self, string):
        return string.replace(' ', '+')

    def search(self, query):
        text = requests.get(self.SEARCH_ENDPOINT + self.url_safe(query)).text
        bs = BeautifulSoup(text, 'html.parser')
        link = bs.find('a', {'rel': 'bookmark'})
        if link is None:
            return 'No results found.'
        return link['href']
