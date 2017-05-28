'''
Created on May 9, 2017

@author: iagmon
'''
import logging
from datetime import datetime
import os
from model.Utils import Consts as consts
class LoggerHandler(object):

    def __init__(self,dirPath):
        self.dirPath = dirPath
        self.currentLoggerName = []

    def addLoggerFile(self, logger_name, log_file):
        log_setup = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        fileHandler = logging.FileHandler(str(self.dirPath) + log_file, mode='a')
        fileHandler.setFormatter(formatter)
        log_setup.addHandler(fileHandler)
        log_setup.setLevel(logging.INFO)
        self.currentLoggerName.append(log_setup.name)

    def create_New_Logger(self,logger_name, folder_name= None):
        if(logger_name == consts.CLI_SESSION):
            log_file =  '\Logs\CMDSessions\cmdSession_' + str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) +'.log'
            self.addLoggerFile(logger_name, log_file)
        if (folder_name!=None):
            self.create_new_dir_and_log(logger_name,folder_name)       
        if(logger_name!=consts.CLI_SESSION):  
            log_file =  '\Logs\LogsPerTest\_'+logger_name+"_" + str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) +'.log'        
            self.addLoggerFile(logger_name, log_file)
        
    def create_new_dir_and_log(self,logger_name, folder_name):
        newpath = str(self.dirPath)+ str(r'\\Logs\\SpecificFolderOfTests\\' + folder_name)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        log_file =  '\\Logs\\SpecificFolderOfTests\\'+folder_name+"\\_"+logger_name+"_" + str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) +'.log'  
        self.addLoggerFile(logger_name+folder_name, log_file)
        
    def remove_Test_File_Logger(self):
        result = []
        for item in self.currentLoggerName:
            if item == consts.CLI_SESSION:
                result.append(item)
        self.currentLoggerName = result
             

    def print_And_Log_To_File(self,msg,printToTerminal, level="info"): 
        for logName in self.currentLoggerName :
            if(logName!=consts.CLI_SESSION):     
                log = logging.getLogger(logName)
                if level == 'info'    : log.info(msg) 
                if level == 'warning' : log.warning(msg)
                if level == 'error'   : log.error(msg)
            elif(printToTerminal):
                self.print_To_Terminal(msg)
    
    def print_To_Terminal(self,msg):
        log = logging.getLogger(consts.CLI_SESSION)
        log.info(msg)
        print msg          
        
    def get_Logger_By_Test_Name(self,nameOfLogger):
        log = logging.getLogger(nameOfLogger)
        return log