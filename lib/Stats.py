from pymongo import MongoClient
from bson import Code
from twitter import TwitterError
from settings import USE_DB, DB_HOST, DB_PORT, STATS_FREQ

import logging
import time

class Stats(object):
    def __init__(self):
        if USE_DB:
            try:
                self.client = MongoClient(DB_HOST, DB_PORT).paste_db.pastes        
            except pymongo.errors.ConnectionFailure, e:
                logging.error('[!] Database failed to start %s'%(e))
                
    def uniqueEmailSet(self):
            map = Code("function () {"
                       " this.emails.forEach(function(z) {"
                       "    emit(z,1);"
                       "    });"
                       "}")
            reduce = Code("function (key,values) {"
                          "var total = 0;"
                          "for (var i = 0; i <values.length; i++) {"
                          "    total += values[i];"
                          "}"
                          "return total;"
                        "}")
            result = self.client.map_reduce(map,reduce,"res") 
            return result  
        
    def uniqueHashSet(self):
            map = Code("function () {"
                       " this.hashes.forEach(function(z) {"
                       "    emit(z,1);"
                       "    });"
                       "}")
            reduce = Code("function (key,values) {"
                          "var total = 0;"
                          "for (var i = 0; i <values.length; i++) {"
                          "    total += values[i];"
                          "}"
                          "return total;"
                        "}")
            result = self.client.map_reduce(map,reduce,"res") 
            return result 

    def status(self):
        if not USE_DB:
            logging.warning("[!] Not going to produce Stats because DB is off.")
            return None
        try:
            e = self.uniqueEmailSet().count()
            h = self.uniqueHashSet().count()
            msg =  "Status as of %s: \n Unique emails: %i, Unique hashes: %i\n #infosec #dataleak"%(time.strftime("%c"),e,h)    
            return msg
        except Exception,e:
            logging.error('[!] Database Error %s'%(e))
            return None
                                                      
    def monitor(self,twitterBot):
        try:
            msg = self.status()
            if msg:
                with twitterBot.tweetLock:
                    try:
                        logging.debug('[+] Status Tweet %s'%(msg))
                        twitterBot.statuses.update(status=msg)
                    except TwitterError as e:
                        logging.debug('[!] TwitterError %s'%(str(e)))
        except Exception,e:
            logging.error('[!] Database Error %s'%(e))
            
        time.sleep(STATS_FREQ)
            
            
            