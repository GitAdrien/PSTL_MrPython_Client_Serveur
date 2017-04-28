# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:43:45 2017

@author: 3605386
"""
import socket
import logging
from StudentInterpreter import StudentInterpreter
import json
from multiprocessing import Pipe, Process
class RunServer():
    def __init__(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        self.buffer_size = 4096
        serverSocket.bind((host, 0)) #Prend le premier port disponible
        port  = sock.getsockname()[1] # numero du port
        config_file=open("config.txt","w")
        config_file.write(port)
        serverSocket.listen(10)
        self.connexion, addresse = serverSocket.accept()
        msgServeur ="Vous êtes connecté au serveur"
        self.connexion.send(msgServeur.encode("Utf8"))
        Logger.info("Listening on %s:%s..." % (host, str(port)))
    def waitResult(self,pipe):
        pass
        res=pipe.recv(self.buffer_size)
        self.connexion.send(res)
    def serverLoop(self):
    
        server_con, interpreter_conn = Pipe()
        interpreter = StudentInterpreter({}, interpreter_conn)

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
                interpreter = StudentInterpreter(prot, interpreter_conn)
                waitproc=Process(target=self.wait_result)
                waitproc.start()
            elif(prot["msg_type"] == "eval"):
                server_con.send(prot)
            else:
                Logger.error("msg_type error")
                

if __name__ == "__main__":
    server = RunServer()
    server.serverLoop()
