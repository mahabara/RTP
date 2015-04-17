# -*- coding: utf-8 -*-
#Created on 2015��3��25��

#@author: etbcffg

#
import constants
import visa
from deviceConfigParser import ConnectionsConfigParser
import time
import MessageQueue
from log4 import log4

def singleton(cls):  
    instances = {}  
    def _singleton(*args, **kw):  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton

class deviceAgentFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def get_DeviceAgent(device_Name):
        if device_Name == constants.DEVICE_NAME_RRU:
            #print device_Name
            return deviceRRUagent(device_Name)

        if device_Name == constants.DEVICE_NAME_SIGNALANALYZER:
            return deviceSAagent(device_Name)

        if device_Name == constants.DEVICE_NAME_SIGNALGENERATOR:
            return deviceSGagent(device_Name)

        if device_Name == constants.DEVICE_NAME_RFBOX:
            return deviceRFBOXagent(device_Name)

        #--------------------- if device_Name == constants.DEVICE_NAME_RuMaster:
            #--------------------------- return deviceRuMasteragent(device_Name)
#------------------------------------------------------------------------------ 
        #-------- if device_Name == constants.DEVICE_NAME_INTERFERENCE_SIGNAL_1:
            #-------------- return deviceINTERFERENCE_SIGNAL_1agent(device_Name)
#------------------------------------------------------------------------------ 
        #-------- if device_Name == constants.DEVICE_NAME_INTERFERENCE_SIGNAL_2:
            #-------------- return deviceINTERFERENCE_SIGNAL_2agent(device_Name)

        else:
            print 'DEVICE NAME ERROR!\n'


class deviceAgentMeta(object):
    def __init__(self,*args,**kw):  
##        print 'args: ',args
##        print 'kw: ',kw
        ccp = ConnectionsConfigParser()
        addressDict = ccp.addressDict
        self.device_name = args[0]
        #print args[0]
        self.device_address = addressDict[args[0]]
        rm = visa.ResourceManager()
        self.device_agent = rm.open_resource(self.device_address)
        #print self.device_address
        # timeout = 1s
        self.device_agent.timeout = constants.OPERATION_TIMEOUT
        #comcp = commandConfigParser(constants.RRU_COMMAND_CONFIG_PATH,constants.RRU_COMMANDS_SECTIONLABLE)
        #self.RRU_commands_dict = comcp.content
        


    def commandline(self):
        while True:
            command = raw_input("Please input comannds:(press 'exit' to quit.)\n")
            if(command == "exit"):
                break
               
            try:
                self.device_agent.write(command)
                feedback = 'Reply from server: ' + self.device_agent().read() + '\n'
                print feedback
            except:
                print "Connect server failed"
                continue
               
    def cmdFormat(self,command):      #format command
        cmdlist = command.split('\n')
        i = 0
        #print len(cmdlist)
        cmdnewlist = []
        while True:
            if i < len(cmdlist):
                        #print i
                if (cmdlist[i]!=''):
                    cmdnewlist.append(cmdlist[i])
                i += 1
                
            else:
                break
        return cmdnewlist
    
    def cmd(self,command,delay=0):
        pass
    
@singleton
class deviceRRUagent(object):
    
    
    def __init__(self,device_name,display_thread,serialins):
        ccp = ConnectionsConfigParser()
        addressDict = ccp.addressDict
        self.device_name = device_name
        self.display_thread = display_thread
        self.serial = serialins
        self.logger = log4()
    
    
    
    def cmd_single(self,command,delay=0):
        
        retval = []
        if delay != 0:
            mesgtimer = MessageQueue.messageTimer(command,self.serial,self.display_thread,retval,delay)
            mesgtimer.start()
            mesgtimer.join()
            return retval
        else:
            self.serial.write(command)
            
            
            
        return 

    def cmd(self,command,delay=0):
        
        
        if 'ts.' in command:
            
            sendcmd = self.RRU_commands_dict.get(command.replace('ts.',''))
            
            sendcmdlist = self.cmdFormat(sendcmd)
            
            for cmd in sendcmdlist:
                self.cmd_single(cmd)
            return 
        else:
            
            return self.cmd_single(cmd,delay)
             

        return 0
    
    

        
        
    def cmdFormat(self,command):      #format command
        cmdlist = command
        i = 0
        #print len(cmdlist)
        cmdnewlist = []
        while True:
            if i < len(cmdlist):
                        #print i
                if (cmdlist[i]!=''):
                    cmdnewlist.append(cmdlist[i])
                i += 1
                
            else:
                break
        return cmdnewlist

    
    
    def testcmd(self,command,delay=0):
        cmdstr = command.split('.')[1]
        sendcmd = self.RRU_commands_dict.get(cmdstr)
        sendcmdlist = self.cmdFormat(sendcmd)
        for i in sendcmdlist:
            print i + ', '

@singleton
class deviceRFBOXagent(object):
    

    def __init__(self,device_name):
        ccp = ConnectionsConfigParser()
        addressDict = ccp.addressDict
        self.device_name = device_name
        self.logger = log4()
        print device_name
        self.device_address = addressDict[device_name]
        
        rm = visa.ResourceManager()
        self.device_agent = rm.open_resource(self.device_address)
        print self.device_address
        # timeout = 1s
        self.device_agent.timeout = constants.OPERATION_TIMEOUT

    
    
    #send cmd like 'RF-Box.BO2 2'
    def cmd(self,command,delay=0):
        #sc = socketclient()
        print 'RFBOX swicth start: ' + command
        readIndex = 0
        self.device_agent.write(command)
        while readIndex<1:    
            try:
                ret = self.device_agent.read()
                self.logger.logging(ret)
                #print ret
            except :
                self.logger.logging('read RFBOX error')
                #print 'read RFBOX error'
                break
            
            readIndex+=1
        if delay!=0:
            time.sleep(float(delay)/float(1000))
            
        if ret.strip()!='':    
            #sc.send(ret)
            return ret
        else:
            return 0        
         
        
        

    
@singleton
class deviceSGagent(object):
    

    def __init__(self,device_name):
        ccp = ConnectionsConfigParser()
        addressDict = ccp.addressDict
        self.logger = log4()
        self.device_name = device_name
        print device_name
        self.device_address = addressDict[device_name]
        rm = visa.ResourceManager()
        self.device_agent = rm.open_resource(self.device_address)
        print self.device_address
        # timeout = 1s
        self.device_agent.timeout = constants.OPERATION_TIMEOUT

    
    
    #send cmd like 'SG.Command:SOURce1:BB:EUTR:STAT ON'
    def cmd(self,command,delay=0):
        #sc = socketclient()
        #print command
        self.device_agent.delay = 0.0
        readIndex = 0
        self.device_agent.write(command)
        while readIndex<1:    
            try:
                ret = self.device_agent.read()
                self.logger.logging(ret)
                #print ret
            except :
                self.logger.logging('read SG error')
                #print 'read SG error'
                break
            
            readIndex+=1
            
        if delay!=0:
            time.sleep(float(delay)/float(1000))
            
        if ret!='':
            #sc.send(ret)
            return ret
        else:
            return 0

    
@singleton
class deviceSAagent(object):
    

    def __init__(self,device_name):
        ccp = ConnectionsConfigParser()
        addressDict = ccp.addressDict
        self.logger = log4()
        self.device_name = device_name
        print device_name
        self.device_address = addressDict[device_name]
        rm = visa.ResourceManager()
        self.device_agent = rm.open_resource(self.device_address)
        print self.device_address
        # timeout = 1s
        self.device_agent.timeout = constants.OPERATION_TIMEOUT

    
    
    #send cmd like 'SA.Command::SYST:PRESET'
    def cmd(self,command,delay=0):
        #sc = socketclient()
        self.device_agent.delay = 0.0
        readIndex = 0
        
        
        self.device_agent.write(command)
        if '?' in command:
            
            while readIndex<1:    
                try:
                    ret = self.device_agent.read()
                    self.logger.logging(ret)
                    #------------------------------------------------- print ret
                    
                    break
                except :
                    self.logger.logging('read SA error')
                    #------------------------------------- print 'read SA error'
                    time.sleep(2)
                    continue

                readIndex+=1
            #print 'deviceSAagent- ' + command+ ' -readvalue:' +str(readvalue)
            
            if len(ret) != 0:
                #sc.send(readvalue[0])
                return ret
            else:
                return 0
        else:
            return 0
    
    