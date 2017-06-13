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
        '''
        the method perform validation to the current httpRequest json 
        '''
        ### in case that the request is the same as the last one and the repeats allowed dig in the next loop
        if(self.repeatsType == typeOfCalling and self.repeatesAllowed == True and self.oldHttpReq == httpRequest):
            ### in case its an heartbeat calling need to check if it is cross the limit 
            ###counter get from the config file or heartbeat call 
            ###passed the timeout that get from the last grant response         
            if(typeOfCalling == consts.HEART_BEAT_SUFFIX_HTTP):
                if(int(self.numberOfHearbeatRequests)<int(self.heartBeatLimitCounter)):
                    self.numberOfHearbeatRequests+=1
                    if(not self.is_Valid_Heart_Beat_Time()):
                        return consts.HEART_BEAT_TIMEOUT_MESSAGE                      
                else:
                    return consts.HEART_BEAT_REACHED_TO_LIMIT_MESSAGE
            self.numberOfStep-=1### if its repeat type json number of step should be the same as it was before

        elif(self.Is_Repeats_Available(self.get_Expected_Json_File_Name(),typeOfCalling)==True):
            if(typeOfCalling == consts.SPECTRUM_INQUIERY_SUFFIX_HTTP): 
                self.Initialize_Repeats_Type_Allowed(consts.SPECTRUM_INQUIERY_SUFFIX_HTTP,httpRequest, typeOfCalling)
            elif(typeOfCalling == consts.HEART_BEAT_SUFFIX_HTTP):#need to verify that the request before was grant#    
                if(self.validDurationTime == None):
                    return consts.GRANT_BEFORE_HEARTBEAT_ERROR                  
                self.Initialize_Repeats_Type_Allowed(consts.HEART_BEAT_SUFFIX_HTTP,httpRequest, typeOfCalling)
                self.numberOfHearbeatRequests+=1 
                self.lastHeartBeatTime = DT.datetime.now()        
        else:
            if(typeOfCalling==consts.GRANT_SUFFIX_HTTP):
                self.grantBeforeHeartBeat = True
                self.numberOfHearbeatRequests=0
            elif(typeOfCalling!=consts.HEART_BEAT_SUFFIX_HTTP):
                self.grantBeforeHeartBeat = False
                self.validDurationTime = 0
                self.numberOfHearbeatRequests=0
            elif(typeOfCalling==consts.HEART_BEAT_SUFFIX_HTTP):
                ### checks that heartbeat request has been sent only after grant or another heartbeat
                if(not self.grantBeforeHeartBeat):
                    return consts.GRANT_BEFORE_HEARTBEAT_ERROR 
            self.repeatesAllowed = False
            self.repeatsType = None              
        try:
            self.compare_Json_Req(httpRequest,self.get_Expected_Json_File_Name(),typeOfCalling)  
                    
        except Exception as e:
            self.validationErrorAccuredInEngine = True  
            return e.message
        if(typeOfCalling==consts.GRANT_SUFFIX_HTTP):
            ### if it is a grant request we need to initialize the valid duration time between the heartbeats
            self.validDurationTime = self.assertion.get_Duration_Time_From_Grant_Json(self.get_Expected_Json_File_Name())
        self.oldHttpReq = httpRequest       
        return self.process_response(typeOfCalling)
     
    def process_response(self,typeOfCalling):  
        '''
        the method sent response to the CBSD from the engine after taking the response from the expected json 
        if this is the last step in the csv file it look for the question part inside the json and presenting it to the cli        
        '''          
        jsonAfterParse = self.parse_Json_To_Dic_By_File_Name(self.get_Expected_Json_File_Name(),consts.RESPONSE_NODE_NAME,self.confFile)
        if(len(self.testDefinietion.jsonNamesOfSteps) == self.numberOfStep+1):
            self.currentLogger.print_And_Log_To_File(consts.NSTEP_SESSION_WITH_TECHNITIAN,True)
            self.questAnswerPartOfJson = self.parse_Json_To_Dic_By_File_Name(self.get_Expected_Json_File_Name(),consts.QUESTION_NODE_NAME,self.confFile)
            self.isLastStepInCSV = True
    
        self.numberOfStep+=1
        return jsonAfterParse
    
    def Is_Repeats_Available(self,expectedJsonName,typeOfCalling):
        '''
        the method checks if the calling is a heartbeat or spectrum type and get the repeatsAllowed value from the expectedJson
        '''
        if(typeOfCalling!= consts.HEART_BEAT_SUFFIX_HTTP and typeOfCalling!= consts.SPECTRUM_INQUIERY_SUFFIX_HTTP):
            return False
        return bool(self.assertion.get_Attribute_Value_From_Json(expectedJsonName,"repeatsAllowed"))

    def compare_Json_Req(self,httpRequest,expectedJsonFileName,typeOfCalling):
        self.assertion.compare_Json_Req(httpRequest,expectedJsonFileName,typeOfCalling+consts.REQUEST_NODE_NAME)
    
    def parse_Json_To_Dic_By_File_Name(self,jsonFileName,nodeName,confFile):
        try:
            return jsonComparer.get_Node_Of_Json_Parsed(jsonFileName,nodeName,confFile,self.dirPath)
        except Exception as e:
            if e.message == "node not exists":
                return consts.SUFFIX_NOT_EXISTS_IN_EXPECTED_JSON_FILE
    
    def get_Expected_Json_File_Name(self,numberOfStep = None):
        if(numberOfStep == None):
            numberOfStep = self.numberOfStep
        return self.testDefinietion.jsonNamesOfSteps[numberOfStep]
    
    def get_Question_Answer_Part(self):
        return self.questAnswerPartOfJson
    
    def Initialize_Repeats_Type_Allowed(self,repeatType, httpRequest, typeOfCalling):
        '''
        the method initialize the repeat type and the boolean that indicates that repeats are allowed
        '''
        self.repeatsType = repeatType
        self.repeatesAllowed = True
        
    def is_Valid_Heart_Beat_Time(self):
        ''''
        the method get the current time and compare the time that had passed from the last heartbeat
        check if it is less then what pulled from the last grant response
        '''
        currentTime = DT.datetime.now()
        timeBetween = (currentTime-self.lastHeartBeatTime).total_seconds()
        if(float(timeBetween)-3.0>float(self.validDurationTime)):
            return False           
        return True
    

    
    
    