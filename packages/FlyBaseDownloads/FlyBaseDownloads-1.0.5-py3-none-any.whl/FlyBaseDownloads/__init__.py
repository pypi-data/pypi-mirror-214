#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 17:35:44 2023

@author: javiera.quiroz
"""

from FlyBaseDownloads.FBD import FBD 

db = FBD()

#Synonyms
Synonyms = db.Synonyms

#Genes
Genes = db.Genes

#GO
GOAnn = db.GOAnn

#Gene_groups
Gene_groups = db.Gene_groups

#Alleles_Stocks
Alleles_Stocks = db.Alleles_Stocks

#Homologs
Homologs = db.Homologs

#Human_disease
Human_disease = db.Human_disease

#Ontology
Ontology_Terms = db.Ontology_Terms

#Organisms
Organisms = db.Organisms

#Insertions
Insertions = db.Insertions

#Clones
Clones = db.Clones

#References
References = db.References