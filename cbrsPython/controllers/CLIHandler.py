'''
Created on Apr 24, 2017

@author: iagmon
'''
import threading
from threading import Thread
from CLIUtils.CsvFileParser import CsvFileParser
from CLIUtils.QuestionHandler import QuestionHandler
from CLIUtils.TestDefinition import TestDefinition
from model.Engine import MyEngine
from model import flaskServer
from ENodeBController import ENodeBController
import time
import model.Utils.Consts as consts
import sys

class CLIHandler(Thread):
    '''
    classdocs
    '''
    def __init__(self,csvFilePath):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.testDefinition =   TestDefinition(CsvFileParser(csvFilePath).initializeTestDefinition())
        self.engine =           MyEngine(self.testDefinition) 
        self.questHandler =     QuestionHandler()
        self._stop =            threading.Event()
        '''self.start()'''
    
    ''' the method get the step list and sent to the engine the correct json file name to wait for '''
        
    def stopThreadBecauseOfException(self):
        logging.info(consts.CLOSE_USER_SESSION)
        self._stop.set() 
    
    '''def run(self):   
        while(not self.engine.isNstep and not self._stop.isSet()):
            time.sleep(1)
            if(self.engine.validationErrorAccuredInEngine):
                self.stopThreadBecauseOfException()
        if not self._stop.is_set():
            finalResults = self.questHandler.ShowQuestionsAndGetAnswersFromClient(self.engine.getQuestionAnswerPart())
            print consts.RESULTS_OF_TEST_MESSAGE + str(finalResults)
            logging.info(consts.RESULTS_OF_TEST_MESSAGE + str(finalResults))
        else:
            print consts.ERROR_VALIDATION_MESSAGE
            logging.info(consts.ERROR_VALIDATION_MESSAGE)'''
            
print (consts.SET_CSV_FILE_MESSAGE)  

import logging
with open('example.log', 'w'):
    pass

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.info(consts.START_TEST_MESSAGE)

inputAnswer=raw_input()     
cliHandler = CLIHandler(inputAnswer)#"C:\Users\iagmon\Desktop\exampleTest.csv"))
flaskServer.enodeBController = ENodeBController(cliHandler.engine)
flaskServer.runFlaskServer()
if(cliHandler.engine.validationErrorAccuredInEngine):
    cliHandler.stopThreadBecauseOfException()

    
       
        