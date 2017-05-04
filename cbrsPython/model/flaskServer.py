from flask import Flask,request,jsonify,g,redirect,url_for,abort, app
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
    logging.info(consts.SENT_FLASK_REQUEST)
    json_dict = json.loads(request.data,object_pairs_hook=OrderedDict)
    while (len(enodeBController.engine.testDefinietion.jsonNamesOfSteps)> enodeBController.engine.numberOfStep):
        response = enodeBController.linker_Between_Flask_To_Engine(json_dict,typeOfCalling)
        print "response in flask " + str(response)
        if(consts.ERROR_VALIDATION_MESSAGE in str(response)):     
            return redirectShutDownDueToAnValidationError()
        return jsonify(response)
    return redirectShutDownDueToFinishOfTest()
        
@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    func = request.environ.get(consts.NAME_OF_SERVER_WERKZUG)
    func()
    if(consts.ERROR_VALIDATION_MESSAGE in str(request.args['validationMessage'])):
        abort(400, consts.ERROR_VALIDATION_MESSAGE)
    return consts.SERVER_SHUT_DOWN_MESSAGE + consts.TEST_HAD_BEEN_FINISHED_FLASK

def redirectShutDownDueToFinishOfTest():
        return redirect(url_for(consts.SHUTDOWN_FUNCTION_NAME, validationMessage=consts.TEST_HAD_BEEN_FINISHED_FLASK))
    
    
def redirectShutDownDueToAnValidationError():
    return redirect(url_for(consts.SHUTDOWN_FUNCTION_NAME, validationMessage=consts.ERROR_VALIDATION_MESSAGE))


def runFlaskServer(host):
    app.run(host)
    



