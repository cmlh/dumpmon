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
            paste.text = self.get_paste_text(paste)
            tweet = helper.build_tweet(paste)
            if tweet:
                logging.info(tweet)
                with bot.tweetLock:
                    if USE_DB:
                        self.db_client.save({
                            'pid' : paste.id,
                            'text' : paste.text,
                            'emails' : paste.emails,
                            'hashes' : paste.hashes,
                            'num_emails' : paste.num_emails,
                            'num_hashes' : paste.num_hashes,
                            'type' : paste.type,
                            'db_keywords' : paste.db_keywords,
                            'url' : paste.url
                           })
                    try:
                        logging.debug('[+] Tweet %s'%(tweet))
                        bot.statuses.update(status=tweet)
                        return tweet
                    except TwitterError as e:
                        logging.debug('[!] TwitterError %s'%(str(e)))

           
    def get_paste_text(self, paste):
        return helper.download(paste.url)