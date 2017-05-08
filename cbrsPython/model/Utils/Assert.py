'''
Created on Apr 20, 2017

@author: iagmon
'''
import sys
import logging

from model.Utils import JsonComparisonUtils
from model.Utils import Consts as consts
from xml.dom import minidom
class Assertion(object):
    '''
    classdocs
    '''


    def __init__(self,confFile,dirPath):
        '''
        Constructor
        '''
        self.confFile = confFile
        self.dirPath  = dirPath
        
    def compare_Json_Req(self,httpRequest,jsonExpected,suffix):
        
        ''' the method will get the request json file name from the client request and will get from the two repo
        off the client and the server the json expected and the real json sent from the client '''
        jsonExpectedObj = JsonComparisonUtils.parse_Json_To_Dic(jsonExpected,suffix,self.confFile,self.dirPath)
        '''in case the suffix is heartbeat the operation state change from time to time '''
        if("heartbeat" in str(suffix)):      
            arr = []
            arr.append("operationState")
            x = JsonComparisonUtils.are_same(httpRequest[suffix],jsonExpectedObj,False,arr)
        else:
            x = JsonComparisonUtils.are_same(httpRequest[suffix],jsonExpectedObj)
        if(False in x):
            print (x)
            logging.info(x)
        assert True in x
                 
    

    
        
        
        
        
        