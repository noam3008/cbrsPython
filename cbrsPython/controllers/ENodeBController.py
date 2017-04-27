'''
Created on Apr 24, 2017

@author: iagmon
'''
import logging

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
        
        
    def linkerBetweenFlaskToEngine(self,jsonReq):######### while flask change it to the request of flask
        logging.info("the enode B controller sent the request he gets from the client to the engine")
        return self.engine.process_request(jsonReq)
    

    
        
        