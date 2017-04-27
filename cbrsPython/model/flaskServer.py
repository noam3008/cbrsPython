from flask import Flask,request,jsonify,g
from controllers.ENodeBController import ENodeBController
app = Flask(__name__)

enodeBController = ENodeBController(None)
@app.route('/cbsd/<typeOfCalling>',methods=['POST'])
def sentFlaskReqToServer(typeOfCalling):
    return jsonify(enodeBController.linkerBetweenFlaskToEngine(request.get_json()))

def runFlaskServer():
    app.run()
    



