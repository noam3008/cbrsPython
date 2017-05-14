from flask import Flask,request,jsonify,g,redirect,url_for,abort
from controllers.ENodeBController import ENodeBController
import logging
import Utils.Consts as consts
from collections import OrderedDict
import json
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

enodeBController = ENodeBController(None)
@app.route('/cbsd/<typeOfCalling>/',methods=['POST'])
def sent_Flask_Req_To_Server(typeOfCalling):
    logger = enodeBController.engine.currentLogger
    json_dict = json.loads(request.data,object_pairs_hook=OrderedDict)
    logger.print_And_Log_To_File(json.dumps(json_dict, indent=4, sort_keys=True),False)
    logger.print_To_Terminal("CBSD sent " + str(typeOfCalling) +" " + consts.REQUEST_NODE_NAME)
    while (len(enodeBController.engine.testDefinietion.jsonNamesOfSteps)> enodeBController.engine.numberOfStep):
        response = enodeBController.linker_Between_Flask_To_Engine(json_dict,typeOfCalling)
        logger.print_And_Log_To_File("response from engine to CBSD " + json.dumps(response, indent=4, sort_keys=True),False)
        if("ERROR" in str(response)):
            return redirect(url_for(consts.SHUTDOWN_FUNCTION_NAME, validationMessage=str(response)))           
        logger.print_To_Terminal("engine sent " + str(typeOfCalling) + " " +consts.RESPONSE_NODE_NAME)
        return jsonify(response)
    return redirectShutDownDueToFinishOfTest()
        
@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    logger = enodeBController.engine.currentLogger
    app.app_context()
    func = request.environ.get(consts.NAME_OF_SERVER_WERKZUG)
    func()
    if("ERROR" in str(request.args['validationMessage'])):
        abort(400, str(request.args['validationMessage']))
        logger.print_And_Log_To_File("the server shot down due to " + str(request.args['validationMessage']))   
    return consts.SERVER_SHUT_DOWN_MESSAGE + consts.TEST_HAD_BEEN_FINISHED_FLASK

def redirectShutDownDueToFinishOfTest():
        return redirect(url_for(consts.SHUTDOWN_FUNCTION_NAME, validationMessage=consts.TEST_HAD_BEEN_FINISHED_FLASK))


def runFlaskServer(host):
    app.run(host,threaded=True)
    



