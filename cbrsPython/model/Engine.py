'''
Created on Apr 20, 2017

@author: iagmon
'''

from model.Utils.Assert import Assertion 
import model.Utils.JsonComparisonUtils as jsonComparer
from controllers.CLIUtils.QuestionHandler import QuestionHandler

class MyEngine(object):

    def __init__(self,testDefinition):
        '''
        Will recieve the test structure (the list of the json file and the step defintions). 
        Will read all the json files and save it as some structure.
        '''
        self.numberOfStep = 0
        self.testDefinietion = testDefinition
        self.assertion= Assertion()
        self.questionHandler = QuestionHandler()
        self.flag = False
        
    def process_request(self,httpRequest):
        '''
        This will received the request that 
        arrived from the eNodeB,
         will assert the request according to the json file and in case the assert was successful,
          will return the response from the json file        '''
        self.assertion.compareJsonReq(httpRequest,self.getExpectedJsonFileName())
        return self.process_response()

    def process_response(self):
        '''
        This will received the request that 
        arrived from the eNodeB,
         will assert the request according to the json file and in case the assert was successful,
          will return the response from the json file
        '''
        "start process response function"
        '''
        if(self.testDefinietion.defenitionsOfSteps[self.numberOfStep] == "nstep"):
            questionAnswerPart = jsonComparer.parseJsonToDic("C:/Users/iagmon/Desktop/jsonFolder/", self.getExpectedJsonFileName(),"questions")
            answers = self.questionHandler.ShowQuestionsAndGetAnswersFromClient(questionAnswerPart)
            print answers'''
                      
        jsonAfterParse = jsonComparer.parseJsonToDic("C:/Users/iagmon/Desktop/jsonFolder/", self.getExpectedJsonFileName(),"response")
        if(self.testDefinietion.defenitionsOfSteps[self.numberOfStep] == "nstep"):
            self.questAnswerPartOfJson = jsonComparer.parseJsonToDic("C:/Users/iagmon/Desktop/jsonFolder/", self.getExpectedJsonFileName(),"questions")
            self.flag = True
        
        self.numberOfStep+=1
        return jsonAfterParse
    
    def getExpectedJsonFileName(self):
        return self.testDefinietion.jsonNamesOfSteps[self.numberOfStep]
    
    def getQuestionAnswerPart(self):
        return self.questAnswerPartOfJson
    
    
    