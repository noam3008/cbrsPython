'''
Created on Apr 20, 2017

@author: iagmon
'''
import sys
import logging

from model.Utils import JsonComparisonUtils
from model.Utils import Consts as consts
import logging

class Assertion(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def compare_Json_Req(self,httpRequest,jsonExpected,suffix):
        
        ''' the method will get the request json file name from the client request and will get from the two repo
        off the client and the server the json expected and the real json sent from the client '''
        jsonExpectedObj = JsonComparisonUtils.parse_Json_To_Dic("C:/Users/iagmon/Desktop/jsonFolder/",jsonExpected,suffix)
        logging.info(consts.COMPARING_JSONS_MESSAGE)              
        x = JsonComparisonUtils.are_same(httpRequest[suffix],jsonExpectedObj)
        if(False in x):
            print x
        assert True in x
                 
    

    
        
        
        
        
        