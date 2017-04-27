# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:50:13 2017

@author: 3605386
"""
from multiprocessing import Process
import pipes
import sys
import json
class ExecProcess(Process):



    def __init__(self, prot):
        Process.__init__(self)
        self.prot = prot

    def run(self):

        self._compileExec(self.prot)
        
    def _computeOutExec(self,contenu, typ):
        error = False
        retcontent={}
        fst_stdout = sys.stdout
        fst_stderr = sys.stderr
        sys.stdout = open("out.txt", 'w+')#redirige la sortie standard
        sys.stderr = open("err.txt",'w+') #redirige la sortie d'erreur
    
    
        if(typ == "exec"):
            code = compile(contenu["source"],'', typ)
            exec(code)
        elif(typ == "eval"):
        
            code = compile(contenu["expr"],'', typ)
            data=eval(code)
            retcontent["data"]=data
        else:
            error = True
            #exec écrit dans la sortie standard

    

            sys.stdout.seek(0) #remise à zero des deux fichier afin de les lires
            sys.stderr.seek(0)
            out_str=sys.stdout.read() # calcul de la sortie
            err_str=sys.stderr.read()
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout=fst_stdout #remise à la normal de la sortie standard
            sys.stderr=fst_stderr
            if(len(err_str)>0):
                error=True
            retcontent["stdout"] = out_str
            retcontent["stderr"] = err_str
            a, b, tb = sys.exc_info()
    
        if(error==True):
            retcontent["report"] = tb
            return retcontent, error
        
    def _compileExec(self,prot):
        print("compileexec")
        while(True):
            error = False
            ret={}
            if(prot == {}):
                 #wait
                prot = self.pipe.recv()
            if(prot["content"]["mode"] == "full"): #Plus d'interet!!!! #TODO
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
                else:
                # aucun mode déféni
                    pass
            else:
                #TODO: mode student
                pass
            prot = {}    

class StudentInterpreter():
    def __init__(self, prot, pipe):
        self.t1 = ExecProcess(prot)
        self.t1.start()
        self.pipe=pipe
        
  
        
