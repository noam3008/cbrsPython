'''
Created on Apr 24, 2017

@author: iagmon
'''
import logging
import model.Utils.Consts as consts
from threading import Thread



class ENodeBController(Thread):
    '''
    classdocs
    '''

    def __init__(self,engine):
        '''
        Constructor
        '''     
        self.engine = engine
        
        
    def linker_Between_Flask_To_Engine(self,jsonReq,typeOfCalling):
        return self.engine.process_request(jsonReq,typeOfCalling)
    

    
        
        