'''
Created on Apr 26, 2017

@author: iagmon
'''
class QuestionHandler(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def ShowQuestionsAndGetAnswersFromClient(self,questionsAndAnswers):
        answers = []
        correctAnsweres = True
        for questAnswer in questionsAndAnswers:          
            print "hey the question is : " + questAnswer["question"] + " please choose one of the answers : " 
            for answer in questAnswer["answers"]:
                print answer 
            
            inputAnswer = raw_input()
            if not inputAnswer == questAnswer["expectedAnswer"]:
                correctAnsweres = False
            
        return correctAnsweres
            
