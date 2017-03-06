
Protocole Client Serveur
===================
Evaluation d'une expression
---------------------------------------
###MrPython

	{"cmd": "evaluate",
	 "filename":"nom du fichier",
	 "source":"code source",
	 "mode":"student"}
ou

	{"cmd": "evaluate",
	 "filename":"nom du fichier",
	 "source":"code source",
	 "mode":"full"}
###RunServer

	 {"status":"success",
	  "output":"rapport d'évaluation"}
	  ou

	{"status":"failure",
	 "output":"rapport d'évaluation"}
	

##Exécution d'un programme
###MrPython

	{"cmd": "execute",
	 "filename":"nom du fichier",
	 "source":"code source",
	 "mode":"student"}
ou

	{"cmd": "execute",
	 "filename":"nom du fichier",
	 "source":"code source",
	 "mode":"full"}
###RunServer

	{"status":"success",
	  "output":"rapport d'exécution"}
ou

	{"status":"failure",
	 "output":"rapport d'exécution"}

##Interruption de l'éxécution
###MrPython
	{"cmd": "interrupt",
	 "filename":"nom du fichier",
	 "source":"code source",
	 "mode":"student"}
ou

	{"cmd": "interrupt",
	 "filename":"nom du fichier",
	 "source":"code source",
	 "mode":"full"}
###RunServer

	{"status":"success",
	  "output":"rapport d'exécution"}
ou

	{"status":"failure",
	 "output":"rapport d'exécution"}

##Interface Graphique
###MrPython
	{"cmd": "graphics",
	 "filename":"nom du fichier",
	 "source":"code source",
	 "mode":"student"}
###RunServer
	{"status": "success"
	 "output":"parametres de création de la figure"}
ou

	{"status":"failure",
	 "output":"rapport d'exécution"}

##Input
###MrPython
	{"cmd": "input",
	 "filename":"nom du fichier",
	 "source":"code source",
	 "mode":"student"}
ou

	{"cmd": "input",
	 "filename":"nom du fichier",
	 "source":"code source",
	 "mode":"full"}
###RunServer

	{"cmd":"inputValues"}
