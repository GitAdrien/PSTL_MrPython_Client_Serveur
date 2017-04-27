# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 11:54:59 2017

@author: 3605386
"""
import ast
from RunReport import RunReport
class Parser():
    #va parser
    def __init__(self,source, rapport):
        self.source = source
        self.rapport = rapport
    def parse(self):
        res = ast.parse(self.source)
        #TODO : créer le rapport d'erreur
        return res, self.rapport
         
#f=open("test.txt")
#str=f.read()
#f.close()  
#r=RunReport()
       
#p=Parser(str,r)
#res,r=p.parse()
#print(res)        