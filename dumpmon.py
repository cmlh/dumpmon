# dumpmon.py
# Author: Jordan Wright
# Version: 0.0 (in dev)

# ---------------------------------------------------
# To Do:
#
#	- Refine Regex
#	- Create/Keep track of statistics

from lib.regexes import regexes
from lib.Pastebin import Pastebin, PastebinPaste
from lib.Slexy import Slexy, SlexyPaste
from lib.Pastie import Pastie, PastiePaste
from lib.HaveIBeen import HaveIBeen, HaveIBeenPaste

from lib.helper import log, createThread
from lib.TwitterBot import TwitterBot
from lib.RegexMgr import RegexMgr
from lib.Stats import Stats
from time import sleep
from settings import log_file
import threading
import logging
from logging.handlers import RotatingFileHandler


def monitor():
    '''
    monitor() - Main function... creates and starts threads

    '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", help="more verbose", action="store_true")
    args = parser.parse_args()
    
    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
    
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s]    [%(module)s]    [%(funcName)s]    %(message)s', filename=log_file, level=level)
    
    handler = RotatingFileHandler(log_file, maxBytes=20*1000,
                                  backupCount=5)
    #logging.addHandler(handler)
    
    logging.info('Monitoring...')
    
    regexMgr = RegexMgr()
    bot = TwitterBot(regexMgr)
                        
    # Create lock for output log
    log_lock = threading.Lock()
         
    createThread(bot.monitor)
    createThread(Stats().monitor,bot)

    createThread(HaveIBeen().monitor,bot)
    createThread(Pastebin().monitor,bot)
    createThread(Slexy().monitor,bot)
    createThread(Pastie().monitor,bot)

    # Let threads run
    try:
        while(1):
            sleep(5)
    except KeyboardInterrupt:
        logging.warn('Stopped.')


if __name__ == "__main__":
    monitor()
