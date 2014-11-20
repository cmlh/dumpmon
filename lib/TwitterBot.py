from twitter import *
from settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, log_file, TWITTER_SCREEN_NAME
import logging
import time
import threading
from lib.Stats import Stats

class TwitterBot(Twitter):
    """
    Subclassing the Twitter API and botifying it
    """
    def __init__(self,regexMgr):
        super(TwitterBot, self).__init__(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
            CONSUMER_KEY, CONSUMER_SECRET))
        
        self.tweetLock= threading.Lock()
        
        self.regexMgr = regexMgr
        self.statusMgr = Stats()
    
    def status(self,aryDM,user):
        return self.statusMgr.status()
        
    def addregex(self,aryDM,user):
        """
        The add regex assumes that ary[0] = 'addregex' and ary[1] = 'theregex'
        """
        response = None
        if self.regexMgr.add(aryDM[1],user):  
            response = "Your regex has been added! Thanks!"
        else:
            response  = "I could not add your regex, it didn't validate. :("
        return response
    
    def _parseTweet(self,dm,t):
        """
        Probably should make this a protocol, but we'll see
        """  
        logging.info('[+] Processing DM request: %s Screen Name: %s'%(dm['text'],dm['sender']['screen_name']))  
        response = None
        #assume that we are going to use a space delim protocol and the ary[0] is the function name to call.
        aryDM = dm['text'].split()
        f = getattr(self,aryDM[0])
        if f:
            response = f(aryDM,dm['sender']['screen_name']) 
            logging.info('[+] Sending DM response: %s Screen Name: %s'%(response,dm['sender']['screen_name'])) 
        else:
            logging.error('[!] Could not find function in protocol: %s Screen Name: %s'%(aryDM[0],dm['sender']['screen_name']))
                          
        if response:
            with self.tweetLock:
                try:
                    self.direct_messages.new(user=dm['sender']['screen_name'],text=response)
                except TwitterError as e:
                    logging.debug('[!] TwitterError %s'%(str(e)))
                
    def monitor(self):
        """
        This function is expected to be on a separate thread.
        This stream function is blocking and will not yield, thus does not need to be in a loop; refer to the docs
        """
        twitter_userstream = TwitterStream(auth=self.auth, domain='userstream.twitter.com')
        try:
            for msg in twitter_userstream.user():
                #logging.debug("{^} %s"%(msg))
                if 'text' in msg:
                    print("[$] Recieved Tweet %s from %s"%(msg['text'],msg['user']['screen_name']))
                
                #process DMs, but only from other people     
                if 'direct_message' in msg and msg['direct_message']['sender']['screen_name'] != TWITTER_SCREEN_NAME:
                    self._parseTweet(msg['direct_message'],msg)

        except StopIteration:
            print("stopping iteration")
            
            
            
            
            
            
            