"""
Troy Hunt's RSS Feed for the last 50 pastes

http://feeds.feedburner.com/HaveIBeenPwnedLatestPastes

"""
import feedparser

from .Site import Site
from .Paste import Paste
from bs4 import BeautifulSoup
from . import helper
from time import sleep
from settings import SLEEP_HAVEIBEEN
from twitter import TwitterError
import logging

class HaveIBeenPaste(Paste):
    def __init__(self, id):
        super(HaveIBeenPaste, self).__init__(id)
        self.headers = None
        self.url = 'http://pastebin.com/raw.php?i=' + self.id
        
    def get(self):
        return helper.curl(self.url)
        
class HaveIBeen(Site):
    def __init__(self):
        super(HaveIBeen, self).__init__()
        self.sleep = SLEEP_HAVEIBEEN
        logging.info('[+] Started HaveIBeen')
        self.feedURL = 'http://feeds.feedburner.com/HaveIBeenPwnedLatestPastes'
        
    def _parse(self):
        try:
            d = feedparser.parse(self.feedURL)
            return d['entries']
        except Exception as e:
            logging.error('[!] Feed Parser Error: %s'%(str(e)))
            return None
        
    def update(self):
        logging.info('Retrieving HaveIBeenPwned ID\'s')
        i=0 
        
        for entry in self._parse():
            l = entry['links'][0]['href']
            link = l.split(r'/')
            paste = HaveIBeenPaste(link[3])
            if not self.hasSeen(paste):
                i+=1
                self.put(paste)
        logging.info('HaveIBeenPwned Added URLs: ' + str(i))

           


if __name__ == '__main__':
    c = HaveIBeen()
    c.update()