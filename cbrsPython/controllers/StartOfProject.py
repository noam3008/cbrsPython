import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from controllers.CLIUtils.TestDefinition import TestDefinition
from controllers.CLIUtils.LoggerHandler import LoggerHandler
import model.Utils.Consts as consts
from xml.dom import minidom
from controllers.CLIHandler import CLIHandler
from controllers.ENodeBController import ENodeBController
from model import flaskServer
from pathlib import Path
from controllers.CLIHandler import CsvFileParser
import ssl

def run_New_Test(dir_path, confFile, loggerHandler):
    '''
    The method start a new test asking the technician which csv file to load from the test repository 
    create a new log file for the test in allTest folder and create if wanted specific log for the test in specific folder 
    that the technician will choose
    running the flask server using the port and ip taken from the config file   
    '''
    loggerHandler.print_To_Terminal(consts.SET_CSV_FILE_MESSAGE)
    inputAnswer = raw_input()
    if (inputAnswer != "quit"):
        try: ### initialize the test definition from the csv file 
            testDefinition = TestDefinition(CsvFileParser(str(dir_path) + confFile.getElementsByTagName("testRepoPath")[0].firstChild.data + inputAnswer).initializeTestDefinition())
        except IOError as e:  ### in case there is file not found error try to enter new csv file name
            loggerHandler.print_To_Terminal(e.message)
            run_New_Test(dir_path, confFile, loggerHandler)
        loggerHandler.print_To_Terminal(consts.ADD_TEST_TO_SPECIFIC_FOLDER_MESSAGE)
        insertToFolderAnswer = raw_input()
        if (insertToFolderAnswer == "yes"):
            loggerHandler.print_To_Terminal("typeNameOfFolder")
            insertToFolderAnswer = raw_input()
            loggerHandler.create_New_Logger(inputAnswer, insertToFolderAnswer) ### if decided to enter to folder create two logs one in the all test folder ### if decided to enter to folder create two logs one in the all test folder
            loggerHandler.print_And_Log_To_File(consts.SELECT_TO_ADD_TEST_MESSAGE+ inputAnswer + consts.SELECT_TO_ADD_FOLDER_MESSAGE 
                                                + insertToFolderAnswer, True)
        else:
            loggerHandler.create_New_Logger(inputAnswer)
            loggerHandler.print_And_Log_To_File(consts.SELECTED_TEST_FROM_USER_MESSAGE + str(inputAnswer), True)
        cliHandler = CLIHandler(inputAnswer, confFile, dir_path, loggerHandler,testDefinition) ### initialize cli session handler
        flaskServer.enodeBController = ENodeBController(cliHandler.engine) 
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2) # use TLS to avoid POODLE
        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.load_verify_locations(str(dir_path) + cliHandler.get_Element_From_Config_File("caCerts"))
        ctx.load_cert_chain(str(dir_path) + cliHandler.get_Element_From_Config_File("pemFilePath"), str(dir_path) + cliHandler.get_Element_From_Config_File("keyFilePath"))## get the certificates for https from config file
        flaskServer.runFlaskServer(cliHandler.get_Element_From_Config_File("hostIp"),cliHandler.get_Element_From_Config_File("port"),ctx) ### run flask server using the host name and port  from conf file
        if (cliHandler.engine.validationErrorAccuredInEngine):
            cliHandler.stop_Thread_Due_To_Exception()
    cliHandler.stop_Thread_Due_To_Exception()

current_path = os.path.dirname(os.path.realpath(__file__))
dir_path = Path(__file__).parents[2]
confFile= minidom.parse(current_path +"\conf.xml") ### initialize the conf file using 2 parents from the current running py file 
loggerHandler = LoggerHandler(dir_path)
loggerHandler.create_New_Logger(consts.CLI_SESSION) ### create a logger for the entire cmd session of all the test that are in the current running
run_New_Test(dir_path, confFile, loggerHandler)

''' exampleTest.csv'''
'''exampleTestWithRegistration.csv'''
'''grantFailureTest'''