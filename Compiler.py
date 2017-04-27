'''
Created on 27 avr. 2017

@author: 3301202
'''

from py_compile import PyCompileError
from RunReport import RunReport
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
        try:
            code = compile(self.ast,self.filename, self.compil_type)
        except PyCompileError as err:
            self.report.add_compilation_error('error', "Compile error", err.lineno, err.offset, details=err.text)
            return None,self.report
        #TODO: ajouter les erreurs
        return code,self.report

f=open("test.txt")
source=f.read()
f.close()  
r=RunReport() 

c=Compiler()    