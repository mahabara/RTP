# -*- coding: utf-8 -*-
#Created on 2015��4��9��

#@author: etbcffg

#
# -*- coding: cp936 -*-



import time
import constants 
from deviceAgentFactory import deviceAgentFactory

      

    
def retvalstrip(retvalue):
    newretvalue = []
    for ret in retvalue:
        if ret !='':
            newretvalue.appent(ret)
    return newretvalue
     
class client:

    def address(self,IP,port):
        pass
       
    def commandline(self):
        pass

    def cmd(self,command,delay=0):
        
        print command
        #�������ͷ�ж���������һ�ȡ��Ӧ��agent:��'SA.Command::SYST:PRESET'
        agent = 0
        if 'SA.Command' in command:   #process SA commands:'SA.Command::SYST:PRESET'
            cmdstr = command.replace('SA.Command:','')
            agent = deviceAgentFactory.get_DeviceAgent(constants.DEVICE_NAME_SIGNALANALYZER)

        if 'SG.Command' in command:   #process SG commands:'SG.Command:SOURce1:BB:EUTR:STAT ON'
            cmdstr = command.replace('SG.Command:','')
            agent = deviceAgentFactory.get_DeviceAgent(constants.DEVICE_NAME_SIGNALGENERATOR)

        if 'ts.' in command or 'RRU.' in command:   #process ts commands:"ts.DL_Release"
            cmdstr = command
            agent = deviceAgentFactory.get_DeviceAgent(constants.DEVICE_NAME_RRU)

        if 'pwr' in command:   #process ts commands:"pwr UL_OAB 0 0 4"
            cmdstr = command.replace('ts.','')
            agent = deviceAgentFactory.get_DeviceAgent(constants.DEVICE_NAME_RRU)


        if 'RF-Box.' in command:   ##process RF-BOX commands
            cmdstr = command.replace('RF-Box.','')
            agent = deviceAgentFactory.get_DeviceAgent(constants.DEVICE_NAME_RFBOX)

        if 'Process.Delay' in command:   #process 'Process.Delay(72000)'
            delay = command.strip('Process.Delay()')
            retvalue = 'delay ' + str(delay) + ' ms'
            
            time.sleep(float(delay)/float(1000))
        return retvalue

        #print cmdstr
        retvalue = agent.cmd(cmdstr,delay)
        
        
        
        return retvalue

    

    def pcmd(self,command,delay=0):
        pass

     
