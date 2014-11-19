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
from lib.helper import log
from lib.TwitterBot import TwitterBot
from time import sleep
from settings import log_file
import threading
import logging


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
        format='%(asctime)s [%(levelname)s] %(funcName)s %(module)s %(message)s', filename=log_file, level=level)
    logging.info('Monitoring...')
    
    bot = TwitterBot()
                            
    # Create lock for output log
    log_lock = threading.Lock()
    
    def createThread(target,*args,**kwargs):        
         t = threading.Thread(target=target, args=args, kwargs=kwargs)         
         t.daemon = True
         t.start()
         
    createThread(bot.monitor)
    createThread(bot.test)
    #createThread(Pastebin().monitor,bot)
    #createThread(Slexy().monitor,bot)
    #createThread(Pastie().monitor,bot)

    # Let threads run
    try:
        while(1):
            sleep(5)
    except KeyboardInterrupt:
        logging.warn('Stopped.')


if __name__ == "__main__":
    monitor()
