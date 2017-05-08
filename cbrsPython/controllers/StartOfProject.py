import logging
import sys
import os.path
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import model.Utils.Consts as consts
from xml.dom import minidom
from controllers.CLIHandler import CLIHandler
from controllers.ENodeBController import ENodeBController
from model import flaskServer
from pathlib import Path

current_path = os.path.dirname(os.path.realpath(__file__))
logs_path =  Path(__file__).parents[2]
logging.basicConfig(format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                filename=str(logs_path) +'\logs\session_' + str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) +'.log',
                filemode='w',
                level=logging.INFO)

dir_path = Path(__file__).parents[2] 
print dir_path
confFile= minidom.parse(current_path +"\conf.xml")
print (consts.SET_CSV_FILE_MESSAGE)  
logging.info(consts.START_TEST_MESSAGE)
inputAnswer=raw_input()   
logging.info("the selected test from the user is : " + inputAnswer)  
cliHandler = CLIHandler(inputAnswer,confFile,dir_path) 
flaskServer.enodeBController = ENodeBController(cliHandler.engine)
flaskServer.runFlaskServer(confFile.getElementsByTagName("hostIp")[0].firstChild.data)
if(cliHandler.engine.validationErrorAccuredInEngine):
    cliHandler.stop_Thread_Due_To_Exception()

    
''' exampleTest.csv'''
'''exampleTestWithRegistration.csv'''