'''
Created on 27 avr. 2017

@author: 3301202
'''

class CheckAST(object):
    '''
    Vérifications de l'AST pour le mode student
    '''


    def __init__(self, ast,report):
        '''
        Constructor
        '''
        self.ast=ast
        self.report=report
    
    def check(self):
        return self.ast,self.report
        