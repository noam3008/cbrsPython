'''
Created on Apr 20, 2017

@author: iagmon
'''
import json
import logging

from model.Utils import JsonComparisonUtils


class Assertion(object):
    '''
    classdocs
    '''


    def __init__(self):
        noam = 1
        '''
        Constructor
        '''
        
    def compareJsonReq(self,httpRequest,jsonExpected):
        logging.info("compare two jsons")
        ''' the method will get the request json file name from the client request and will get from the two repo
        off the client and the server the json expected and the real json sent from the client '''
        jsonExpectedObj = JsonComparisonUtils.parseJsonToDic("C:/Users/iagmon/Desktop/jsonFolder/",jsonExpected,"request")       
        x = JsonComparisonUtils.are_same(httpRequest["request"],jsonExpectedObj)
        assert True in x
        
        
        ################## the compare of the actual and expected request
                
    def compare_json(self,x,y):
        for i in range(len(x)):
            self.assertEqual(x[i],y[i])
            
    def assertEqual(self,actual,expected):
        assert actual==expected
                 
    

    
        
        
        
        
        