# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:43:45 2017

@author: 3605386
"""
import socket
from logging import Logger
from StudentInterpreter import StudentInterpreter
import json
from multiprocessing import Pipe, Process
from Parser import Parser
from Compiler import Compiler
from CheckAST import CheckAST
from Executor import Executor
class RunServer():
    def __init__(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        self.buffer_size = 4096
        serverSocket.bind((host, 0)) #Prend le premier port disponible
        port  = serverSocket.getsockname()[1] # numero du port
        print(port)
        config_file=open("config.txt","w")
        config_file.write(str(port))
        config_file.flush()
        print("ecrit")
        serverSocket.listen(10)
        print("ecoute")
        self.connexion, addresse = serverSocket.accept()
        print("accept")
        msgServeur ="Vous êtes connecté au serveur"
        
        self.connexion.send(msgServeur.encode("Utf8"))
        #Logger.info("Listening on %s:%s..." % (host, str(port)))
    def waitResult(self,pipe):
        pass
        res=pipe.recv()
        self.connexion.send(res)
        
    def serverLoop(self):
        
        server_con, interpreter_conn = Pipe()
        parser=Parser()
        compiler=Compiler()
        check_ast=CheckAST()
        executor=Executor()
        interpreter = StudentInterpreter({}, interpreter_conn,compiler,check_ast,parser,executor)

        while True:
            data = self.connexion.recv(self.buffer_size)
            if(not data):
                self.connexion.close()
                return
            sdata = data.decode("Utf8")
            prot = json.loads(sdata)
            
            if(prot["msg_type"]=="interrupt"):

                if(interpreter.t1.is_alive()):
                    interpreter.t1.terminate()
                    retour={}
                    retour["msg_type"]="interrupt_success"
                    retour["session_id"]=prot["session_id"]
                    retour["msg_id"]=prot["msg_id"]+1
                    retour["protocol_version"]=prot ["protocol_version"]
                    retour["content"]={}
                    jsonRetour = json.dumps(retour)
                    self.connexion.send(jsonRetour.encode("Utf8"))
                else:
                    retour={}
                    retour["msg_type"]="interrupt_fail"
                    retour["session_id"]=prot["session_id"]
                    retour["msg_id"]=prot["msg_id"]+1
                    retour["protocol_version"]=prot["protocol_version"]
                    retour["content"]={}
                    jsonRetour = json.dumps(retour)
                    self.connexion.send(jsonRetour.encode("Utf8"))
            elif(prot["msg_type"]=="exec"):
               
                

                interpreter.t1.terminate()
                interpreter = StudentInterpreter(prot, interpreter_conn,compiler,check_ast,parser,executor)
                waitproc=Process(target=self.waitResult,args=(server_con,))
                waitproc.start()
            elif(prot["msg_type"] == "eval"):
                server_con.send(prot)
            else:
                Logger.error("msg_type error")
            
                

if __name__ == "__main__":
    server = RunServer()
    server.serverLoop()
