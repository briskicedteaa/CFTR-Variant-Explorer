# CFTR Variant Explorer

### UnivaBio Hackathon 2026

An interactive bioinformatics tool for exploring genetic variants across the CFTR protein and examining their locations, consequences, evolutionary conservation, and protein-region characteristics.

### Project Overview

I developed the CFTR Variant Explorer to investigate where genetic variants occur across the CFTR protein, what types of variants occur at those positions, and what characteristics of the affected protein regions might help explain differences in their potential functional effects.

The project combines computational analysis with an interactive Streamlit application that allows users to enter a CFTR amino-acid position and explore the variant information associated with it.

### Research Question

Where do CFTR variants occur across the protein, what types of variants occur at those positions, and what characteristics of the affected protein regions might help explain their different effects on CFTR function?

### Why CFTR?

I chose CFTR because it is a well-studied protein with extensive publicly available biological and genetic data. This made it a practical protein for investigating relationships between variant location, variant consequence, evolutionary conservation, and protein-region characteristics.

CFTR is also clinically important because substantial disruption of CFTR function is associated with cystic fibrosis. This provided a meaningful biological context for investigating how variants are distributed throughout the protein.

### What the CFTR Variant Explorer Does

Users can enter a human CFTR amino-acid position and explore information associated with that position, including the CFTR protein domain, evolutionary conservation, number of recorded variants, variants recorded at the position, and variant consequences.

The application also provides broader visualizations of conservation, variant distribution, and variant consequences to help place individual positions into the larger context of the CFTR protein.

### Data and Methodology

I used publicly available CFTR sequence and variant data, including the human CFTR reference sequence (UniProt accession P13569).

The analysis included processing and characterizing recorded CFTR variants, examining variant positions and consequences, collecting CFTR protein sequences from different organisms, filtering the sequences to retain appropriate CFTR homologs, performing multiple sequence alignment using Clustal Omega, calculating evolutionary conservation across alignment positions, mapping alignment positions back to human CFTR amino-acid positions, comparing conservation with variant distribution, assigning human CFTR positions to major protein domains using UniProt annotations, comparing variant consequences and conservation across CFTR domains, and incorporating the resulting analyses into the interactive CFTR Variant Explorer.

### Evolutionary Analysis

To investigate evolutionary conservation, I compared CFTR protein sequences from different organisms using multiple sequence alignment.

Conservation scores were calculated from the aligned sequences and mapped back to human CFTR positions. This allowed me to examine whether positions with different levels of evolutionary conservation showed different patterns of recorded variant distribution.

### Domain Analysis

Human CFTR positions were assigned to five major protein regions based on the curated UniProt annotation for CFTR_HUMAN (P13569).

TMD1: residues 81–365

NBD1: residues 423–646

R domain: residues 654–831

TMD2: residues 859–1155

NBD2: residues 1210–1443

Positions outside these annotated regions were classified as “Other.”

### Technology

This project uses Python, Pandas, NumPy, Biopython, Matplotlib, Altair, Streamlit, EMBL’s Clustal Omega, Google Colab, and UniProt data.

### Repository Structure
```text
CFTR-Variant-Explorer/
│
├── data/
├── figures/
├── images/
├── notebooks/
├── src/
├── README.md
└── requirements.txt
```

### Running the Application

Clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

Then run the Streamlit application:

streamlit run app.py

### Limitations

This project is intended for exploratory bioinformatics analysis and does not diagnose disease, predict individual patient outcomes, or determine whether a specific variant is clinically harmful.

The presence, frequency, or consequence category of a variant does not by itself establish its clinical significance. Evolutionary conservation and other characteristics examined in this project describe patterns within the analyzed datasets and should not be interpreted as proof of causation.

The evolutionary analysis is also dependent on the sequences included in the multiple sequence alignment and the methods used to calculate conservation.

### Sources

#### Protein and Domain Information

UniProtKB. CFTR_HUMAN (P13569).

https://www.uniprot.org/uniprotkb/P13569

#### CFTR Structure and Function

Csanády, L., Vergani, P., & Gadsby, D. C. (2019). Structure, Gating, and Regulation of the CFTR Anion Channel. Physiological Reviews, 99(1), 707–738.

https://doi.org/10.1152/physrev.00007.2018

#### CFTR Molecular Evolution

Infield, D. T., et al. (2021). The molecular evolution of function in the CFTR chloride channel. Journal of General Physiology, 153(12), e202012625.

https://doi.org/10.1085/jgp.202012625

#### Acknowledgments

This project was developed as an individual entry for the UnivaBio Hackathon 2026.

The accompanying research notebook documents the computational analysis and development process used to create the CFTR Variant Explorer.
