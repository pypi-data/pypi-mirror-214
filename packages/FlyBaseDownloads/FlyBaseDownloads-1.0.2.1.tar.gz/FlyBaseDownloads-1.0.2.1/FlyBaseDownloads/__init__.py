#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 17:35:44 2023

@author: javiera.quiroz
"""

from FlyBaseDownloads.FBD import FBD 

db = FBD()

#Synonyms
Synonyms = db.Synonyms(db)

#Genes
Genes = db.Genes(db)

#GO
Gene_Ontology_annotation = db.Gene_Ontology_annotation(db)

#Gene_groups
Gene_groups = db.Gene_groups(db)

#Alleles_Stocks
Alleles_Stocks = db.Alleles_Stocks(db)

#Homologs
Homologs = db.Homologs(db)

#Human_disease
Human_disease = db.Human_disease(db)

#Ontology
Ontology_Terms = db.Ontology_Terms(db)

#Organisms
Organisms = db.Organisms(db)

#Insertions
Insertions = db.Insertions(db)

#Clones
Clones = db.Clones(db)

#References
References = db.References(db)