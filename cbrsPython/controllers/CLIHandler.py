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
import logging
import time
import model.Utils.Consts as consts
from xml.dom import minidom

class CLIHandler(Thread):
    '''
    classdocs
    '''
    def __init__(self,csvFilePath):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.confFile =         minidom.parse("conf.xml")
        self.testDefinition =   TestDefinition(CsvFileParser(self.confFile.getElementsByTagName("testRepoPath")[0].firstChild.data+csvFilePath).initializeTestDefinition())
        self.engine =           MyEngine(self.testDefinition) 
        self.questHandler =     QuestionHandler()
        self._stop =            threading.Event()
        self.start()
    
    ''' the method get the step list and sent to the engine the correct json file name to wait for '''
        
    def stop_Thread_Due_To_Exception(self):
        logging.info(consts.CLOSE_USER_SESSION)
        self._stop.set() 
    
    def run(self):   
        while(not self.engine.isNstep and not self._stop.isSet()):
            time.sleep(2)
            if(self.engine.validationErrorAccuredInEngine):
                self.stop_Thread_Due_To_Exception()
        if not self._stop.is_set():
            finalResults = self.questHandler.ShowQuestionsAndGetAnswersFromClient(self.engine.get_Question_Answer_Part())
            print consts.RESULTS_OF_TEST_MESSAGE + str(finalResults[0])
            if(finalResults[1]!=""):
                print consts.ADDITIONAL_COMMENTS_MESSAGE + str(finalResults[1])
            logging.info(consts.RESULTS_OF_TEST_MESSAGE + str(finalResults))
        else:
            print consts.ERROR_VALIDATION_MESSAGE
            


    
       
        