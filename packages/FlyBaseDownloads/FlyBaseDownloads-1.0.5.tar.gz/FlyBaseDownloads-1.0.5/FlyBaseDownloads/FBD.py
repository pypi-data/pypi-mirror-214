#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 12:42:17 2023

@author: javiera.quiroz
"""

from .classes.Synonyms import Synonyms
from .classes.Genes import Genes
from .classes.Gene_Ontology_annotation import Gene_Ontology_annotation
from .classes.Gene_groups import Gene_groups
from .classes.Homologs import Homologs
from .classes.Ontology_Terms import Ontology_Terms
from .classes.Organisms import Organisms
from .classes.Insertions import Insertions
from .classes.Clones import Clones
from .classes.References import References
from .classes.Alleles_Stocks import Alleles_Stocks
from .classes.Human_disease import Human_disease



class FBD():
    
    def __name__(self):
        self.__name__ = 'FlyBase Downloads'
    
    def __init__(self):
        self.main_url = 'ftp://ftp.flybase.net/releases/current/precomputed_files/'
        self.Synonyms = Synonyms(self.main_url)
        self.Genes = Genes(self.main_url)
        self.GOAnn = Gene_Ontology_annotation(self.main_url) 
        self.Gene_groups = Gene_groups(self.main_url)
        self.Homologs = Homologs(self.main_url)
        self.Ontology_Terms = Ontology_Terms(self.main_url)
        self.Organisms = Organisms(self.main_url)
        self.Insertions = Insertions(self.main_url)
        self.Clones = Clones(self.main_url)
        self.References = References(self.main_url)
        self.Alleles_Stocks = Alleles_Stocks(self.main_url)
        self.Human_disease = Human_disease(self.main_url)
        