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

def run_New_Test(dir_path, confFile, loggerHandler):
    loggerHandler.print_To_Terminal(consts.SET_CSV_FILE_MESSAGE)
    inputAnswer = raw_input()
    if (inputAnswer != "quit"):
        try:
            testDefinition = TestDefinition(CsvFileParser(str(dir_path) + confFile.getElementsByTagName("testRepoPath")[0].firstChild.data + inputAnswer).initializeTestDefinition())
        except IOError as e:
            loggerHandler.print_To_Terminal(e.message)
            run_New_Test(dir_path, confFile, loggerHandler)
        loggerHandler.print_To_Terminal(consts.ADD_TEST_TO_SPECIFIC_FOLDER_MESSAGE)
        insertToFolderAnswer = raw_input()
        if (insertToFolderAnswer == "yes"):
            loggerHandler.print_To_Terminal("typeNameOfFolder")
            insertToFolderAnswer = raw_input()
            loggerHandler.create_New_Logger(inputAnswer, insertToFolderAnswer)
            loggerHandler.print_And_Log_To_File(consts.SELECT_TO_ADD_TEST_MESSAGE+ inputAnswer + consts.SELECT_TO_ADD_FOLDER_MESSAGE + insertToFolderAnswer, True)
        else:
            loggerHandler.create_New_Logger(inputAnswer)
            loggerHandler.print_And_Log_To_File(consts.SELECTED_TEST_FROM_USER_MESSAGE + str(inputAnswer), True)
        cliHandler = CLIHandler(inputAnswer, confFile, dir_path, loggerHandler,testDefinition)
        flaskServer.enodeBController = ENodeBController(cliHandler.engine)
        flaskServer.runFlaskServer(confFile.getElementsByTagName("hostIp")[0].firstChild.data)
        if (cliHandler.engine.validationErrorAccuredInEngine):
            cliHandler.stop_Thread_Due_To_Exception()
    cliHandler.stop_Thread_Due_To_Exception()


current_path = os.path.dirname(os.path.realpath(__file__))
dir_path = Path(__file__).parents[2]
confFile= minidom.parse(current_path +"\conf.xml")
loggerHandler = LoggerHandler(dir_path)
loggerHandler.create_New_Logger(consts.CLI_SESSION)
run_New_Test(dir_path, confFile, loggerHandler)

''' exampleTest.csv'''
'''exampleTestWithRegistration.csv'''