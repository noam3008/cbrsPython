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
import time
import model.Utils.Consts as consts
from model import flaskServer
from ENodeBController import ENodeBController
import ssl

class CLIHandler(Thread):
    '''
    classdocs
    '''
    def __init__(self,csvFilePath,confFile,dirPath,loggerHandler,testDefinition):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.testName           = csvFilePath
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
        ''' 
        the thread checks all the time if its the last step from the csv file or an error validation had accured
        while validate inside the engine
        if the test had been finished successfully it show the question answer session from the last expected json
        '''  
        while(not self.engine.check_Last_Step_In_All_CBRS() and not self._stop.isSet()):
            time.sleep(1)
            if(self.engine.check_Validation_Error()):
                self.stop_Thread_Due_To_Exception()
        if not self._stop.is_set():
            finalResults = self.questHandler.ShowQuestionsAndGetAnswersFromClient(self.engine.get_Question_Answer_Part())
            self.loggerHandler.print_And_Log_To_File(consts.RESULTS_OF_TEST_MESSAGE + self.testName + " is : " +  str(finalResults[0]),True)
            if(finalResults[1]!=""):
                self.loggerHandler.print_And_Log_To_File(consts.ADDITIONAL_COMMENTS_MESSAGE + str(finalResults[1]),True)
            self.start_another_test(self)
        else:
            self.loggerHandler.print_And_Log_To_File(consts.RESULTS_OF_TEST_MESSAGE +self.testName +  " is : " + consts.FAIL_MESSAGE,True)
            self.start_another_test(self)
        
    def start_another_test(self,cliHandler): 
        '''
        as same as in the startOfProject.py 
        initialize new logger for each test and if requested to the specific folder
        stop the last reports of the test running before the new test
        and running a new instance of the flask server  
        '''     
        self.loggerHandler.print_To_Terminal(consts.SET_CSV_FILE_MESSAGE)
        inputAnsweres=raw_input() 
        try:
            csvFileParser = CsvFileParser(str(self.dirPath) + self.confFile.getElementsByTagName("testRepoPath")[0].firstChild.data + inputAnsweres)
            self.testDefinition = TestDefinition(csvFileParser.initializeTestDefinition(),csvFileParser.find_Number_Of_Cols())
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
            cliHandler = CLIHandler(inputAnsweres,self.confFile,self.dirPath,self.loggerHandler,self.testDefinition) 
            flaskServer.enodeBController = ENodeBController(cliHandler.engine)
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2) # use TLS to avoid POODLE
            ctx.verify_mode = ssl.CERT_REQUIRED
            ctx.load_verify_locations(str(self.dir_path) + cliHandler.get_Element_From_Config_File("caCerts"))
            ctx.load_cert_chain(str(self.dirPath) + cliHandler.get_Element_From_Config_File("pemFilePath"), str(self.dirPath) + cliHandler.get_Element_From_Config_File("keyFilePath"))
            flaskServer.runFlaskServer(self.get_Element_From_Config_File("hostIp"),self.get_Element_From_Config_File("port"),ctx) 
            
        if(cliHandler.engine.validationErrorAccuredInEngine):
            cliHandler.stop_Thread_Due_To_Exception()

    def get_Element_From_Config_File(self,elementName):
        return self.confFile.getElementsByTagName(elementName)[0].firstChild.data
        
        
            