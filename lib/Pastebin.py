from .Site import Site
from .Paste import Paste
from bs4 import BeautifulSoup
from . import helper
from time import sleep
from settings import SLEEP_PASTEBIN
from twitter import TwitterError
import logging


class PastebinPaste(Paste):
    def __init__(self, id):
        super(PastebinPaste, self).__init__(id)
        self.headers = None
        self.url = 'http://pastebin.com/raw.php?i=' + self.id

class Pastebin(Site):
    def __init__(self):
        self.BASE_URL = 'http://pastebin.com'
        self.sleep = SLEEP_PASTEBIN
        super(Pastebin, self).__init__()
        logging.info('[+] Started PasteBin')
        
    def parse(self):
        return BeautifulSoup(helper.download(self.BASE_URL + '/archive')).find_all(
            lambda tag: tag.name == 'td' and tag.a and '/archive/' not in tag.a['href'] and tag.a['href'][1:])        
        
    def update(self):
        '''update(self) - Fill Queue with new Pastebin IDs'''
        logging.info('Retrieving Pastebin ID\'s')
        i=0            
        for entry in self.parse():
            paste = PastebinPaste(entry.a['href'][1:])
            if not self.hasSeen(paste):
                #logging.info('Adding URL: ' + paste.url)
                i+=1
                self.put(paste)
        logging.info('Pastebin Added URLs: ' + str(i))
           
    def get_paste_text(self, paste):
        return helper.download(paste.url)
