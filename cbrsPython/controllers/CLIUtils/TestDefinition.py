import logging
import model.Utils.Consts as consts

class TestDefinition(object):
    
    def __init__(self,steps):
        logging.info(consts.INIT_TEST_DEFINITION)
        self.defenitionsOfSteps = []
        self.jsonNamesOfSteps = []
        for step in steps:    
            self.defenitionsOfSteps.append(step.defOfStep)
            self.jsonNamesOfSteps.append(step.jsonOfStep)
            