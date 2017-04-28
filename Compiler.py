'''
Created on 27 avr. 2017

@author: 3301202
'''

from py_compile import PyCompileError
from RunReport import RunReport
from Parser import Parser
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
        except SyntaxError as err:
            self.report.add_compilation_error('error', "Compile error", err.lineno, err.offset, details=err.text)
            print("compileerror")
            print(self.report.compilation_errors[0].error_details())
            return None,self.report
        except ValueError as err:
            self.report.add_compilation_error('error', "Compile error", err.lineno, err.offset, details=err.text)
            print("compileerror")
            print(self.report.compilation_errors[0].error_details())
            return None,self.report
        #TODO: ajouter les erreurs
        return code,self.report

#f=open("test.txt")
#source=f.read()
#f.close()  
#report=RunReport() 

#p=Parser(source,report,"test.txt")
#ast,report=p.parse()
#c=Compiler(ast,report,"exec","test.txt")
#c.compile()
