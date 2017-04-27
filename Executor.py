'''
Created on 27 avr. 2017

@author: 3301202
'''

class Executor(object):
    '''
    classe d'execution
    '''


    def __init__(self, code,report):
        '''
        Constructor
        '''
        self.code=code
        self.report=report
     
    def execute(self):
        exec(self.code)
        
        #TODO: rapport
        return self.report
            