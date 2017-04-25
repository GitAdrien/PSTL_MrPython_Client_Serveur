# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:23:26 2017

@author: 3301202
"""

import socket
import json
import sys
import py_compile

from threading import Thread
from multiprocessing import Process


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 5001

buffer_size = 4096

serverSocket.bind((host, port))
serverSocket.listen(10)
connexion, addresse = serverSocket.accept()
msgServeur ="Vous êtes connecté au serveur"
connexion.send(msgServeur.encode("Utf8"))
print("Listening on %s:%s..." % (host, str(port)))

def _computeOutExec(contenu, typ):
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
def _compileExec(prot):
    print("compileexec")
    error = False
    ret={}
    if(prot["content"]["mode"] == "full"):
        if(prot["msg_type"] == "exec"):
            ret["content"], error = _computeOutExec(prot["content"], "exec")
            ret["session_id"] = prot["session_id"]+1
            ret["msg_id"]=prot["msg_id"]+1
            if(error == True):
                ret["msg_type"] = "exec_error"
            else:
                ret["msg_type"] = "exec_success"
            ret["protocol_version"] = prot["protocol_version"]
            jsonRetour = json.dumps(ret)
            connexion.send(jsonRetour.encode("Utf8"))
        elif(prot["msg_type"] == "eval"):
            #TODO : mode eval
            print("_compileExec eval")
            ret["content"], error = _computeOutExec(prot["content"], "eval")
            print("compute_eval")
            ret["session_id"] = prot["session_id"]+1
            ret["msg_id"]=prot["msg_id"]+1
            if(error == True):
                ret["msg_type"] = "eval_error"
            else:
                ret["msg_type"] = "eval_success"
            ret["protocol_version"] = prot["protocol_version"]
            jsonRetour = json.dumps(ret)
            connexion.send(jsonRetour.encode("Utf8"))
            print("json envoyé")
            pass
        else:
            # aucun mode déféni
            pass
    else:
        #TODO: mode student
        pass



class ExecProcess(Process):



    def __init__(self, prot):
        Process.__init__(self)
        self.prot = prot

    def run(self):

        _compileExec(self.prot)


#exec_proc=Process(target=_compileExec,args=({}))
#mon_fichier = open("loop.txt", "r")
#contenu = mon_fichier.read()
#mon_fichier.close()
#docJson ={ "session_id": 1, "msg_id": 1, "msg_type" : "exec", "protocol_version": 0.1, "content" : {"source" : contenu, "mode": "full" }}

t1=ExecProcess({})
#t1.start()

def serverLoop(t1):
    while True:
        print("serverloop")
        data=connexion.recv(buffer_size)
        if(not data):
            connexion.close()
            return
        sdata = data.decode("Utf8")
        print("sdata=",sdata)
        test = json.loads(sdata)
        
        if(test["msg_type"]=="interrupt"):

            if(t1.is_alive()):
                t1.terminate()
                retour={}
                retour["msg_type"]="interrupt_success"
                retour["session_id"]=test["session_id"]
                retour["msg_id"]=test["msg_id"]+1
                retour["protocol_version"]=test ["protocol_version"]
                retour["content"]={}
                jsonRetour = json.dumps(retour)
                connexion.send(jsonRetour.encode("Utf8"))
            else:
                retour={}
                retour["msg_type"]="interrupt_fail"
                retour["session_id"]=test["session_id"]
                retour["msg_id"]=test["msg_id"]+1
                retour["protocol_version"]=test["protocol_version"]
                retour["content"]={}
                jsonRetour = json.dumps(retour)
                connexion.send(jsonRetour.encode("Utf8"))
        elif(test["msg_type"]=="exec" or test["msg_type"]=="eval" ):
            #exec_proc=Process(target=_compileExec,args=(test))
            t1=ExecProcess(test)
            t1.start()
            
        

serverLoop(t1)





#connexion.close()
