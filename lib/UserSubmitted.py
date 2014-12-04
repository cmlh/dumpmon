from .Site import Site
from .Paste import Paste
from bs4 import BeautifulSoup
from . import helper
import time
from settings import USE_DB
from twitter import TwitterError
import logging
from urlunshort import resolve

class UserSubmittedPaste(Paste):
    def __init__(self, url):
        super(UserSubmittedPaste, self).__init__(url)
        self.headers = None
        self.url = resolve(url)
        logging.info('[+] URL expanded to %s'%(self.url))

    def get(self):
        self.text =  helper.curl(self.url)

class UserSubmitted(Site):
    def __init__(self):
        super(UserSubmitted, self).__init__()
        logging.info('[+] Started UserSubmitted')
        
    def parse(self):
        pass       
        
    def update(self,url):
        paste = UserSubmittedPaste(url)
        if not self.hasSeen(paste):
            logging.info('Adding User Sumbmitted URL: ' + paste.url)
            self.put(paste)

    def monitor(self, bot):
        if not self.empty():
            paste = self.get()
            logging.info('[*] Checking ' + paste.url)
            paste.get()
            tweet = helper.build_tweet(paste)
            if tweet:
                logging.info(tweet)
                with bot.tweetLock:
                    if USE_DB:
                        self.db_client.save(repr(paste))
                    try:
                        logging.debug('[+] Tweet %s'%(tweet))
                        bot.statuses.update(status=tweet)
                        return tweet
                    except TwitterError as e:
                        logging.debug('[!] TwitterError %s'%(str(e)))

           
