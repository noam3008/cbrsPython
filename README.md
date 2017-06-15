# cbrsPython
the project main goal is to be a mock-sas that will handle the CBRS requests

# prerequisite
python 2.7
java

# installation
for install the site packages requested for the project
incide the cmd change dir to the python installation dir
change dir to the scripts dir and enter the command:
pip install -r "the path of the project/requirements.txt"

# getting started
  # create a csv file 
  each column in the csv file should contain first row as : 
  "jsonFileName1" for the first CBRS
  "jsonFileName2" for the second CBRS and etc. depend on the amount of cbrs you wish to check
  the rest row of the csv should contain the expected jsons you wish to check
  
  # create jsons
  each json should contain a calling request and response
  for example if the type of calling is registration
  the json should contain nodes of "registrationRequest" and "response" node
  
  # optional params
  each type of calling (registration,grant,heartbeat,spectrumInquiery,relinquishment)
  will have a json file inside the folder OptionalParams that contains
  key and values that in case you have an optional key 
  that the request not must include this parameter
  but if it includes it you want to validate it you can add them to this file
  (if the key will be in both of the jsons the validation will check only the value
  that is in the original json)
  
  
  # range values
  json value can be in the type of range , inside the value 
  you should enter "${range:0To50} and if the post from the 
  CBRS will be in the range the validation will succedded
  
  # or values
  json value can be in type of or, inside the value 
  you should enter {"$or":["EUTRA_CARRIER_RSSI_NON_TX","EUTRA_CARRIER_RSSI_ALWAYS"]}
  and if the post will contain one of the values the validation will pass
  
  # length values
  json value can be in type of length, inside the value 
  you should enter "${maximumLength:128}"
  and if the post will contain value with less chars than the maximum length
  the validation will pass
  
  # heartBeat jsons
  the heartbeat json should contains also boolean "repeatsAllowed" key 
  that will point if repeats are allowed from this heartbeat request
  if you have two diffrent heartbeats request that the first will be only one time
  and the second type will return few times each of the heartbeats expected json should
  be inserted in the csv file but only the second will have "repeatsAllowed" true key
  
  the heartbeatInterval key point how long the time to wait between heartbeats
  if the time will be too short and the heartbeat will take more time than
  written in the heartbeat the test will fail
  
  the "transmitExpireTime" key in response is optional if not be inserted in the expected
  json it will be taken with the pc time plus the "secondsToAddForExpireTime" from
  the CBRS conf file added in the project itself in model.CBRSConf folder
  
  the conf file of the entire project which located in the path controllers/conf.xml
  contains a value of "heartbeatLimit" it point how many heartbeat from the same request
  you allowed the engine to get from the CBRS itself
  
  # spectrum inquiery jsons
  the spectrum json should contains also boolean "repeatsAllowed" key 
  that will point if repeats are allowed from this spectrum request
  
  if you have two diffrent spectrum request that the first will be only one time
  and the second type will return few times each of the spectrum expected json should
  be inserted in the csv file but only the second will have "repeatsAllowed" true key
  
  # grant jsons
  the "grantExpireTime" key in response is optional if not be inserted in the expected
  json it will be taken with the pc time plus the "secondsToAddForExpireTime" from
  the CBRS conf file added in the project itself in model.CBRSConf folder
  
  # running project
  for running the project after you did the installation, create csv and jsons
  inside the conf.xml of the entire project change the ip to your computer ip
  you should enter the cmd change dir to the python and insert the command:
  python (pathOfTheProject/cbrsPython/controllers/startOfProject.py)
  after that the engine will check which test you wish to test
  the second question is if you want to enter it to a folder
  
  by entering to exists folder or create new folder you will have the ability 
  to get statistic on group of tests 
   
  # questions answer part  
  if all the steps had passed successfully you will reached to the question answeres part
  inside the expected json of the json file name inserted in the last row of the csv
  you should enter a node that will look similar to this :
  "questions":
	[
		{
			"question" : "OK?",
			"answers" : ["y", "n"], 
			"expectedAnswer" : "y"
		}
	],
    
    if the client will answer to the question as expected answer value the test will pass
  
  # classes explanation
  
  # flaskServer.py 
  	           the class is handle all the session of the cbrs rest calling and response from the engine to the eNodeB
  	           the class have three method:
		   sent_Flask_Req_To_Server() - taking the request from the CBRS parse the json to a dict
		   and send it to the engine
		   shutdown() - in case of validation error during the engine validate the engine will sent a string "ERROR - specific 		           message", this will activate the shutdown function that sent an abort - 400 message to the CBRS.
		   runFlaskServer() - the method will get a port,ip,certificates and will create an https server
		   
 # engine.py 
     the class get the request from the flask server seperate to single CBRS request (in case its a domain proxy the request will
     have more than one cbrs request ) and send the request to the CBRS obj 
     the class methods:
     process_request() - the method seperate to specific cbrsObj request , in case its registration request he create an cbrsObj class
     that the identifier of the class will be the "cbsdSerialNumber" if its other request as (spec,grant...) it send the request to an
     existing cbrsObj by the value sent from the request of "cbsdId" that contains the cbsdSerialNumber inside the value.
     the class also manage the response if the request was build from an array of two reg request he will send array of two also in the      response.
     check_Last_Step_In_All_CBRS() - the method pass on all the cbrs obj that is available (check if the csv file column is equal to the      registerd CBRS obj) and then check if all the registered cbrs are finish validating the last step.
     get_Question_Answer_Part() - the method get all the question answer part from the cbrs obj.
     
# CBRSRequestHandler.py 
    the class is responsible of all the cbrs obje initialize from the json handling the request and sending the response to the CBRS
    this is the main validation class the massive logic of the engine is made in this class
    the method are:
    set_Current_Json_Steps() - the only way to build the cbrsObj class is to have registration request (all the test must start with         registation), the method enter to the registrationRequest node and it passes on all the csv column, if the first row in column  	     expected json contain the same cbsdSerialNumber sent from the flask it initialize all the expected json array from this column in       the csv (if two column first json will have the same value it will initilize by the first column only) , it search the specific xml     file (every cbrs obj that should be tested in the test should have an specific conf xml in the directory model.CBRSConf 
    handle_Http_Req() - the main method of the project that make all the validation of the request from the flask,
    - spectrum request : it checks if repeats are allowed (spectrum inquery request can show everywhere         after the registration       response, but if you want to get spectrum inquery you must specified it in the csv file and if you want to       have many of the       same request the expected json should include variable of repeatsAllowed inside.
    - grant request : it initialize the grant expire time from the config file it add to pc time the value of the config file in             minutes, it indicates that an grant request recived because an heartbeat request can be only after grant or after another heartbeat
    -heartbeat : check if the heartbeat contains repeats allowed true value, check if grant request has arrived before already,
    initialize the transmition time from the CBRSobj config file , check that the time between each heartbeats is less than given in the     "heartbeatInterval" key in grant request and check if the counter of the heartbeat from the same type is less then whats given in       the main config file of the project.
    all the class have methods that serve what ive written above about the calling type
# JsonComparisonUtils.py
    the class handle all the json file , it gets json from the expected repo and the json from the request and make some validation of       the jsons.
    at the start of the readme file i explained that jsons can have range,or,length type of value the class know to handle this values       type also
    the class have method that know to take json and add key and value to the json after the creation.
# consts.py
    the class olds consts string variable that can be used in each class of the project
# assert.py
    the class make the assertion of the expected json and the request json
    the class have few methods:
    compare_Json_Req() - the method get the request from the CBRS gets the expected json file name and sent to the jsonComparisonUtils       class to make the validation and check if the validation pass, it have the possibility to add to the expected json key and values       from the cbrsObj config file.
    get_Attribute_Value_From_Json() - checks if the json have the specific key and return some value.
    add_Json_Optional_Parameters() - each request suffix as registration,spec and etc. have json that includes an optional parameters
    if the request have some key and the original expected json dont have the key inside it search the key in the optionalParameters         json file and add it to the expected json
# LogObserver.py
    this logObserver is an observerPattern it handle all the logs methods such as startStep,EndStep,startTest,endTest
    and send it to all the listeners logs (for now it have three listeners: debugLog,cmdLog and xmlLog)
# xmlLogger.py 
    this class initialize the html report by the test status and step status handle few tests the inserted to the same folder from the       start of the test.
# debugLogger.py
    this class is listener of the logobserver class and specified all the request and response jsons the cli session at the end of the       test and the finalresult of the test
# cmdLogger.py
    the class is listener of the logObserver class and save the current cmd session as it shown in the cli.
# startOfProject.py
    the start of the test is starting when run this py file the class is handle the valid csv file input, the folder name to insert the    test, add the loggers to the loggerObserver and run the flask server, initialize the main conf file.
# CLIHandler.py
    this method holds a thread that in case of an error start a new test session as explained in the startOfProject.py above and in case     the test finished and get to the last csv steps its open a session of the questionAnswer part

   
   
    

    
     
     

   
  
		   
  

  
