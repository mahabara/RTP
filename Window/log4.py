# -*- coding: utf-8 -*-
#Created on 2015��4��9��

#@author: etbcffg

#

import logging,datetime  
from  logging.handlers import  BaseRotatingHandler
import os

def singleton(cls):  
    instances = {}  
    def _singleton(*args, **kw):  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton

class timeRotatingFileHandler(BaseRotatingHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size.
    """
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0):
        """
        Open the specified file and use it as the stream for logging.

        By default, the file grows indefinitely. You can specify particular
        values of maxBytes and backupCount to allow the file to rollover at
        a predetermined size.

        Rollover occurs whenever the current log file is nearly maxBytes in
        length. If backupCount is >= 1, the system will successively create
        new files with the same pathname as the base file, but with extensions
        ".1", ".2" etc. appended to it. For example, with a backupCount of 5
        and a base file name of "app.log", you would get "app.log",
        "app.log.1", "app.log.2", ... through to "app.log.5". The file being
        written to is always "app.log" - when it gets filled up, it is closed
        and renamed to "app.log.1", and if files "app.log.1", "app.log.2" etc.
        exist, then they are renamed to "app.log.2", "app.log.3" etc.
        respectively.

        If maxBytes is zero, rollover never occurs.
        """
        # If rotation/rollover is wanted, it doesn't make sense to use another
        # mode. If for example 'w' were specified, then if there were multiple
        # runs of the calling application, the logs from previous runs would be
        # lost if the 'w' is respected, because the log file would be truncated
        # on each run.
        if maxBytes > 0:
            mode = 'a'
        BaseRotatingHandler.__init__(self, filename, mode, encoding, delay)
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        self.baseFilename = self.baseFilename.split('+')[0]+'+'+datetime.datetime.now().strftime('%Y-%m-%d__%H-%M-%S-%f')+'.txt'

    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None
            
        self.baseFilename = self.baseFilename.split('+')[0]+'+'+datetime.datetime.now().strftime('%Y-%m-%d__%H-%M-%S-%f')+'.txt'
        #--------------------------------- dfn = self.baseFilename + '.' +dstnow
#------------------------------------------------------------------------------ 
        #----------------------------------------------- if os.path.exists(dfn):
            #---------------------------------------------------- os.remove(dfn)
            #- # Issue 18940: A file may not have been created if delay is True.
        #--------------------------------- if os.path.exists(self.baseFilename):
                #----------------------------- os.rename(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        if self.stream is None:                 # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:                   # are we rolling over?
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  #due to non-posix-compliant Windows feature
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        return 0

@singleton    
class log4(object):
    
    def __init__(self):
    
        if not os.path.exists('log'):
            os.mkdir('log')  
        self.LOG_FILE = r'.\log\RTP-log'+'+'+datetime.datetime.now().strftime('%Y-%m-%d__%H-%M-%S-%f')+'.txt'  
  
        self.handler = timeRotatingFileHandler(self.LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # handler
 
        self.fmt = '%(asctime)s - %(message)s'  
  
        self.formatter = logging.Formatter(self.fmt)   # formatter  
        self.handler.setFormatter(self.formatter)      # Ϊhandler
  
        self.logger = logging.getLogger('tst')    # Ϊtstlogger  
        self.logger.addHandler(self.handler)           # Ϊloggerhandler  
        self.logger.setLevel(logging.DEBUG)
        
    def logging(self,message):
        self.logger.info(message)
        print message
          
