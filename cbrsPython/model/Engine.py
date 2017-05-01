'''
Created on Apr 20, 2017

@author: iagmon
'''

from model.Utils.Assert import Assertion 
import model.Utils.JsonComparisonUtils as jsonComparer
from controllers.CLIUtils.QuestionHandler import QuestionHandler
import logging
import model.Utils.Consts as consts

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
        self.validationErrorAccuredInEngine = False
        self.isNstep = False
        
    def process_request(self,httpRequest,typeOfCalling):
        '''
        This will received the request that 
        arrived from the eNodeB,
         will assert the request according to the json file and in case the assert was successful,
          will return the response from the json file        '''
        paramsForResponse =[]
        if typeOfCalling == consts.HEART_BEAT_SUFFIX_HTTP:
            logging.info(consts.HEART_BEAT_ARRIVED_MESSAGE)
            self.compareJsonReq(httpRequest, consts.HEART_BEAT_SUFFIX_HTTP+ consts.SUFFIX_OF_JSON_FILE)
            return self.process_response(True)
                 
        try:
            self.compareJsonReq(httpRequest,self.getExpectedJsonFileName(),typeOfCalling)
        except Exception:
            print "catch exception in comparing jsons"
            self.validationErrorAccuredInEngine = True
            paramsForResponse.append(consts.ERROR_VALIDATION_MESSAGE)
            #paramsForResponse.append(self.validationErrorAccuredInEngine)
            return paramsForResponse
        return self.process_response()

    def compareJsonReq(self,httpRequest,expectedJsonFileName,typeOfCalling):
        print "type of calling " + typeOfCalling
        if(typeOfCalling=="registration"):
            print "http req" + str(httpRequest)
            self.assertion.compareJsonReq(httpRequest,expectedJsonFileName,"registrationRequest")
        if(typeOfCalling=="spectrumInquiry"):
            self.assertion.compareJsonReq(httpRequest,expectedJsonFileName,"spectrumInquiryRequest")
        
        
    def process_response(self,heartBeatRequest=False):
        '''
        This will received the request that 
        arrived from the eNodeB,
         will assert the request according to the json file and in case the assert was successful,
          will return the response from the json file
        '''      
        if((heartBeatRequest)and(self.testDefinietion.jsonNamesOfSteps[self.numberOfStep-1]==consts.GRANT_SUFFIX_HTTP+ consts.SUFFIX_OF_JSON_FILE)):
            logging.info(consts.HEARTBEAT_FROM_ENGINE_TO_ENODEB_MESSAGE)
            return self.parseJsonToDicByFileName(consts.HEART_BEAT_SUFFIX_HTTP + consts.SUFFIX_OF_JSON_FILE, consts.RESPONSE_NODE_NAME)
        
        jsonAfterParse = self.parseJsonToDicByFileName(self.getExpectedJsonFileName(),consts.RESPONSE_NODE_NAME)
        print "after parse to response node " + str(jsonAfterParse)
        print "expected file name  " + str(self.getExpectedJsonFileName())
        if(self.testDefinietion.defenitionsOfSteps[self.numberOfStep] == "nstep"):
            logging.info(consts.NSTEP_SESSION_WITH_TECHNITIAN)
            self.questAnswerPartOfJson = self.parseJsonToDicByFileName(self.getExpectedJsonFileName(),consts.QUESTION_NODE_NAME)
            self.isNstep = True
        
        self.numberOfStep+=1
        return jsonAfterParse
    
    def parseJsonToDicByFileName(self,jsonFileName,nodeName,jsonRepoPath="C:/Users/iagmon/Desktop/jsonFolder/"):
        return jsonComparer.parseJsonToDic(jsonRepoPath, jsonFileName,nodeName)
    
    def getExpectedJsonFileName(self):
        return self.testDefinietion.jsonNamesOfSteps[self.numberOfStep]
    
    def getQuestionAnswerPart(self):
        return self.questAnswerPartOfJson
    
    
    