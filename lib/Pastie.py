from .Site import Site
from .Paste import Paste
from bs4 import BeautifulSoup
from . import helper
from time import sleep
from settings import SLEEP_PASTIE
from twitter import TwitterError
import logging


class PastiePaste(Paste):
    def __init__(self, id):
        super(PastiePaste, self).__init__(id)
        self.headers = None
        self.url = 'http://pastie.org/pastes/' + self.id + '/text'

class Pastie(Site):
    def __init__(self, last_id=None):
        if not last_id:
            last_id = None
        self.ref_id = last_id
        self.BASE_URL = 'http://pastie.org'
        self.sleep = SLEEP_PASTIE
        super(Pastie, self).__init__()
        
    def parse(self):
        return [tag for tag in BeautifulSoup(helper.download(
            self.BASE_URL + '/pastes')).find_all('p', 'link') if tag.a]

    def update(self):
        '''update(self) - Fill Queue with new Pastie IDs'''
        logging.info('Retrieving Pastie ID\'s')
        i=0    
        for entry in self.parse():
            paste = PastiePaste(entry.a['href'].replace(
                self.BASE_URL + '/pastes/', ''))
            if not self.hasSeen(paste):
                i+=1
                self.put(paste)
        logging.info('Pastie Added URLs: ' + str(i))

    def get_paste_text(self, paste):
        return BeautifulSoup(helper.download(paste.url)).pre.text