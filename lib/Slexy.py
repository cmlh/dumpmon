from .Site import Site
from .Paste import Paste
from bs4 import BeautifulSoup
from . import helper
from time import sleep
from settings import SLEEP_SLEXY
from twitter import TwitterError
import logging


class SlexyPaste(Paste):
    def __init__(self, id):
        super(SlexyPaste, self).__init__(id)
        self.headers = {'Referer': 'http://slexy.org/view/' + self.id}
        self.url = 'http://slexy.org/raw/' + self.id

class Slexy(Site):
    def __init__(self):
        self.BASE_URL = 'http://slexy.org'
        self.sleep = SLEEP_SLEXY
        super(Slexy, self).__init__()
        logging.info('[+] Started Slexy')
        
    def parse(self):
        return BeautifulSoup(helper.curl(self.BASE_URL + '/recent')).find_all(
            lambda tag: tag.name == 'td' and tag.a and '/view/' in tag.a['href'])  
        
    def update(self):
        '''update(self) - Fill Queue with new Slexy IDs'''
        logging.info('[*] Retrieving Slexy ID\'s')

        i=0   
        for entry in self.parse():
            paste = SlexyPaste(entry.a['href'].replace('/view/', ''))
            if not self.hasSeen(paste):
                i+=1
                self.put(paste)
        logging.info('Slexy Added URLs: ' + str(i))

    def get_paste_text(self, paste):
        return helper.curl(paste.url, paste.headers['Referer'])
