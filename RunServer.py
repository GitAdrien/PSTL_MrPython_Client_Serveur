# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:43:45 2017

@author: 3605386
"""
class RunServer():
    def __init__(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 5001
        buffer_size = 4096
        serverSocket.bind((host, port))
        serverSocket.listen(10)
        self.connexion, addresse = serverSocket.accept()
        msgServeur ="Vous êtes connecté au serveur"
        connexion.send(msgServeur.encode("Utf8"))
        print("Listening on %s:%s..." % (host, str(port)))
    def serverLoop(self):
    
        server_con, interpreter_conn = Pipe()
        interpreter = StudentInterpreter({}, interpreter_conn)

        while True:
            print("serverloop")
            data = self.connexion.recv(buffer_size)
            if(not data):
                self.connexion.close()
                return
            sdata = data.decode("Utf8")
            print("sdata=",sdata)
            test = json.loads(sdata)
            
            if(test["msg_type"]=="interrupt"):

                if(interpreter.t1.is_alive()):
                    interptrer.t1.terminate()
                    retour={}
                    retour["msg_type"]="interrupt_success"
                    retour["session_id"]=test["session_id"]
                    retour["msg_id"]=test["msg_id"]+1
                    retour["protocol_version"]=test ["protocol_version"]
                    retour["content"]={}
                    jsonRetour = json.dumps(retour)
                    self.connexion.send(jsonRetour.encode("Utf8"))
                else:
                    retour={}
                    retour["msg_type"]="interrupt_fail"
                    retour["session_id"]=test["session_id"]
                    retour["msg_id"]=test["msg_id"]+1
                    retour["protocol_version"]=test["protocol_version"]
                    retour["content"]={}
                    jsonRetour = json.dumps(retour)
                    self.connexion.send(jsonRetour.encode("Utf8"))
            elif(test["msg_type"]=="exec"):
                #exec_proc=Process(target=_compileExec,args=(test))
                #Lancer une instance d'un interpreter
                interpreter.t1.terminate()
                interpreter = StudentInterpreter(prot, t)
            elif(test["msg_type"] == "eval"):
                server_con.send(prot)
                

if __name__ == "__main__":
    server = RunServer()
    server.serverLoop()
