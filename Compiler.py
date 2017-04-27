'''
Created on 27 avr. 2017

@author: 3301202
'''

class Compiler(object):
    '''
    Compilateur
    '''


    def __init__(self, ast,report,compil_type,filename):
        '''
        Constructor
        '''
        self.ast=ast
        self.report=report
        self.compil_type=compil_type
        self.filename=filename
    
    def compile(self):
        if(self.compil_type == "exec"):
            code = compile(self.ast,self.filename, self.compil_type)
            #TODO: ajouter les erreurs
            return code,self.report
        elif(self.compil_type == "eval"):
            #TODO: ajouter les erreurs
            code = compile(self.ast,self.filename, self.compil_type)
            return code