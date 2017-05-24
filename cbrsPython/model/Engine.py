'''
Created on Apr 20, 2017

@author: iagmon
'''

from model.Utils.Assert import Assertion 
import model.Utils.JsonComparisonUtils as jsonComparer
import model.Utils.Consts as consts
import datetime as DT
from model.CBRSObject import CBRSObject as cbrsObj
from Tkconstants import FIRST


class MyEngine(object):

    def __init__(self,testDefinition,confFile,dirPath,currentLogger):
        self.numberOfStep                       = 0
        self.numberOfHearbeatRequests           = 0
        self.testDefinition                    = testDefinition
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
        self.validDurationTime                  = 0
        self.lastHeartBeatTime                  = None
        self.grantBeforeHeartBeat               = False
        self.cbrsObjArray                       = []
        self.allTheCBRSRegistered               = False

    def process_request(self,httpRequest,typeOfCalling):
        '''
        the method perform validation to the current httpRequest json 
        '''
        nodeResponse = typeOfCalling+consts.RESPONSE_NODE_NAME.title()
        i = 0
        for httpReq in httpRequest[typeOfCalling+consts.REQUEST_NODE_NAME]:
            
            if(typeOfCalling=="registration"):
                try:
                    self.add_Cbrs_Obj(httpReq["fccId"])
                except:
                    self.validationErrorAccuredInEngine = True
                    return consts.JSON_REQUEST_NOT_INCLUDE_KEY + " fccId " 
                try:
                    if(i==0):
                        response = self.handle_Http_Req(httpReq["fccId"],httpReq,typeOfCalling)
                        self.raise_In_Case_Of_An_Error(response)
                    elif (i>0):
                        tempResp = self.handle_Http_Req(httpReq["fccId"],httpReq,typeOfCalling)
                        self.raise_In_Case_Of_An_Error(response)
                        response[nodeResponse].append(tempResp[nodeResponse][0])
                except Exception as E:
                    self.validationErrorAccuredInEngine = True
                    return "for the CBRS with the fccId :" + str(httpReq["fccId"]) + E.message
                    
                    
            else:
                try:
                    reqIndex = str(httpReq["cbsdId"]).index("cbsd")
                except : 
                    self.validationErrorAccuredInEngine = True
                    return consts.JSON_REQUEST_NOT_INCLUDE_KEY + " cbsdId " 
                try:
                    if(i==0):
                        response = self.handle_Http_Req(str(httpReq["cbsdId"])[:reqIndex], httpReq, typeOfCalling)
                        self.raise_In_Case_Of_An_Error(response)
                    elif (i>0):
                        tempResp = self.handle_Http_Req(httpReq["cbsdId"][:reqIndex],httpReq,typeOfCalling)
                        self.raise_In_Case_Of_An_Error(response)
                        response[nodeResponse].append(tempResp[nodeResponse][0])               
                except Exception as E:
                    self.validationErrorAccuredInEngine = True
                    return "for the CBRS with the fccId :" + str(httpReq["fccId"]) + E.message
            i+=1
        if(typeOfCalling==consts.REGISTRATION_SUFFIX_HTTP):
            self.allTheCBRSRegistered = True
        return response
                    
    
    def add_Cbrs_Obj(self,fccIdAttr):
        tempCbrsObj = cbrsObj(fccIdAttr, self.testDefinition, self.confFile, self.dirPath,self.currentLogger)
        if tempCbrsObj not in self.cbrsObjArray:
            self.cbrsObjArray.append(tempCbrsObj)
        del tempCbrsObj
    
    def handle_Http_Req(self,fccIdAttr,httpReq,typeOfCalling):
        for cbrsObj in self.cbrsObjArray: 
            if cbrsObj.fccId == fccIdAttr:
                return cbrsObj.handle_Http_Req(httpReq,typeOfCalling)
        self.validationErrorAccuredInEngine = True
        raise IOError("ERROR - there is no cbrs obj registered with the fccId :  " + str(fccIdAttr) )
    
    def check_Validation_Error(self):
        if self.validationErrorAccuredInEngine == True:
            return True
        for cbrsObj in self.cbrsObjArray: 
            if cbrsObj.validationErrorAccuredInEngine ==True:
                return True
        return False
        
    def raise_In_Case_Of_An_Error(self,response):
        if "ERROR" in response:
            raise IOError(response)
        
    def check_Last_Step_In_All_CBRS(self):
        if(self.allTheCBRSRegistered == True):
            for cbrsObj in self.cbrsObjArray:
                print cbrsObj.fccId 
                if(cbrsObj.isLastStepInCSV == False):
                    return False
            if(len(self.cbrsObjArray)==0):
                return False
            self.currentLogger.print_And_Log_To_File(consts.NSTEP_SESSION_WITH_TECHNITIAN,True)
            return True
        return False
    
    def get_Question_Answer_Part(self):
        i=0
        for cbrsObj in self.cbrsObjArray:
            if(i==0):
                tempQuestAnswerPart = cbrsObj.get_Question_Answer_Part()
            if len(self.cbrsObjArray) == 1:
                return tempQuestAnswerPart
            elif(i>0):
                tempResp = cbrsObj.get_Question_Answer_Part()
                tempQuestAnswerPart["questions"].append(tempResp["questions"][0])       
        return tempQuestAnswerPart        
        
        
        
            
        
        
    

    
    
    