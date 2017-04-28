# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:50:13 2017

@author: 3605386
"""
from multiprocessing import Process
import sys
import json
from RunReport import RunReport
from Parser import Parser
from CheckAST import CheckAST
from Compiler import Compiler
from Executor import Executor
class ExecProcess(Process):



    def __init__(self, prot,pipe,compiler,check_ast,parser,executor):
        Process.__init__(self)
        self.prot = prot
        self.compiler=compiler
        self.check_ast=check_ast
        self.parser=parser
        self.executor=executor
        self.pipe=pipe

    def run(self):

        self._compileExec(self.prot)
        
    def _computeOutExec(self,contenu, typ):
        error = False
        retcontent={}
        #fst_stdout = sys.stdout
        #fst_stderr = sys.stderr
        #sys.stdout = open("out.txt", 'w+')#redirige la sortie standard
        #sys.stderr = open("err.txt",'w+') #redirige la sortie d'erreur
    
    
        #if(typ == "exec"):
            #code = compile(contenu["source"],'', typ)
            #exec(code)
        #elif(typ == "eval"):
            
            #code = compile(contenu["expr"],'', typ)
            #data=eval(code)
            #retcontent["data"]=data
        #else:
            #error = True
            #exec écrit dans la sortie standard

    

            #sys.stdout.seek(0) #remise à zero des deux fichier afin de les lires
            #sys.stderr.seek(0)
            #out_str=sys.stdout.read() # calcul de la sortie
            #err_str=sys.stderr.read()
            #sys.stdout.close()
            #sys.stderr.close()
            #sys.stdout=fst_stdout #remise à la normal de la sortie standard
            #sys.stderr=fst_stderr
            #if(len(err_str)>0):
            #    error=True
        # retcontent["stdout"] = out_str
        #  retcontent["stderr"] = err_str
        #   a, b, tb = sys.exc_info()
    
        #if(error==True):
        #   retcontent["report"] = tb
        #   return retcontent, error
        report=RunReport()
        #Parser
        self.parser=Parser(contenu["source"],report,contenu["filename"])
        ast,report=self.parser.parse()
        if(ast==None):
            error=True
            retcontent["report"]=report
            return retcontent,error
        #check
        self.check_ast=CheckAST(ast,report)
        ast,report=self.check_ast.check()
        if(ast==None):
            error=True
            retcontent["report"]=report
            return retcontent,error
        #compilee
        self.compiler=Compiler(ast,report,contenu["mode"],contenu["filename"])
        code,report=self.compiler.compile()
        if(code==None):
            error=True
            retcontent["report"]=report
            return retcontent,error
        #executor
        self.executor=Executor(code,report)
        error,report,out_str,err_str=self.executor.execute()
        if(error):
            retcontent["report"]=report
            return error,retcontent
        retcontent["stderr"]=err_str
        retcontent["stdout"]=out_str
        return retcontent,error
            
         
        
        
    def compileExec(self,prot):
        print("compileexec")
        while(True):
            error = False
            ret={}
            if(prot == {}):
                #wait
                prot = self.pipe.recv()
                if(prot["msg_type"] == "exec"):
                    ret["content"], error = self._computeOutExec(prot["content"], "exec")
                    ret["session_id"] = prot["session_id"]+1
                    ret["msg_id"]=prot["msg_id"]+1
                    if(error == True):
                        ret["msg_type"] = "exec_error"
                    else:
                        ret["msg_type"] = "exec_success"
                    ret["protocol_version"] = prot["protocol_version"]
                    jsonRetour = json.dumps(ret)
                    #mettre sur le pipe : le truc dumpé
                    self.pipe.send(jsonRetour.encode("Utf8"))
                elif(prot["msg_type"] == "eval"):
                    #TODO : mode eval
                    print("_compileExec eval")
                    ret["content"], error = self._computeOutExec(prot["content"], "eval")
                    print("compute_eval")
                    ret["session_id"] = prot["session_id"]+1
                    ret["msg_id"]=prot["msg_id"]+1
                    if(error == True):
                        ret["msg_type"] = "eval_error"
                    else:
                        ret["msg_type"] = "eval_success"
                    ret["protocol_version"] = prot["protocol_version"]
                    jsonRetour = json.dumps(ret)
                    self.pipe.send(jsonRetour.encode("Utf8"))
                    print("json envoyé")
                 

class StudentInterpreter():
    def __init__(self, prot, pipe,compiler,check_ast,parser,executor):
        self.pipe=pipe
        self.compiler=compiler
        self.check_ast=check_ast
        self.executor=executor
        self.parser=parser
        self.t1 = ExecProcess(prot,pipe,compiler,check_ast,parser,executor)
        self.t1.start()
  
        
