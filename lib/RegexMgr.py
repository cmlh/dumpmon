import re
from pymongo import MongoClient
from settings import USE_DB, DB_HOST, DB_PORT

class RegexMgr(object):
    def __init__(self):
        if USE_DB:
            try:
                self.client = MongoClient(DB_HOST, DB_PORT).paste_db.regexes        
            except pymongo.errors.ConnectionFailure, e:
                logging.error('[!] Database failed to start %s'%(e))
                
    def add(self,regex, user):
        if self.valid(regex):
            return True
        
    def valid(self,regex):        
        try:
            re.compile(regex)
            is_valid = True
        except re.error:
            is_valid = False
        return is_valid