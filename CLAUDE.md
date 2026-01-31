# Cellmarker Annotation App

## Development Environment Setup

Please run any command in the mamba environment named `cellmarkerAnno`.

The `mamba` command location is: `/home/hzl/miniforge3/bin/mamba`.

Here is the example command to install python packages by `pip` in the `cellmarkerAnno` environment:

```bash
/home/hzl/miniforge3/bin/mamba run -n cellmarkerAnno pip install <package_name>
```

And the `streamlit` is installed in the `cellmarkerAnno` environment. You can run the streamlit app by:

```bash
/home/hzl/miniforge3/bin/mamba run -n cellmarkerAnno streamlit run app.py
```

## Application Overview

This application is designed for query the cell marker information from the CellMarker database. It provides an interactive interface to search for cell markers based on cell types, tissues, and species.

## The CellMarker Database

The CellMarker database is an Excel file named `Cell_marker_All.xlsx`, which path can be set in the `app.py` file. 

The database contains comprehensive information about cell markers. Here are the first 10 rows of the database:

```text
species	tissue_class	tissue_type	uberonongology_id	cancer_type	cell_type	cell_name	cellontology_id	marker	Symbol	GeneID	Genetype	Genename	UNIPROTID	technology_seq	marker_source	PMID	Title	journal	year
Human	Abdomen	Abdomen	UBERON_0000916	Normal	Normal cell	Macrophage	CL_0000235	MERTK	MERTK	10461	protein_coding	MER proto-oncogene, tyrosine kinase	Q12866	None	Experiment	31982413	Peritoneal Level of CD206 Associates With Mortality and an Inflammatory Macrophage Phenotype in Patients With Decompensated Cirrhosis and Spontaneous Bacterial Peritonitis	Gastroenterology	2020
Human	Abdomen	Abdomen	UBERON_0000916	Normal	Normal cell	Macrophage	CL_0000235	CD16	FCGR3A	2215	protein_coding	Fc fragment of IgG receptor IIIb	O75015	None	Experiment	31982413	Peritoneal Level of CD206 Associates With Mortality and an Inflammatory Macrophage Phenotype in Patients With Decompensated Cirrhosis and Spontaneous Bacterial Peritonitis	Gastroenterology	2020
Human	Abdomen	Abdomen	UBERON_0000916	Normal	Normal cell	Macrophage	CL_0000235	CD206	MRC1	4360	protein_coding	mannose receptor C-type 1	P22897	None	Experiment	31982413	Peritoneal Level of CD206 Associates With Mortality and an Inflammatory Macrophage Phenotype in Patients With Decompensated Cirrhosis and Spontaneous Bacterial Peritonitis	Gastroenterology	2020
Human	Abdomen	Abdomen	UBERON_0000916	Normal	Normal cell	Macrophage	CL_0000235	CRIg	VSIG4	11326	protein_coding	V-set and immunoglobulin domain containing 4	Q9Y279	None	Experiment	31982413	Peritoneal Level of CD206 Associates With Mortality and an Inflammatory Macrophage Phenotype in Patients With Decompensated Cirrhosis and Spontaneous Bacterial Peritonitis	Gastroenterology	2020
Human	Abdomen	Abdomen	UBERON_0000916	Normal	Normal cell	Macrophage	CL_0000235	CD163	CD163	9332	protein_coding	CD163 molecule	Q86VB7	None	Experiment	31982413	Peritoneal Level of CD206 Associates With Mortality and an Inflammatory Macrophage Phenotype in Patients With Decompensated Cirrhosis and Spontaneous Bacterial Peritonitis	Gastroenterology	2020
Human	Abdomen	Abdominal fat pad		Normal	Normal cell	Brown adipocyte	CL_0000449	FABP4	FABP4	2167	protein_coding	fatty acid binding protein 4	E7DVW4	sci-RNA-seq	Experiment	32355218	Single-cell transcriptional networks in differentiating preadipocytes suggest drivers associated with tissue heterogeneity	Nature communications	2020
Human	Abdomen	Abdominal fat pad		Normal	Normal cell	Brown adipocyte	CL_0000449	PDGFRα 						sci-RNA-seq	Experiment	32355218	Single-cell transcriptional networks in differentiating preadipocytes suggest drivers associated with tissue heterogeneity	Nature communications	2020
Human	Abdomen	Abdominal fat pad		Normal	Normal cell	Brown adipocyte	CL_0000449	UCP1	UCP1	7350	protein_coding	uncoupling protein 1	P25874	sci-RNA-seq	Experiment	32355218	Single-cell transcriptional networks in differentiating preadipocytes suggest drivers associated with tissue heterogeneity	Nature communications	2020
Mouse	Abdomen	Muscle	UBERON_0001630	Normal	Normal cell	Fibro-adipogenic progenitor cell		Wisp1	Ccn4	22402	protein_coding	cellular communication network factor 4	O54775	10x Chromium	Experiment	35439171	An estrogen-sensitive fibroblast population drives abdominal muscle fibrosis in an inguinal hernia mouse model	JCI insight	2022
```
