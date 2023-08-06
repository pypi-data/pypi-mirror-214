#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:33:17 2023

@author: usuario
"""

from FlyBaseDownloads.Downloads import Downloads 

class Organisms():
    
    def __init__(self, main_url):
        self.main_url = main_url
        self.org_url = 'species/organism_list_fb*.tsv.gz'
        self.header = 4
        
    
    def Species_list(self):
        
        url = self.main_url + self.org_url
        
        descargas = Downloads(url)
        
        return descargas.get(self.header)