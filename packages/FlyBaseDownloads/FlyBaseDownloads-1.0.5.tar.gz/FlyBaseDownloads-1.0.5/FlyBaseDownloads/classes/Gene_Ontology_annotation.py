#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:25:55 2023

@author: usuario
"""

from FlyBaseDownloads.Downloads import Downloads 
import pandas as pd


class Gene_Ontology_annotation():
    
    def __init__(self, main_url):
    
        self.main_url = main_url
        self.go_url = 'go/gene_association.fb.gz'
        self.header = 5
        self.df_columns = ['DB', 'DB_Object_ID', 'DB_Object_Symbol',
                           'Qualifier', 'GO ID', 'DB:Reference',
                           'Evidence', 'With (or) From', 'Aspect',
                           'DB_Object_Name', 'DB_Object_Synonym', 'DB_Object_Type',
                           'taxon', 'Date', 'Assigned_by']
        
    def get(self):
        
        url = self.main_url + self.go_url
        descargas = Downloads(url)
        
        archivos = []
        
        archivos = descargas.download_file()
        
        if len(archivos) > 0:
            df = descargas.open_file_tsv(archivos[0], self.header)
            df = df.iloc[:, :-2]
            df_ = pd.DataFrame(df.columns).T
            df_.columns = self.df_columns
            df.columns = self.df_columns
            return pd.concat([df_, df])