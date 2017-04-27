'''
Created on Apr 24, 2017

@author: iagmon
'''
from threading import Thread
from CLIUtils.CsvFileParser import CsvFileParser
from CLIUtils.QuestionHandler import QuestionHandler
from CLIUtils.TestDefinition import TestDefinition
from model.Engine import MyEngine
from model import flaskServer
from ENodeBController import ENodeBController
import time

class Mcontroller(Thread):
    '''
    classdocs
    '''
    def __init__(self,csvFilePath):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.testDefinition = TestDefinition(CsvFileParser(csvFilePath).initializeTestDefinition())
        self.engine = MyEngine(self.testDefinition) 
        self.questHandler = QuestionHandler()
        self.start()
    
    ''' the method get the step list and sent to the engine the correct json file name to wait for '''
        
    def getResponseFromEngine(self, jsonAfterParse,questAnswerPartOfJson):
        self.questHandler.ShowQuestionsAndGetAnswersFromClient(questAnswerPartOfJson)
    
    def run(self):
        while(not self.engine.flag):
            time.sleep(1)
        print "The final result of the test is : " + str(self.questHandler.ShowQuestionsAndGetAnswersFromClient(self.engine.getQuestionAnswerPart()))
        
    
      
print ("Please enter a csv file path that include the test you request to run")   
inputAnswer = raw_input()     
mController = Mcontroller(inputAnswer)#"C:\Users\iagmon\Desktop\exampleTest.csv")
flaskServer.enodeBController = ENodeBController(mController.engine)
flaskServer.runFlaskServer()
        
        