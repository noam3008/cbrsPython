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
        self.numberOfStep                       = 0
        self.numberOfHearbeatRequests           = 0
        self.testDefinietion                    = testDefinition
        self.assertion                          = Assertion()
        self.questionHandler                    = QuestionHandler()
        self.validationErrorAccuredInEngine     = False
        self.isNstep                            = False
        self.firstHeartbeatStep                 = True

        
    def process_request(self,httpRequest,typeOfCalling):
        
        '''
        This will received the request that 
        arrived from the eNodeB,
         will assert the request according to the json file and in case the assert was successful,
          will return the response from the json file        '''
        if (typeOfCalling == consts.HEART_BEAT_SUFFIX_HTTP) and self.numberOfHearbeatRequests<30:
            try:
                self.compare_Json_Req(httpRequest,consts.HEART_BEAT_SUFFIX_HTTP+consts.SUFFIX_OF_JSON_FILE,typeOfCalling)
            except Exception:
                self.validationErrorAccuredInEngine = True  
                return consts.ERROR_VALIDATION_MESSAGE
                 
        try:
            self.compare_Json_Req(httpRequest,self.get_Expected_Json_File_Name(),typeOfCalling)
        except Exception:
            self.validationErrorAccuredInEngine = True  
            return consts.ERROR_VALIDATION_MESSAGE
        return self.process_response(typeOfCalling)

    def compare_Json_Req(self,httpRequest,expectedJsonFileName,typeOfCalling):
        self.assertion.compare_Json_Req(httpRequest,expectedJsonFileName,typeOfCalling+consts.REQUEST_NODE_NAME)
        
        
    def process_response(self,typeOfCalling):
        '''
        This will received the request that 
        arrived from the eNodeB,
         will assert the request according to the json file and in case the assert was successful,
          will return the response from the json file
        '''      
        if(typeOfCalling == "heartbeat"):
            logging.info(consts.HEARTBEAT_FROM_ENGINE_TO_ENODEB_MESSAGE)
            print "get to heartbeat area response"
            if(self.firstHeartbeatStep):
                self.numberOfStep+=1
                self.firstHeartbeatStep = False
            return self.parse_Json_To_Dic_By_File_Name(consts.HEART_BEAT_SUFFIX_HTTP + consts.SUFFIX_OF_JSON_FILE, consts.RESPONSE_NODE_NAME)
        
        jsonAfterParse = self.parse_Json_To_Dic_By_File_Name(self.get_Expected_Json_File_Name(),consts.RESPONSE_NODE_NAME)
        if(self.testDefinietion.defenitionsOfSteps[self.numberOfStep] == consts.LAST_STEP_TYPE):
            logging.info(consts.NSTEP_SESSION_WITH_TECHNITIAN)
            self.questAnswerPartOfJson = self.parse_Json_To_Dic_By_File_Name(self.get_Expected_Json_File_Name(),consts.QUESTION_NODE_NAME)
            self.isNstep = True
        
        
        self.numberOfStep+=1
        return jsonAfterParse
    
    def parse_Json_To_Dic_By_File_Name(self,jsonFileName,nodeName):
        return jsonComparer.parse_Json_To_Dic(jsonFileName,nodeName)
    
    def get_Expected_Json_File_Name(self):
        return self.testDefinietion.jsonNamesOfSteps[self.numberOfStep]
    
    def get_Question_Answer_Part(self):
        return self.questAnswerPartOfJson
    
    
    