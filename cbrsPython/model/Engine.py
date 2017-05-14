'''
Created on Apr 20, 2017

@author: iagmon
'''

from model.Utils.Assert import Assertion 
import model.Utils.JsonComparisonUtils as jsonComparer
import model.Utils.Consts as consts
import datetime as DT


class MyEngine(object):

    def __init__(self,testDefinition,confFile,dirPath,currentLogger):
        self.numberOfStep                       = 0
        self.numberOfHearbeatRequests           = 0
        self.testDefinietion                    = testDefinition
        self.validationErrorAccuredInEngine     = False
        self.isLastStepInCSV                    = False
        self.confFile                           = confFile
        self.dirPath                            = dirPath
        self.heartBeatLimitCounter              = confFile.getElementsByTagName("heartbeatLimit")[0].firstChild.data
        self.currentLogger                      = currentLogger
        self.assertion                          = Assertion(confFile,dirPath,currentLogger)
        self.repeatesAllowed                    = False
        self.repeatsType                        = None
        self.oldHttpReq                         = None
        self.validDurationTime                   = 0
        self.lastHeartBeatTime                  = None
        self.grantBeforeHeartBeat               = False

    def process_request(self,httpRequest,typeOfCalling):
                    
        if(self.repeatsType == typeOfCalling and self.repeatesAllowed == True and self.oldHttpReq == httpRequest):
            if(typeOfCalling == consts.HEART_BEAT_SUFFIX_HTTP):
                if(int(self.numberOfHearbeatRequests)<int(self.heartBeatLimitCounter)):
                    self.numberOfHearbeatRequests+=1
                    if(not self.is_Valid_Heart_Beat_Time()):
                        return consts.HEART_BEAT_TIMEOUT_MESSAGE                      
                else:
                    return consts.HEART_BEAT_REACHED_TO_LIMIT_MESSAGE
            self.numberOfStep-=1       
        
        elif(self.Is_Repeats_Available(self.get_Expected_Json_File_Name())):                  
            if(typeOfCalling == consts.SPECTRUM_INQUIERY_SUFFIX_HTTP): 
                if(self.Is_Repeats_Available(self.get_Expected_Json_File_Name())):
                    self.Initialize_Repeats_Type_Allowed(consts.SPECTRUM_INQUIERY_SUFFIX_HTTP,httpRequest, typeOfCalling)
            elif(typeOfCalling == consts.HEART_BEAT_SUFFIX_HTTP):#need to verify that the request before was grant#     
                if(self.validDurationTime == None):
                    return consts.GRANT_BEFORE_HEARTBEAT_ERROR                  
                if(self.Is_Repeats_Available(self.get_Expected_Json_File_Name())):
                    self.Initialize_Repeats_Type_Allowed(consts.HEART_BEAT_SUFFIX_HTTP,httpRequest, typeOfCalling)
                    self.numberOfHearbeatRequests+=1 
                    self.lastHeartBeatTime = DT.datetime.now()        
        else:
            if(typeOfCalling==consts.GRANT_SUFFIX_HTTP):
                self.validDurationTime = self.assertion.get_Duration_Time_From_Grant_Json(self.get_Expected_Json_File_Name())
                self.grantBeforeHeartBeat = True
            elif(typeOfCalling!=consts.HEART_BEAT_SUFFIX_HTTP):
                self.grantBeforeHeartBeat = False
                self.validDurationTime = 0
            self.repeatesAllowed = False
            self.repeatsType = None              
        try:
            self.compare_Json_Req(httpRequest,self.get_Expected_Json_File_Name(),typeOfCalling)  
            self.numberOfHearbeatRequests=0        
        except Exception:
            self.validationErrorAccuredInEngine = True  
            return consts.ERROR_VALIDATION_MESSAGE
        self.oldHttpReq = httpRequest
        return self.process_response(typeOfCalling)
     
    def process_response(self,typeOfCalling):            
        jsonAfterParse = self.parse_Json_To_Dic_By_File_Name(self.get_Expected_Json_File_Name(),consts.RESPONSE_NODE_NAME,self.confFile)
        if(len(self.testDefinietion.jsonNamesOfSteps) == self.numberOfStep+1):
            self.currentLogger.print_And_Log_To_File(consts.NSTEP_SESSION_WITH_TECHNITIAN,True)
            self.questAnswerPartOfJson = self.parse_Json_To_Dic_By_File_Name(self.get_Expected_Json_File_Name(),consts.QUESTION_NODE_NAME,self.confFile)
            self.isLastStepInCSV = True
    
        self.numberOfStep+=1
        return jsonAfterParse
    
    def Is_Repeats_Available(self,expectedJsonName):
        return self.assertion.get_Attribute_Value_From_Json(expectedJsonName,"repeatsAllowed")

    def compare_Json_Req(self,httpRequest,expectedJsonFileName,typeOfCalling):
        self.assertion.compare_Json_Req(httpRequest,expectedJsonFileName,typeOfCalling+consts.REQUEST_NODE_NAME)
    
    def parse_Json_To_Dic_By_File_Name(self,jsonFileName,nodeName,confFile):
        return jsonComparer.get_Node_Of_Json_Parsed(jsonFileName,nodeName,confFile,self.dirPath)
    
    def get_Expected_Json_File_Name(self,numberOfStep = None):
        if(numberOfStep == None):
            numberOfStep = self.numberOfStep
        return self.testDefinietion.jsonNamesOfSteps[numberOfStep]
    
    def get_Question_Answer_Part(self):
        return self.questAnswerPartOfJson
    
    def Initialize_Repeats_Type_Allowed(self,repeatType, httpRequest, typeOfCalling):
        self.repeatsType = repeatType
        self.repeatesAllowed = True
        
    def is_Valid_Heart_Beat_Time(self):
        currentTime = DT.datetime.now()
        timeBetween = (currentTime-self.lastHeartBeatTime).total_seconds()
        if(float(timeBetween)-3.0>float(self.validDurationTime)):
            return False           
        return True
    

    
    
    