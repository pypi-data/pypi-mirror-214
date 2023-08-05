# FlyBaseDownloads

Python package to facilitate the data download from FlyBase. Most of the available data from their official wiki can be downloaded. One of the purposes of this library is to organize the data as closely as possible to the source, **FlyBase**. Despite not being the official package, it is organized by data class/type and provides direct downloads of the current bulk data files from the FTP site.
For more information, visit the [official FlyBase wiki](https://wiki.flybase.org/wiki/FlyBase:Downloads_Overview).


# Bulk data files

In order to simplify the download of FlyBase files, the names have been kept as close as possible. To access the data, follow these steps:

1. Install the library using the pip command.

    > pip install FlyBaseDownloads

2. Import the library into your file.

    > import FlyBaseDownloads as FBD

3. Access the different classes of the library described below.



## Synonyms

To download the file, execute the following command.

    Synonyms = FBD.Synonyms.get()

The file reports current symbols and synonyms for the following objects in FlyBase: genes (FBgn), alleles (FBal), balancers (FBba), aberrations (FBab), transgenic constructs (FBtp), insertions (FBti), transcripts (FBtr), and proteins (FBpp).

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
| primary_FBid   | Primary FlyBase identifier for the object |
| organism_abbreviation   | Abbreviation (from the Species Abbreviations list) indicating the species of origin |
| current_symbol   | Current symbol used in FlyBase for the object |
| current_fullname   | Current full name used in FlyBase for the object|
| fullname_synonym(s)   | 	Non-current full name(s) associated with the object (pipe separated values) |
| symbol_synonym(s)   | Non-current symbol(s) associated with the object (pipe separated values) |


## Genes

To facilitate its usage, it is suggested to access the data using the following command.

    Genes = FBD.Genes

Then, enter the specific method according to the desired data

#### Genetic interaction table

To download the file, execute the following command.

    Genetic_interaction_table = Genes.Genetic_interaction_table()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
| Starting_gene(s)_symbol | Current FlyBase symbol of gene(s) involved in the starting genotype |
| Starting_gene(s)_FBgn | Current FlyBase identifier (FBgn#) of gene(s) involved in the starting genotype |
| Interacting_gene(s)_symbol | Current FlyBase symbol of gene(s) involved in the interacting genotype |
| Interacting_gene(s)_FBgn | Current FlyBase identifier (FBgn#) of gene(s) involved in the interacting genotype |
| Interaction_type | Type of interaction observed, either 'suppressible' or 'enhanceable' |
|Publication_FBrf | Current FlyBase identifier (FBrf#) of publication from which the data came |


#### RNA-Seq RPKM values

To download the file, execute the following command.

    RNASeq_values = Genes.RNASeq_values()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
| Release_ID | The D. melanogaster annotation set version from which the gene model used in the analysis derives |
| FBgn#	| The unique FlyBase gene ID for this gene |
| GeneSymbol	| The official FlyBase symbol for this gene |
| Parent_library_FBlc# | The unique FlyBase ID for the dataset project to which the RNA-Seq experiment belongs |
| Parent_library_name	| The official FlyBase symbol for the dataset project to which the RNA-Seq experiment belongs |
| RNASource_FBlc#	| The unique FlyBase ID for the RNA-Seq experiment used for RPKM expression calculation |
| RNASource_name	| The official FlyBase symbol for the RNA-Seq experiment used for RPKM expression calculation |
| RPKM_value	| The RPKM expression value for the gene in the specified RNA-Seq experiment |
| Bin_value	| The expression bin classification of this gene in this RNA-Seq experiment, based on RPKM value. Bins range from 1 (no/extremely low expression) to 8 (extremely high expression)| 
| Unique_exon_base_count	T| he number of exonic bases unique to the gene (not overlapping exons of other genes). Field will be blank for genes derived from dicistronic/polycistronic transcripts |
| Total_exon_base_count	| The number of bases in all exons of this gene |
| Count_used	| Indicates if the RPKM expression value was calculated using only the exonic regions unique to the gene and not overlapping exons of other genes (Unique), or, if the RPKM expression value was calculated based on all exons of the gene regardless of overlap with other genes (Total). RPKM expression values are typically reported for the "Unique" count, except for genes on dicistronic/polycistronic transcripts, in which case the "Total" count is reported |

#### RNA-Seq RPKM values matrix

To download the file, execute the following command.

    RNASeq_values_matrix = Genes.RNASeq_values_matrix()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
| gene_primary_id	| The unique FlyBase gene ID for this gene.
|gene_symbol	| The official FlyBase symbol for this gene.|
| gene_fullname	| The official full name for this gene.|
| gene_type	| The type of gene: e.g., protein_coding_gene, non_protein_coding_gene.|
| DATASAMPLE_NAME_(DATASET_ID)	| Each subsequent column reports the gene RPKM values for the sample listed in the header. The dataset "FBlc" ID is listed in parentheses, and can be pasted into FlyBase search to access more information on the sample from the "dataset" report.|


#### Single Cell RNA-Seq Gene Expression

To download the file, execute the following command.

    SingleCellRNASeq_Gene_Expression = Genes.Single_Cell_RNA_Gene_Expression()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
| Pub_ID	| The FlyBase FBrf ID for the reference in which the expression was reported.| 
| Pub_miniref	| The FlyBase citation for the publication in which the expression was reported.| 
| Clustering_Analysis_ID	| The FlyBase FBlc ID for the dataset representing the clustering analysis.| 
| Clustering_Analysis_Name	| The FlyBase name for the dataset representing the clustering analysis.|
| Source_Tissue_Sex	| The sex of the source tissue used for the experiment: male, female or mixed.|
| Source_Tissue_Stage	| The life stage of the source tissue used for the experiment, using only high-level terms: embryonic stage, larval stage, pupal stage, adult stage or mixed.|
| Source_Tissue_Anatomy	| The anatomical region of the source tissue used for the experiment; only "mixed" is shown if many| 
| Cluster_ID	| The FlyBase FBlc ID for the dataset representing the cell cluster.| 
| Cluster_Name	| The FlyBase name for the dataset representing the cell cluster.|
| Cluster_Cell_Type_ID	| The FlyBase FBbt ID for the cell type represented by the cell cluster.| 
| Cluster_Cell_Type_Name	| The FlyBase name for the cell type represented by the cell cluster.| 
| Gene_ID	| The FlyBase FBgn ID for the expressed gene.| 
| Gene_Symbol	| The FlyBase symbol for the expressed gene (ASCII-format).|
| Mean_Expression	| The average level of expression of the gene across all cells of the cluster in which the gene is detected at all.|
| Spread	| The proportion of cells in the cluster in which the gene is detected.| 

#### Physical interaction MITAB file

To download the file, execute the following command.

    Physical_interaction_MITAB = Genes.Physical_interaction_MITAB()

Columns Description

| Column number	| Column heading	| General format	| FlyBase example	| Content description | 
|----------------------|--------------------|----------------------|--------------------|----------------------|
| 1 | ID(s) Interactor A                   | database:identifier            | flybase:FBgn0002121| The unique Flybase identifier for the first gene of the interacting pair.              |                           |
| 2 | ID(s) Interactor B                   | -                              | -                  | The unique Flybase identifier for the second gene of the interacting pair.             |                           |
| 3 | Alt ID(s) Interactor A               | database:identifier            | flybase:CG2671\| entrez gene/locuslink:33156 | The alternative gene identifiers currently provided are Flybase annotation IDs (CG#) and NCBI’s Entrez Gene ID separated by “\|“                           |
| 4 | Alt ID(s) Interactor B               | -                              | -                  |                        -                          |
| 5 | Alias(es) Interactor A               | database:name(alias type)      | flybase:l(2)gl(gene name) | The official Flybase gene symbol. It is referred to as “gene name” to adhere to the psi-mi ontology. |                           |
| 6 | Alias(es) Interactor B               | -                              | ”-                  |                    -      |                       
| 7 | Interaction Detection Method(s)      | ontology:identifier(method name) | psi-mi:"MI:0006"(anti bait coimmunoprecipitation) | The assay used to detect the interaction, taken from the psi-mi ontology. |                           |
| 8 | Publication 1st Author(s)            | surname initial(s) (publication year) | Betschinger K. (2003) | The first author and year of the publication where the interaction is described. |                           |
| 9 | Publication ID(s)                    | database:identifier            | flybase:FBrf0157155\|pubmed:12629552 | The unique FlyBase identifier for the publication followed by the unique PubMed identifier (if there is one) separated by “\|”. |                           |
| 10| Taxid Interactor A                   | taxid:identifier               | taxid:7227("Drosophila melanogaster") | The NCBI taxonomy identifier for the source organism of the interactor. The vast majority of interactors in FlyBase come from D. melanogaster. There are, however, a few interspecies interactions consisting of a D. melanogaster interactor and an interactor of a different species. |                           |
| 11| Taxid Interactor B                   | -                              | -                  |           -                |                           
| 12| Interaction Type(s)                  | ontology:identifier(interaction type) | psi-mi:"MI:0915"(physical association) | Taken from the psi-mi ontology. Most often “physical association” for FlyBase. |                           |
| 13| Source Database(s)                   | ontology:identifier(database name) | psi-mi:"MI:0478"(flybase) | All interactions are curated by FlyBase. |                           
| 14| Interaction Identifier(s)            | database:identifier            | flybase:FBrf0157155-13.coIP.WB | The unique FlyBase identifier for this interaction. |                                             
| 15	| Confidence Value(s) |	-|-|		Not applicable	
| 16	| Expansion Method(s) |-|-| Not applicable
| 17	| Biological Role(s)  Interactor A	| -|-|		Not applicable	
| 18	| Biological Role(s) Interactor B	| -|-|		Not applicable	
| 19	| Experimental Role(s) Interactor A	| ontology:identifier(experimental role name) |	psi-mi:"MI:0496"(bait)	| The role played by the interactor in the experiment. Taken from the psi-mi ontology.	|
| 20	| Experimental Role(s) Interactor B | -|-|	-|	
| 21	| Type(s) Interactor A |	ontology:identifier(interactor type name)	| psi-mi:"MI:0326"(protein)	| The molecule type. For FlyBase, these are limited to protein or ribonucleic acid. Taken from the psi-mi ontology.	|
| 22	| Type(s) Interactor B	| -|-|-|		
| 23	| Xref(s) Interactor A	|-|-|	Not applicable	
| 24	| Xref(s) Interactor B	|	-|-|	Not applicable	
| 25	| Interaction Xref(s) |	database:identifier	| flybase:FBig0000000103	| Cross references for the interactions. For Flybase, these include an interaction group identifier (FBig) and possibly a collection identifier (FBlc) separated by “\|”. All experiments that show an interaction between the products of gene A and gene B are compiled into an A-B interaction group, such that all interactions are associated with an interaction group identified by an FBig number. Interactions identified as part of a large scale study are also associated with the collection identifier, or FBlc number.	|
| 26	| Annotation(s) Interactor A |	topic:text	isoform-| comment:a isoform	| Information on whether the interaction is specific to a particular interactor isoform.	
| 27	| Annotation(s) Interactor B |	- | - | -| 	
| 28	| Interaction Annotation(s) |	topic:text	| comment:Phosphorylated isoforms of @l(2)gl@ are absent when @aPKC@ is knocked down by RNAi.	| Describes the source(s) of the interaction participants and includes free text comments about the interaction.	|
| 29	| Host Organism(s)	|	- | - | Not applicable	|
| 30	| Interaction Parameters  | - | -	|	Not applicable	|
| 31	| Creation Date	| - | - |	Not applicable	|
| 32	| Update Date	| - | - |		Not applicable	|
| 33	| Checksum Interactor A	| - | -	|	Not applicable	|
| 34	| Checksum Interactor B	| - | -	|	Not applicable	|
| 35	| Interaction Checksum	| - | -	|	Not applicable	|
| 36	| Negative |-| FALSE	| 	All interactions in FlyBase are positive.	|
| 37	| Feature(s) Interactor A	| feature_type:range(text)	| sufficient binding region:aa 1-58(N-terminal region)	| Describes features of Interactor A such as binding sites, mutations that disrupt the interaction, epitope tags, etc.	|
| 38	| Feature(s) Interactor B	| -	| - | -|
| 39	| Stoichiometry Interactor A |-|-| Not applicable	|
| 40	| Stoichiometry Interactor B |-|-| Not applicable| 
| 41	| Identification Method(s) Participant A	|-|-|	Not applicable| 
| 42	| Identification Method(s) Participant B |-|-|	Not applicable| 


#### Functional complementation table

To download the file, execute the following command.

    Functional_complementation = Genes.Functional_complementation()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
| Dmel gene (symbol)	|Current FlyBase symbol of Dmel gene.|
| Dmel gene (FBgn)	| Current FlyBase identifier (FBgn#) of Dmel gene in column 1.|
| Functionally complementing ortholog (symbol)	| Current FlyBase symbol of a non-Dmel ortholog of the Dmel gene in column 1 where this non-Dmel gene has been show to functionally complement the Dmel gene.|
| Functionally complementing ortholog (FBgn#)	| Current FlyBase identifier (FBgn#) of a non-Dmel ortholog of the Dmel gene in column 1 where this non-Dmel gene has been show to functionally complement the Dmel gene.|
| Supporting_FBrf	| Current FlyBase identifier (FBrf#) of the publication that provides support for the functional complementation statement (the publication that reported the suppression of a mutant phenotype of the Dmel gene by a transgenic construct/mutant allele of the non-Dmel ortholog).|

#### FBgn to DB Accession IDs

To download the file, execute the following command.

    FBgn_toDB_Accession_IDs = Genes.FBgn_toDB_Accession_IDs()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
| gene_symbol	|Current symbol of gene.|
| organism_abbreviation	| Abbreviation (from the Species Abbreviations list) indicating the species of origin of the gene.|
|	primary_FBgn#	| Current FlyBase identifier (FBgn#) of gene.|
nucleotide_accession	| EMBL/GenBank/DDBJ nucleotide accession associated with the gene.|
| na_based_protein_accession	| EMBL/GenBank/DDBJ protein accession associated with the gene and the nucleotide accession in the preceeding 'nucleotide_accession' column|
| UniprotKB/Swiss-Prot/TrEMBL_accession	| UniProtKB/SwissProt/TrEMBL protein accession associated with the gene.|
|EntrezGene_ID	| NCBI Entrez ID associated with the gene.
|RefSeq_transcripts	| NCBI RefSeq transcript accession associated with the gene.|
RefSeq_proteins	| NCBI RefSeq protein accession associated with the gene and the transcript accession in the preceeding 'RefSeq_transcripts' column.|

#### FBgn to Annotation ID

To download the file, execute the following command.

    FBgn_toAnnotation_ID = Genes.FBgn_toAnnotation_ID()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
| gene_symbol	| Current symbol of gene.|
| organism_abbreviation	| Abbreviation (from the Species Abbreviations list) indicating the species of origin of the gene.|
| primary_FBgn#	| Current FlyBase identifier (FBgn#) of gene.|
| secondary_FBgn#(s)	| Secondary FlyBase identifier(s) (FBgn#) associated with the gene (comma separated values).| 
| annotation_ID	| Current annotation identifier associated with the gene.|
| secondary_annotation_ID(s)	|Secondary annotation identifier(s) associated with the gene (comma separated values).|

#### FBgn to GLEANR IDs

To download the file, execute the following command.

    FBgn_toGLEANR_IDs = Genes.FBgn_toGLEANR_IDs()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
|organism_abbreviation	| Abbreviation (from the Species Abbreviations list) indicating the species of origin of the gene.|
|gene_symbol	| Current FlyBase gene symbol.|
|primary_FBgn#	| Current FlyBase identifier (FBgn#) of the gene.|
|GLEANR_ID	| GLEANR identifier assigned by the AAA Consortium.|

#### FBgn to FBtr to FBpp IDs

To download the file, execute the following command.

    FBgn_to_FBtr_to_FBpp = Genes.FBgn_to_FBtr_to_FBpp()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
|FlyBase_FBgn	|Current FlyBase identifier (FBgn#) of the gene.|
|FlyBase_FBtr	|Current FlyBase identifier (FBtr#) of a transcript encoded by the gene listed in the preceeding 'FlyBase_FBgn' column.|
|FlyBase_FBpp	|Current FlyBase identifier (FBpp#) of a polypeptide encoded by the transcript listed in the preceeding 'FlyBase_FBtr' column, where this is relevant.|

#### FBgn to FBtr to FBpp IDs (expanded)

To download the file, execute the following command.

    FBgn_to_FBtr_to_FBpp_exp = Genes.FBgn_to_FBtr_to_FBpp_expanded()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
| organism	|Abbreviation (from the Species Abbreviations list) indicating the species of origin of the gene.|
|gene_type	|The type of gene, represented by a Sequence Ontology term.|
|gene_ID	|Current "FBgn" identifier of gene.|
|gene_symbol	|Current symbol of the gene.|
|gene_fullname	|Current full name of the gene.|
|annotation_ID	|Current FlyBase annotation identifier of the gene.|
|transcript_type	|The type of transcript, represented by a Sequence Ontology term.|
|transcript_ID	|Current FlyBase annotation identifier of the transcript.|
|transcript_symbol	|Current symbol of the transcript.|
|polypeptide_ID	|Current FlyBase annotation identifier of the polypeptide.|
|polypeptide_symbol	|Current symbol of the polypeptide.|

#### FBgn exons to Affy1 

To download the file, execute the following command.

    FBgn_exons2affy1 = Genes.FBgn_exons2affy1()

The file is generated by testing for overlaps, no matter how small, of the locations of Affy1 oligos in the genome with the locations of gene exons, as defined by the Dmel gene models for the current release of FlyBase. If the location of an Affy1 oligo shows any kind of overlap with an exon of a gene, a Gene=>Affy reference is recorded in this file.

The extent of the overlap has no influence on the inclusion of a crossreference in this file. The overlap might be just one nucleotide, or it could be an exact match to the exon. For interpretation of the significance of a partial overlap please contact Affymetrix.

The file includes the following Dmel genes:

 - Nuclear genes located to the sequence


it excludes:
 - genes not located to the sequence
 - mitochondrial genes

The first column of a line it is the FBgn ID, and the second one is the Affy1 ID that overlaps with an exon of the gene.

#### FBgn exons to Affy2

To download the file, execute the following command.

    FBgn_exons2affy2 = Genes.FBgn_exons2affy2()

Similar to the Affy1 but with Affy2.

#### Genes Sequence Ontology (SO) data

To download the file, execute the following command.

    Genes_Sequence_Ontology = Genes.Genes_Sequence_Ontology()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
|gene_primary_id	|The unique FlyBase gene ID for this gene.|
|gene_symbol	|The official FlyBase symbol for this gene.|
|so_term_name	|The SO term name.|
|so_term_id	|The SO term primary identifier.|

#### Genes map table

To download the file, execute the following command.

    Genes_map = Genes.Genes_map()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
|organism_abbreviation	|Abbreviation (from the Species Abbreviations list) indicating the species of origin of the gene.|
|current_symbol	|Current FlyBase gene symbol.|
|primary_FBid	|Current FlyBase identifier (FBgn#) of gene.|
|recombination_loc	|Recombination map location.|
|cytogenetic_loc	|Cytogenetic location.|
|sequence_loc	|Genomic location.|

#### Best gene summaries

To download the file, execute the following command.

    Best_gene_summaries = Genes.Best_gene_summaries()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
|FBgn_ID	|Current FlyBase identifier number for the gene.|
|Gene_Symbol	|Current FlyBase symbol of the gene.|
|Summary_Source	|The source of the gene summary.|
|Summary	|The gene summary text.|

### Automated_gene_summaries

To download the file, execute the following command.

`Automated_gene_summaries = Genes.Automated_gene_summaries()`

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
|FlyBase ID. | The Valid FlyBase identifier number for the gene.|
|Summary| The gene summary as a string of plain text.|

#### Gene Snapshots

To download the file, execute the following command.

    Gene_Snapshots = Genes.Gene_Snapshots()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
|FBgn_ID	|Current FlyBase identifier number for the gene.|
|GeneSymbol	|Current FlyBase symbol of the gene.|
|GeneName	|Current FlyBase name of the gene.|
|datestamp	|Date on which the information was last reviewed.|
|gene_snapshot_text	| Gene snapshot information for the gene. Cases that are in progress or are deemed to have insufficient data to summarize are stated as such|


#### Unique protein isoforms

To download the file, execute the following command.

    Unique_protein_isoforms = Genes.Unique_protein_isoforms()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
|FBgn	|Current FlyBase identifier (FBgn#) of the gene.|
|FB_gene_symbol	|Current FlyBase gene symbol of the gene.|
|representative_protein	|Current FlyBase protein symbol of the representative protein isoform.|
|identical_protein(s)	|Current FlyBase protein symbol(s) of identical protein isoforms.|

### Non-coding RNAs

To download the file, execute the following command.

    Noncoding_RNAs = Genes.Noncoding_RNAs()

This file reports all ncRNAs with gene models supported by FlyBase in JSON format, as submitted to [RNAcentral](http://rnacentral.org/). Pseudogenes are excluded. In addition to the symbols and IDs for ncRNAs, this file also includes their associated gene, genomic location, sequence, Sequence Ontology classification, etc.


#### Enzyme data

To download the file, execute the following command.

    Enzyme = Genes.Enzyme()

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
|group_id	|FlyBase gene group (FBgg) ID of the relevant terminal group within the ENZYMES (FBgg0001715) hierarchy (only terminal groups contain members).
|group_name	|FlyBase gene group (FBgg) name of relevant terminal group within the ENZYMES (FBgg0001715) hierarchy (only terminal groups contain members).|
|group_GO_ID	|The GO molecular function term ID on the given gene group. Multiple entries are separated with a pipe.|
|group_GO_name	|The GO molecular function term name on the given gene group. Multiple entries are separated with a pipe.|
|group_EC_number	|The EC number on the given gene group, if present. (This is computed, corresponding to the EC cross-reference on the GO molecular function term.)|
|group_EC_name	|The EC name on the given gene group, if present. (This is computed, corresponding to the EC cross-reference on the GO molecular function term.)|
|gene_id	|The current FlyBase gene ID (FBgn) of the gene.|
|gene_symbol	|The current FlyBase symbol of the gene.|
|gene_name	|The current FlyBase name of the gene.|
|gene_EC_number	|The EC number(s) associated with the gene, if present. Multiple entries are separated with a pipe. (This is computed, corresponding to the EC cross-reference(s) on any positive GO molecular function term(s) annotated to the gene.)
|gene_EC_name	|The EC name(s) associated with the gene, if present. Multiple entries are separated with a pipe. (This is computed, corresponding to the EC cross-reference(s) on any positive GO molecular function term(s) annotated to the gene.)|
