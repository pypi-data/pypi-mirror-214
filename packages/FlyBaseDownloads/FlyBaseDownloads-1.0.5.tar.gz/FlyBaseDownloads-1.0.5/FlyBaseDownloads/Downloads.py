#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:04:19 2023

@author: usuario
"""


import pandas as pd
import fnmatch
import gzip
from ftplib import FTP
import re
import csv
import obonet
import json
import os


class Downloads():
    
    def __init__(self, url):
        
        self.url = url
        
    def download_file(self):
        
        url = self.url
        
        ftp = FTP(url.split('/')[2])
        ftp.login()
        ruta_directorio = '/'.join(url.split('/')[3:-1])


        ftp.cwd(ruta_directorio)

        archivos_remotos = ftp.nlst()

        archivos_filtrados = list(fnmatch.filter(archivos_remotos, url.split('/')[-1]))

        archivos = []
        for archivo in archivos_filtrados:
            ruta_archivo = '../' + archivo
            if not os.path.exists(archivo):
                with open(ruta_archivo, 'wb') as archivo_local:
                    ftp.retrbinary('RETR ' + archivo, archivo_local.write)
    
                    archivos.append(archivo)
            else:
                archivos.append(archivo)

        ftp.quit()
        if len(archivos) > 0:
            return archivos
        else:
            print('Failed to download the file')
            return []
        
    
    
    
    def open_file_tsv(self, ruta_archivo, header):
        a = []

        if re.search(r'gz', ruta_archivo):
            
            try: 
                with gzip.open('../' + ruta_archivo, 'rt') as archivo:
                   df = pd.read_csv(archivo, sep='\t', header=header)
                   a.append(df)
                return (a[0])
            
            except: 
                try:
                    with gzip.open('../' + ruta_archivo, 'rt') as archivo:
                        df = csv.reader(archivo, delimiter='\t')
                        a.append(pd.DataFrame(df))
                
                    df = a[0]
                    columns = df.iloc[header, :].tolist()
        
                    # Elimina la fila del encabezado del DataFrame
                    df = df.iloc[header + 1:, :]
                    
                    # Asigna los nuevos nombres de columna al DataFrame
                    df.columns = columns
                    df = df.dropna(axis='columns')
                  
  
                    return (df)
                except:
                    print('Failed to download the file') 
                    
    def open_file_json(self, ruta_archivo):
        
        a = []

        if re.search(r'gz', ruta_archivo):
            
            try: 
                with gzip.open('../' + ruta_archivo, 'rt') as archivo:
                    d = json.load(archivo)
                    d_ = d['data']
                    datos = pd.DataFrame(d_)
                    a.append(datos)
                   
            except:
                try:
                    with gzip.open('../' + ruta_archivo, 'rt') as archivo:
                        return json.load(archivo)
                except:
                    print('Failed to download the file') 
            
        
        return a[0]
                    
    def open_obo(self, ruta_archivo):
    
        a = []
        
        try:
            if re.search(r'gz', ruta_archivo):
                with gzip.open('../' + ruta_archivo, 'rt') as archivo:
                   if re.search(r'obo', ruta_archivo):
                       
                      graph = obonet.read_obo(archivo)
                      
                      a.append(graph)

            return a[0]
        
        except:
            print('Failed to download the file') 
        
    
    def get(self, header = None):
        
        archivos = []
        
        try:
            archivos = self.download_file()
        except:
            print('Failed to download the file') 
        patron = r"##?\s?\w+"
        
        def df_r(df):
            if re.search(r"FB\w{9}", df.columns[0]):
                df_columns = pd.DataFrame(df.columns).T

                df.columns = range(len(df.columns))
                
                # Unir la fila de columnas con el resto del DataFrame
                df = pd.concat([df_columns, df], ignore_index=True, axis = 0)
            
            if re.search(patron, df.iloc[-1,0]):
                df = df.iloc[:-1, :]
            
            return df
        
        
        if len(archivos) > 0:
            if re.search('.obo', self.url):
                return self.open_obo(archivos[0])
            elif re.search('.json', self.url):
                try:
                    return df_r(self.open_file_json(archivos[0]))
                    
                except:
                    try:
                        df = self.open_file_json(archivos[0])
                        df = pd.concat([df.drop(['driver'], axis=1), df['driver'].apply(pd.Series)], axis=1)

                        # Reemplazar los valores None por NaN
                        df = df.replace({None: pd.NA})
                        return df_r(df)
                    except:
                        return self.open_file_json(archivos[0])
                    
            else:
                return df_r(self.open_file_tsv(archivos[0], header))
        
    
