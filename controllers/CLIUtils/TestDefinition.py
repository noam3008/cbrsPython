import logging
import model.Utils.Consts as consts

class TestDefinition(object):
    
    def __init__(self,steps):
        self.jsonNamesOfSteps = []
        for step in steps:    
            self.jsonNamesOfSteps.append(step.jsonOfStep)
        
            