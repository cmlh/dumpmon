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
        format='%(asctime)s [%(levelname)s][%(module)s][%(funcName)s] %(message)s', filename=log_file, level=level)
    
    handler = RotatingFileHandler(log_file, maxBytes=20*1000,
                                  backupCount=5)
    #logging.addHandler(handler)
    
    logging.info('Monitoring...')
    
    regexMgr = RegexMgr()
    bot = TwitterBot(regexMgr)
                        
    # Create lock for output log
    log_lock = threading.Lock()
    
    #create an event to tell threads to keep running
    isRunning = threading.Event()
    isRunning.set()
    #array to keep a handle on threads    
    workers = []         
    createThread(bot.monitor)
    createThread(Stats().monitor,bot)
    workers.append(createThread(HaveIBeen().monitor,bot,isRunning))
    workers.append(createThread(Pastebin().monitor,bot,isRunning))
    workers.append(createThread(Slexy().monitor,bot,isRunning))
    workers.append(createThread(Pastie().monitor,bot,isRunning))

    # Let threads run
    try:
        while(1):
            sleep(5)
    except KeyboardInterrupt:
        #signal threads to shutdown
        isRunning.clear()
        print 'stopping'
        #wait for threads to join
        for t in workers:
            t.join()
        print 'stopped'    
        logging.warn('Stopped.')


if __name__ == "__main__":
    monitor()
