import socket
import json
import sys
import py_compile

def _compileExec(execOrEval, filename, source, mode):
    error = False
    try :
        if(mode == "full"):
            if(execOrEval == "exec"):
                mon_fichier = open(filename, "r")
                contenu = mon_fichier.read()
                mon_fichier.close()
                sys.stdout = open(source, 'w')
                code = compile(contenu,source, 'exec')
                exec(code)
            else:
                #TODO : mode eval
        else:
            #TODO: mode student
    except py_compile.pyCompileError:
        error = True
    return source, error
    
    
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 5000

buffer_size = 4096

serverSocket.bind((host, port))
serverSocket.listen(10)
connexion, addresse = serverSocket.accept()
msgServeur ="Vous êtes connecté au serveur"
connexion.send(msgServeur.encode("Utf8"))
print("Listening on %s:%s..." % (host, str(port)))
data = connexion.recv(buffer_size)
retour ={}
sdata = data.decode("Utf8")
test = json.loads(sdata)
execOrEval = test["execOrEval"]
filename = test["filename"]
source = test["source"]
mode = test["mode"]
retour["output"] , retour["status"] = _compileExec(execOrEval, filename, source, mode)
jsonRetour = json.dumps(retour)
connexion.send(jsonRetour.encode("Utf8"))
connexion.close()

