'''
Created on Apr 20, 2017

@author: iagmon
'''
import sys
import logging

from model.Utils import JsonComparisonUtils
from model.Utils import Consts as consts
from xml.dom import minidom
import json
class Assertion(object):
    '''
    classdocs
    '''


    def __init__(self,confFile,dirPath,loggerHandler):
        '''
        Constructor
        '''
        self.confFile = confFile
        self.dirPath  = dirPath
        self.loggerHandler = loggerHandler
        
    def compare_Json_Req(self,httpRequest,jsonExpected,suffix):
        
        ''' the method will get the request json file name from the client request and will get from the two repo
        off the client and the server the json expected and the real json sent from the client '''
        
        jsonExpectedObj = JsonComparisonUtils.get_Node_Of_Json_Parsed(jsonExpected,suffix,self.confFile,self.dirPath)
        x = JsonComparisonUtils.are_same(httpRequest[suffix],jsonExpectedObj)
        if(False in x):
            self.loggerHandler.print_And_Log_To_File(x,True)
        assert True in x
        

    def is_Json_Contains_Key(self, jsonExpected,keyToVerify):
        return JsonComparisonUtils.Is_Json_contains_key(jsonExpected, keyToVerify, self.confFile, self.dirPath)
    
    def get_Attribute_Value_From_Json(self,jsonExpected,keyToVerify):
        if(self.is_Json_Contains_Key(jsonExpected, keyToVerify)):
            return JsonComparisonUtils.get_Node_Of_Json_Parsed(jsonExpected,keyToVerify,self.confFile,self.dirPath)
        return None
    
    def get_Duration_Time_From_Grant_Json(self,jsonExpected):
        responsePart = JsonComparisonUtils.get_Node_Of_Json_Parsed(jsonExpected,consts.RESPONSE_NODE_NAME,self.confFile,self.dirPath)
        return responsePart[consts.GRANT_SUFFIX_HTTP+consts.RESPONSE_NODE_NAME.title()][0]['heartbeatDuration']
    

    
        
        
        
        
        