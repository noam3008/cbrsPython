'''
Created on Apr 26, 2017

@author: iagmon
'''
import model.Utils.Consts as consts
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
            print "hey the question is : " + questAnswer[consts.QUESTION_NODE] + consts.CHOOSE_ONE_OF_THE_ANSWERS_MESSAGE
            for answer in questAnswer[consts.ANSWERS_NODE]:
                print answer 
            
            inputAnswer = raw_input()
            if not inputAnswer == questAnswer[consts.EXPECT_ANSWER_NODE]:
                correctAnsweres = False
            
        print consts.ADDITIONAL_COMMENTS_MESSAGE
        inputAnswer = raw_input()
            
        answers.append(correctAnsweres)
        answers.append(inputAnswer) 
        return answers
            
