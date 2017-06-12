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
  
  
  

  
