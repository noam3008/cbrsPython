from flask import Flask,request,jsonify,g,redirect,url_for,abort
import sys
from controllers.ENodeBController import ENodeBController
import logging
import Utils.Consts as consts
import os
app = Flask(__name__)

enodeBController = ENodeBController(None)
@app.route('/cbsd/<typeOfCalling>/',methods=['POST'])
def sent_Flask_Req_To_Server(typeOfCalling):
    logging.info(consts.SENT_FLASK_REQUEST)
    validationErrorMessage = consts.ERROR_VALIDATION_MESSAGE
    while (len(enodeBController.engine.testDefinietion.jsonNamesOfSteps)> enodeBController.engine.numberOfStep) :     
        response = enodeBController.linker_Between_Flask_To_Engine(request.get_json(),typeOfCalling)
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


def runFlaskServer():
    app.run(host="70.14.0.72")
    



