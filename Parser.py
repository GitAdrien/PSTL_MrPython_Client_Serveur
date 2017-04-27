# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 11:54:59 2017

@author: 3605386
"""

class Parser():
    #va parser
    def __init__(source, rapport):
        self.source = source
        self.rapport = rapport
    def parse():
        res = ast.parse(self.source)
        #TODO : créer le rapport d'erreur
        return res, rapport
         