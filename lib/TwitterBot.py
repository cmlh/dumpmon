from twitter import *
from settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, log_file
import logging
import time
import threading

class TwitterBot(Twitter):
    """
    Subclassing the Twitter API and botifying it
    """
    def __init__(self):
        super(TwitterBot, self).__init__(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
            CONSUMER_KEY, CONSUMER_SECRET))
        
        self.tweetLock= threading.Lock()

    def test(self):
        while(True):
            print("Doing stuff")
            time.sleep(2)
           
    def monitor(self):
        twitter_userstream = TwitterStream(auth=self.auth, domain='userstream.twitter.com')
        try:
            for msg in twitter_userstream.user():
                if 'text' in msg:
                    print("[$] Recieved Tweet %s from %s"%(msg['text'],msg['user']['screen_name']))

        except StopIteration:
            print("stopping iteration")
            