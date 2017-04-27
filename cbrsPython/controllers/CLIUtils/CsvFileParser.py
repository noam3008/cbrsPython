'''
Created on Apr 25, 2017

@author: iagmon
'''
import csv
from controllers.CLIUtils.Step import Step
class CsvFileParser(object):
    '''
    classdocs
    '''


    def __init__(self,csvFileName):
        '''
        Constructor
        '''
        self.csvFileName = csvFileName
        
    def initializeTestDefinition(self):
        steps = []
        with open(self.csvFileName) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:         
                steps.append(Step(row['stepType'], row['jsonFileName']))
        return steps



