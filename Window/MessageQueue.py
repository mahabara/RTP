
import threading,serial,time
import Queue
from log4 import log4

def singleton(cls):  
    instances = {}  
    def _singleton(*args, **kw):  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton

@singleton
class messageTimer(threading.Thread):
    def __init__(self,cmd,serialins,display_thread,retval,delay):
        self.delay = float(delay)/float(1000)    #float,ms
        self.queue = display_thread.queue
        self.disthread = display_thread
        self.retval = retval
        self.cmd = cmd
        self.serial = serialins
        
    def run(self):
        self.disthread.put_to_queue = True
        self.serial.write(self.cmd)
        time.sleep(self.delay)
        self.disthread.put_to_queue = False
        while self.queue.empty()!=True:
            
            self.retval.append(self.queue.get())
            self.queue.task_done()

class RRU_trace_display_thread(threading.Thread):
    def __init__(self,serialins): 
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        self.stopFlag = False
        self.put_to_queue = False
        self.ser = serialins
        self.queue =  Queue.Queue(-1)
        self.daemon = False 
        self.logger = log4()
        
        
        
    def run(self):
        self.logger.logging('RRU_trace_read_thread start!')
        #print 'RRU_trace_read_thread start'
        while 1:
            if self.stopFlag == False:
                
                try:
                    item = self.ser.readline()
                    #print item
                except serial.SerialException:
                    self.logger.logging('Serialtest.SerialException ERROR!')
                    
                    continue
            
                if len(item.strip('\n\r').strip())!=0:
                    self.logger.logging(item.strip('\n\r'))
                    #---------------------------------- print item.strip('\n\r')
                    
                if self.put_to_queue == True:
                    
                    self.queue.Put(item)
                    self.queue.task_done()
            else:
                self.logger.logging('RRU_trace_read_thread stop!')
                
                break
            
        
        

class RRU_trace_read_thread(threading.Thread):
    def __init__(self,queue,serialtest): 
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        
        self.ser = serialtest
         
        self.daemon = False 
        self.queue = queue
        
        
        
    def run(self):
        print 'RRU_trace_read_thread start'
        while 1:
            try:
                item = self.ser.readline()
            except serial.SerialException:
                print 'serialtest.SerialException ERROR'
                #print traceback.format_exc()
                continue
            
            if len(item.strip('\n\r').strip())!=0:
                self.queue.put(item.strip('\n\r'))
                self.queue.task_done()
            
        self.queue.task_done()
        return

class RRU_trace_print_thread(threading.Thread): 
    def __init__(self): 
        threading.Thread.__init__(self) 
        self.daemon = False 
        self.stopFlag = False
        
         
    def run(self):
        print 'RRU_trace_print_thread start' 
        while 1: 
            if self.stopFlag == False:
                pass
            else:
                print 'thread stoped'
                break
         
 

