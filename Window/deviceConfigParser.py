# -*- coding: utf-8 -*-
#Created on 2015��3��24��

#@author: etbcffg

#
import sys,os
import ConfigParser
import constants

#File_path = 'ConnectionConfig.ini'           #file path


class ConnectionsConfigParser(object):
    def __init__(self, config_file_path = constants.CONNECTION_CONFIG):
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)

        s = cf.sections()
        self.sections = s                        #add all sections to a list

        self.addressDict = {}
        for k in self.sections:
            self.addressDict[k] = cf.items(k)[0][1]  #add section and address pairs to dict[('SIGNALANALYZER', 'TCPIP0::10.166.128.22::inst0::INSTR'), ('RuMaster', '')]

    #with section to find address
    def get_Address(self,section):
        print self.addressDict[section]
        return self.addressDict[section]
    
    def set_Address(self,addressDict,config_file_path = constants.CONNECTION_CONFIG):
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        for (x,y) in addressDict.items():
            
            cf.set(x, constants.CONNECTION_CONFIG_OPTION, y)
        cf.write(open(config_file_path,'w'))

if __name__ == "__main__":
    pass