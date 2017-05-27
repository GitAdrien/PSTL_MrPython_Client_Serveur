'''
Created on 27 avr. 2017

@author: 3301202
'''

from py_compile import PyCompileError
from InterpreterServer.RunReport import RunReport
from InterpreterServer.Parser import Parser
class Compiler(object):
    '''
    Compilateur
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def compile(self, ast, report, compil_type, filename):
        try:
            code = compile(ast, filename, compil_type)
        except SyntaxError as err:
            report.add_compilation_error('error', "Compile error", err.lineno,
                                         err.offset, details=err.text)
            return None, report
        except ValueError as err:
            report.add_compilation_error('error', "Compile error",
                                         err.lineno, err.offset, details=err.text)
            return None, report
        return code, report
