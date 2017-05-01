from flask import Flask,request,jsonify,g,redirect,url_for,abort
import sys
from controllers.ENodeBController import ENodeBController
import logging
import Utils.Consts as consts
from flask.templating import render_template
app = Flask(__name__)

enodeBController = ENodeBController(None)
@app.route('/cbsd/<typeOfCalling>/',methods=['POST'])
def sentFlaskReqToServer(typeOfCalling):
    logging.info(consts.SENT_FLASK_REQUEST)
    validationErrorMessage = consts.ERROR_VALIDATION_MESSAGE
    #while (len(enodeBController.engine.testDefinietion.jsonNamesOfSteps)> enodeBController.engine.numberOfStep) :    
    if(len(enodeBController.engine.testDefinietion.jsonNamesOfSteps)< enodeBController.engine.numberOfStep):
        return "the test had been finished"  
    response = enodeBController.linkerBetweenFlaskToEngine(request.get_json(),typeOfCalling)
    print "response in flask " + str(response)
    if(consts.ERROR_VALIDATION_MESSAGE in str(response)):
        abort(400, consts.ERROR_VALIDATION_MESSAGE)

        
        #if(validationErrorMessage in response):
            #return redirect(url_for(consts.SHUTDOWN_FUNCTION_NAME, validationMessage=validationErrorMessage))
    return jsonify(response)
    #return redirect(url_for(consts.SHUTDOWN_FUNCTION_NAME, validationMessage=consts.TEST_HAD_BEEN_FINISHED_FLASK))
        
@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    func = request.environ.get(consts.NAME_OF_SERVER_WERKZUG)
    func()
    shutDownMessage =consts.SERVER_SHUT_DOWN_MESSAGE + str(request.args['validationMessage'])
    logging.info (shutDownMessage)
    return shutDownMessage


def runFlaskServer():
    app.run(host="70.14.0.72")
    



