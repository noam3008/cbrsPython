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
from model import flaskServer
from ENodeBController import ENodeBController

class CLIHandler(Thread):
    '''
    classdocs
    '''
    def __init__(self,csvFilePath,confFile,dirPath,loggerHandler,testDefinition):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.confFile           = confFile
        self.dirPath            = dirPath
        self._stop              = threading.Event()
        self.loggerHandler      = loggerHandler
        self.questHandler       = QuestionHandler(self.loggerHandler)
        self.testDefinition     = testDefinition
        self.numberOfLogger     = self.loggerHandler.currentLoggerName
        self.engine             = MyEngine(self.testDefinition,confFile,dirPath,loggerHandler)
        self.server             = None 
        self.start()
        
    def stop_Thread_Due_To_Exception(self):
        self._stop.set() 
    
    def run(self):   
        while(not self.engine.isLastStepInCSV and not self._stop.isSet()):
            time.sleep(1)
            if(self.engine.validationErrorAccuredInEngine):
                self.stop_Thread_Due_To_Exception()
        if not self._stop.is_set():
            finalResults = self.questHandler.ShowQuestionsAndGetAnswersFromClient(self.engine.get_Question_Answer_Part())
            self.loggerHandler.print_And_Log_To_File(consts.RESULTS_OF_TEST_MESSAGE + str(finalResults[0]),True)
            if(finalResults[1]!=""):
                self.loggerHandler.print_And_Log_To_File(consts.ADDITIONAL_COMMENTS_MESSAGE + str(finalResults[1]),True)
            self.start_another_test(self)
        else:
            self.loggerHandler.print_And_Log_To_File(consts.ERROR_VALIDATION_MESSAGE,True)
            self.loggerHandler.print_And_Log_To_File(consts.RESULTS_OF_TEST_MESSAGE + " is : " + consts.FAIL_MESSAGE)
            self.start_another_test(self)
        
    def start_another_test(self,cliHandler):      
        self.loggerHandler.print_To_Terminal(consts.SET_CSV_FILE_MESSAGE)
        inputAnsweres=raw_input() 
        try:
            testDefenition = TestDefinition(CsvFileParser(str(self.dirPath) + self.confFile.getElementsByTagName("testRepoPath")[0].firstChild.data + inputAnsweres).initializeTestDefinition())
        except IOError as e:
            self.loggerHandler.print_To_Terminal(e.message)
            self.start_another_test(cliHandler)
        if (inputAnsweres !="quit"):
            self.loggerHandler.remove_Test_File_Logger()
            self.loggerHandler.print_To_Terminal(consts.ADD_TEST_TO_SPECIFIC_FOLDER_MESSAGE)
            insertToFolderAnswer = raw_input()
            if (insertToFolderAnswer == "yes"):
                self.loggerHandler.print_To_Terminal("typeNameOfFolder")
                insertToFolderAnswer = raw_input()
                self.loggerHandler.create_New_Logger(inputAnsweres,insertToFolderAnswer)
                self.loggerHandler.print_And_Log_To_File(consts.SELECT_TO_ADD_TEST_MESSAGE + inputAnsweres + consts.SELECT_TO_ADD_FOLDER_MESSAGE + insertToFolderAnswer,True)
            else:
                self.loggerHandler.create_New_Logger(inputAnsweres)
                self.loggerHandler.print_And_Log_To_File(consts.SELECTED_TEST_FROM_USER_MESSAGE + inputAnsweres,True)
            cliHandler = CLIHandler(inputAnsweres,self.confFile,self.dirPath,self.loggerHandler,testDefenition) 
            flaskServer.enodeBController = ENodeBController(cliHandler.engine)
            flaskServer.runFlaskServer(self.confFile.getElementsByTagName("hostIp")[0].firstChild.data) 
               
        if(cliHandler.engine.validationErrorAccuredInEngine):
            cliHandler.stop_Thread_Due_To_Exception()
           
        
        
            