import logging


class TestDefinition(object):
    
    def __init__(self,steps):
        logging.info("init the test definition by the test steps sent from the user")
        self.defenitionsOfSteps = []
        self.jsonNamesOfSteps = []
        for step in steps:    
            self.defenitionsOfSteps.append(step.defOfStep)
            self.jsonNamesOfSteps.append(step.jsonOfStep)
            