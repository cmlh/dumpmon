import re
from pymongo import MongoClient
from settings import USE_DB, DB_HOST, DB_PORT
import time
import logging

import threading

class RegexMgr(object):
    """
    This class is intended to handle all the regex stuff and persistance to the DB for observers
    """
    def __init__(self):        
        self.regexLock = threading.Lock()
        
        if USE_DB:
            try:
                self.client = MongoClient(DB_HOST, DB_PORT).paste_db.regexes        
            except pymongo.errors.ConnectionFailure, e:
                logging.error('[!] Database failed to start %s'%(e))
                
        self.customRegexes = []  
        self._loadRegexes()

    
    def _loadRegexes(self):
        with self.regexLock:
            cursor = self.client.find()
            for row in cursor:
                customRegex = {}
                rc = re.compile(row['regex'])
                customRegex['regex'] = rc
                customRegex['user'] = row['user']
                customRegex['added'] = time.strftime("%c")
                self.customRegexes.append(customRegex)
                           
            logging.info("[+] Loaded custom regexes: %s"%(self.customRegexes))  
    
    def reloadCustomRegexes(self):
        self.customRegexes = []
        self._loadRegexes()
                      
    def add(self,regex, user):
        if self.valid(regex):
            o = {"user":user,"regex":regex,"added":time.strftime("%c")}
            self.client.insert(o)
            self.customRegexes.append(o)
            return True
        
    def valid(self,regex):        
        try:
            re.compile(regex)
            is_valid = True
        except re.error:
            is_valid = False
        return is_valid
    
    
    
    
    