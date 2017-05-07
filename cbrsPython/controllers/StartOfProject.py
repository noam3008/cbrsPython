import logging
import model.Utils.Consts as consts
from xml.dom import minidom
from controllers.CLIHandler import CLIHandler
from controllers.ENodeBController import ENodeBController
from model import flaskServer

print (consts.SET_CSV_FILE_MESSAGE)  
confFile = minidom.parse("conf.xml")
logging.info(consts.START_TEST_MESSAGE)

inputAnswer=raw_input()     
cliHandler = CLIHandler(inputAnswer) 
flaskServer.enodeBController = ENodeBController(cliHandler.engine)
flaskServer.runFlaskServer(confFile.getElementsByTagName("hostIp")[0].firstChild.data)
if(cliHandler.engine.validationErrorAccuredInEngine):
    cliHandler.stop_Thread_Due_To_Exception()

    
''' exampleTest.csv'''
'''exampleTestWithRegistration.csv'''