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
from Reporter import Reporter

class StudentExecProcess(Process):



    def __init__(self, prot,pipe,compiler,check_ast,parser,executor):
        Process.__init__(self)
        self.prot = prot
        self.compiler=compiler
        self.check_ast=check_ast
        self.parser=parser
        self.executor=executor
        self.pipe=pipe
        

    def run(self):

        self.compileExec(self.prot)
        
    def _computeOutExec(self,contenu, typ):
        if(typ == "eval"):
            error = False
            retcontent={}
            report = RunReport()
            reporter = Reporter()
            code,report=self.compiler.compile(contenu["expr"],report,typ,contenu["filename"])
            if(code==None):
                error=True
                retcontent["report"]=reporter.compute_report(report)
                return retcontent,error
            data,report,out_str,err_str=self.executor.evaluate(code,report)
            print(data)
            if(data==None):
                retcontent["report"]=reporter.compute_report(report)
                return retcontent,error
            retcontent["stderr"]=err_str
            retcontent["stdout"]=out_str
            retcontent["data"]=data
            retcontent["report"]=reporter.compute_report(report)
            return retcontent,error
        elif(typ == "exec"):
            error = False
            retcontent={}
            report = RunReport()
            reporter = Reporter()
            #Parser
            ast,report = self.parser.parse(contenu["source"],report,contenu["filename"])
            if(ast==None):
                error = True
                retcontent["report"]=reporter.compute_report(report)
                return retcontent,error
            #check
            ast,report=self.check_ast.check(ast,report)
            if(ast==None):
                error=True
                retcontent["report"]=reporter.compute_report(report)
                return retcontent,error
            #compilee
        
            code,report=self.compiler.compile(ast,report,typ,contenu["filename"])
            if(code==None):
                error=True
                retcontent["report"]=reporter.compute_report(report)
                return retcontent,error
            #executor
            
            error,report,out_str,err_str=self.executor.execute(code,report)
            print(error)
            if(error):
                retcontent["report"]=reporter.compute_report(report)
                return retcontent,error
            retcontent["stderr"]=err_str
            retcontent["stdout"]=out_str
            retcontent["report"]=reporter.compute_report(report)
            return retcontent,error
            
         
        
        
    def compileExec(self,prot):
        print("compileexec")
        while(True):
            error = False
            ret={}
            if(prot=={}):
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
            prot={}
                 

class StudentInterpreter():
    def __init__(self, prot, pipe,compiler,check_ast,parser,executor):
        self.pipe=pipe
        self.compiler=compiler
        self.check_ast=check_ast
        self.executor=executor
        self.parser=parser
        self.t1 = StudentExecProcess(prot,pipe,compiler,check_ast,parser,executor)
        self.t1.start()
  
        
