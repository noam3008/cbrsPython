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
        Thread.__init__(self)      
        self.engine = engine
        
        
    def linker_Between_Flask_To_Engine(self,jsonReq,typeOfCalling):
        logging.info(consts.E_NODE_B_SENT_TO_ENGINE_REQUEST)
        return self.engine.process_request(jsonReq,typeOfCalling)
    

    
        
        