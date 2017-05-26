'''
Created on 27 avr. 2017

@author: 3301202
'''
import traceback
import sys
from InterpreterServer.RunReport import RunReport
from InterpreterServer.Parser import Parser
from InterpreterServer.Compiler import Compiler
from InterpreterServer.translate import tr

class Executor(object):
    '''
    classe d'execution
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.locals = {}

    def execute(self, code, report):
        '''
        Exécute le programme
        Renvoie un booléen indiquant une erreur ainsi que les valeurs de stdin et stdout
        '''
        fst_stdout = sys.stdout
        fst_stderr = sys.stderr
        sys.stdout = open("out.txt", 'w+')#redirige la sortie standard
        sys.stderr = open("err.txt", 'w+') #redirige la sortie d'erreur
        try:
            exec(code, self.locals, self.locals)
        except TypeError as err:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = fst_stdout #remise à la normal de la sortie standard
            sys.stderr = fst_stderr
            a, b, tb = sys.exc_info()
            filename, lineno, file_type, line = traceback.extract_tb(tb)[-1]
            err_str = self._extract_error_details(err)
            report.add_execution_error('error', tr("Type error"), lineno, details=str(err))
            return (True, None, None)
        except NameError as err:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = fst_stdout #remise à la normal de la sortie standard
            sys.stderr = fst_stderr
            a, b, tb = sys.exc_info() # Get the traceback object
            # Extract the information for the traceback corresponding to the error
            # inside the source code : [0] refers to the result = exec(code)
            # traceback, [1] refers to the last error inside code
            filename, lineno, file_type, line = traceback.extract_tb(tb)[-1]
            err_str = self._extract_error_details(err)
            report.add_execution_error('error', tr("Name error (unitialized variable?)"), lineno, details=err_str)
            return (True, report, None, None)
        except ZeroDivisionError:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = fst_stdout #remise à la normal de la sortie standard
            sys.stderr = fst_stderr
            a, b, tb = sys.exc_info()
            filename, lineno, file_type, line = traceback.extract_tb(tb)[-1]
            report.add_execution_error('error', tr("Division by zero"), lineno)
            return (True, report, None, None)
        except AssertionError:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = fst_stdout #remise à la normal de la sortie standard
            sys.stderr = fst_stderr
            a, b, tb = sys.exc_info()
            lineno = None
            traceb = traceback.extract_tb(tb)
            if len(traceb) > 1:
                filename, lineno, file_type, line = traceb[-1]
            report.add_execution_error('error', tr("Assertion error (failed test?)"), lineno)
            return (True, report, None, None)
        except Exception as err:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = fst_stdout #remise à la normal de la sortie standard
            sys.stderr = fst_stderr
            a, b, tb = sys.exc_info() # Get the traceback object
            # Extract the information for the traceback corresponding to the error
            # inside the source code : [0] refers to the result = exec(code)
            # traceback, [1] refers to the last error inside code
            lineno = None
            traceb = traceback.extract_tb(tb)
            if len(traceb) > 1:
                filename, lineno, file_type, line = traceb[-1]
            report.add_execution_error('error', a.__name__, lineno, details=str(err))
            return (True, report, None, None)
        sys.stdout.seek(0) #remise à zero des deux fichier afin de les lires
        sys.stderr.seek(0)
        out_string = sys.stdout.read() # calcul de la sortie
        err_string = sys.stderr.read()
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = fst_stdout #remise à la normal de la sortie standard
        sys.stderr = fst_stderr
        return(False, report, out_string, err_string)

    def _extract_error_details(self, err):
        err_str = err.args[0]
        start = err_str.find("'") + 1
        end = err_str.find("'", start + 1)
        details = err_str[start:end]
        return details

    def evaluate(self, code, report):
        '''
        Evalue le programme
        Renvoie les valeurs de stdin et stdout et la valeur de l'expression
        '''
        fst_stdout = sys.stdout
        fst_stderr = sys.stderr
        sys.stdout = open("out.txt", 'w+')#redirige la sortie standard
        sys.stderr = open("err.txt", 'w+') #redirige la sortie d'erreur
        try:
            data=eval(code, self.locals, self.locals)            
        except TypeError as err:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = fst_stdout #remise à la normal de la sortie standard
            sys.stderr = fst_stderr
            a, b, tb = sys.exc_info()
            filename, lineno, file_type, line = traceback.extract_tb(tb)[-1]
            err_str = self._extract_error_details(err)
            report.add_execution_error('error', tr("Type error"), lineno, details=str(err))
            return (None, report, None, None, True)
        except NameError as err:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = fst_stdout #remise à la normal de la sortie standard
            sys.stderr = fst_stderr
            a, b, tb = sys.exc_info() # Get the traceback object
            # Extract the information for the traceback corresponding to the error
            # inside the source code : [0] refers to the result = exec(code)
            # traceback, [1] refers to the last error inside code
            filename, lineno, file_type, line = traceback.extract_tb(tb)[-1]
            err_str = self._extract_error_details(err)
            report.add_execution_error('error', tr("Name error (unitialized variable?)"), lineno, details=err_str)
            return (None, report, None, None, True)
        except ZeroDivisionError:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = fst_stdout #remise à la normal de la sortie standard
            sys.stderr = fst_stderr
            a, b, tb = sys.exc_info()
            filename, lineno, file_type, line = traceback.extract_tb(tb)[-1]
            report.add_execution_error('error', tr("Division by zero"), lineno)
            return (None, report, None, None, True)
        except AssertionError:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = fst_stdout #remise à la normal de la sortie standard
            sys.stderr = fst_stderr
            a, b, tb = sys.exc_info()
            lineno = None
            traceb = traceback.extract_tb(tb)
            if len(traceb) > 1:
                filename, lineno, file_type, line = traceb[-1]
            report.add_execution_error('error', tr("Assertion error (failed test?)"), lineno)
            return (None, report, None, None, True)
        except Exception as err:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = fst_stdout #remise à la normal de la sortie standard
            sys.stderr = fst_stderr
            a, b, tb = sys.exc_info() # Get the traceback object
            # Extract the information for the traceback corresponding to the error
            # inside the source code : [0] refers to the result = exec(code)
            # traceback, [1] refers to the last error inside code
            lineno = None
            traceb = traceback.extract_tb(tb)
            if len(traceb) > 1:
                filename, lineno, file_type, line = traceb[-1]
            report.add_execution_error('error', a.__name__, lineno, details=str(err))
            return (None, report, None, None, True)
        sys.stdout.seek(0) #remise à zero des deux fichier afin de les lires
        sys.stderr.seek(0)
        out_string = sys.stdout.read() # calcul de la sortie
        err_string = sys.stderr.read()
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = fst_stdout #remise à la normal de la sortie standard
        sys.stderr = fst_stderr
        return(data, report, out_string, err_string, False)
