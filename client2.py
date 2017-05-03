# Définition d'un client réseau rudimentaire
# Ce client dialogue avec un serveur ad hoc

#Test avec un exec puis un eval
import uuid
import socket, sys
import json
import time
from threading import Thread
HOST = socket.gethostname()
mon_fichier_config = open("config.txt","r")
PORT = int(mon_fichier_config.read())

# 1) création du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# 2) envoi d'une requête de connexion au serveur :
try:
    mySocket.connect((HOST, PORT))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()
print("Connexion établie avec le serveur.")

class PrintThread(Thread):

    """Thread chargé simplement d'éxécuter un thread."""

    def __init__(self):
        Thread.__init__(self)
        

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        while True:
            msgServeur=mySocket.recv(1024).decode("Utf8")
            if(not msgServeur):
                mySocket.close()
                return
            prot=json.loads(msgServeur)
            print("protocole reçu")
            print(prot)
            
# 3) Dialogue avec le serveur :
msgServeur = mySocket.recv(1024).decode("Utf8")
print("msgserveur")
t=PrintThread()
t.start()
mon_fichier=open("test.txt","r")
contenu = mon_fichier.read()
mon_fichier.close()

id_exec = uuid.uuid1().int
docJson ={ "session_id": id_exec, "msg_id": 1, "msg_type" : "exec", "protocol_version": 0.1, "content" : {"source" : contenu, "mode": "full","filename":"loop.txt" }}
##docJson = {"execOrEval" : "exec", "filename" : "test.txt", "source" : "testReturn.txt", "mode" : "full"}
docJson2 = json.dumps(docJson)
print("S>", msgServeur)
msgClient = docJson2
mySocket.send(msgClient.encode("Utf8"))
mon_fichier2=open("test2.txt","r")
contenu2 = mon_fichier2.read()
mon_fichier2.close()
time.sleep(1)
docJson3 ={ "session_id": uuid.uuid1().int, "msg_id": 1, "msg_type" : "interrupt", "protocol_version": 0.1, "content" : {"expr" : contenu2, "mode": "full","filename":"test2.txt" }}
#docJson3 ={ "session_id": 2, "msg_id": 1, "msg_type" : "eval", "protocol_version": 0.1, "content" : {"expr" : contenu2, "mode": "full","filename":"test2.txt" }}
docJson4 = json.dumps(docJson3)
mySocket.send(docJson4.encode("Utf8"))



t.join()
# 4) Fermeture de la connexion :
print("Connexion interrompue.")

