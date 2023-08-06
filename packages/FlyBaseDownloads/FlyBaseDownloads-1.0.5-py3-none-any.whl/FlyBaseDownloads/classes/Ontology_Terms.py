#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:32:48 2023

@author: usuario
"""

from FlyBaseDownloads.Downloads import Downloads 


class Ontology_Terms():
    
    def __init__(self, main_url):
    
        self.main_url = main_url
        self.go_url = 'ontologies/'
        self.header = None
        
    def get(self):
        
        url = self.main_url + self.go_url + self.un_url
        descargas = Downloads(url)
        
        return descargas.get(self.header)
        
    def Fly_anatomy(self):
        self.un_url = 'fly_anatomy.obo.gz'
        return self.get()
    
    def Fly_development(self):
        self.un_url = 'fly_development.obo.gz'
        return self.get()
    
    def Flybase_controlled_vocabulary(self):
        self.un_url = 'flybase_controlled_vocabulary.obo.gz'
        return self.get()
    
    def Flybase_stock_vocabulary(self):
        self.un_url = 'flybase_stock_vocabulary.obo.gz'
        return self.get()
    
    def GO_ontology(self):
        self.un_url = 'go-basic.obo.gz'
        return self.get()
    
    def Image_ontology(self):
        self.un_url = 'image.obo.gz'
        return self.get()
    
    def DO_ontology(self):
        self.un_url = 'so-simple.obo.gz'
        return self.get()