# CFTR Variant Explorer

## UnivaBio Hackathon 2026

An interactive bioinformatics tool for exploring genetic variants across the CFTR protein and examining their locations, consequences, evolutionary conservation, protein-region characteristics, and predicted variant consequences using machine learning.

### Project Overview

I developed the CFTR Variant Explorer to investigate where genetic variants occur across the CFTR protein, what types of variants occur at those positions, and what characteristics of the affected protein regions might help explain differences in their potential functional effects.

The project combines computational bioinformatics analysis with machine learning and an interactive Streamlit application. Users can enter a human CFTR amino-acid position and explore the variants recorded at that position, associated protein characteristics, broader patterns across CFTR, and machine-learning predictions for eligible amino-acid substitutions.

### Research Question

Where do CFTR variants occur across the protein, what types of variants occur at those positions, and what characteristics of the affected protein regions might help explain their different effects on CFTR function?

### Why CFTR?

I chose CFTR because it is a well-studied protein with extensive publicly available biological and genetic data. This made it a practical protein for investigating relationships between variant location, variant consequence, evolutionary conservation, and protein-region characteristics.

CFTR is also clinically important because substantial disruption of CFTR function is associated with cystic fibrosis. This provided a meaningful biological context for investigating how variants are distributed throughout the protein and how different characteristics of CFTR regions may relate to variant consequences.

### What the CFTR Variant Explorer Does

Users can enter a human CFTR amino-acid position and explore information associated with that position, including the CFTR protein domain, evolutionary conservation, number of recorded variants, variants recorded at the position, and variant consequences.

The application also provides broader visualizations of conservation and variant distribution across CFTR. These visualizations allow individual positions to be examined within the larger context of the protein.

For eligible amino-acid substitutions, the application also provides a machine-learning prediction of the likely variant consequence. The prediction section allows users to select a recorded substitution, view the model’s predicted consequence, compare it with the recorded consequence in the dataset, and view the model’s confidence.

### Data and Methodology

I used publicly available CFTR sequence and variant data, including the human CFTR reference sequence (UniProt accession P13569).

The analysis included processing and characterizing recorded CFTR variants, examining variant positions and consequences, collecting CFTR protein sequences from different organisms, filtering the sequences to retain appropriate CFTR homologs, performing multiple sequence alignment using Clustal Omega, calculating evolutionary conservation across alignment positions, mapping alignment positions back to human CFTR amino-acid positions, comparing conservation with variant distribution, assigning human CFTR positions to major protein domains using UniProt annotations, comparing variant consequences and conservation across CFTR domains, engineering sequence- and mutation-level features for machine learning, training a Random Forest classifier to predict variant consequence categories, and incorporating the resulting analyses into the interactive CFTR Variant Explorer.

### Evolutionary Analysis

To investigate evolutionary conservation, I compared CFTR protein sequences from different organisms using multiple sequence alignment.

Conservation scores were calculated from the aligned sequences and mapped back to human CFTR positions. Alignment-based features were also used as inputs for the machine-learning analysis, including the frequency of the human residue, frequency of the mutant residue, gap frequency, number of distinct residues observed at an alignment position, and whether the mutant residue was observed among the aligned sequences.

This allowed evolutionary information to be incorporated into both the broader conservation analysis and the machine-learning feature set.

### Domain Analysis

Human CFTR positions were assigned to five major protein regions based on the curated UniProt annotation for CFTR_HUMAN (P13569).

TMD1: residues 81–365

NBD1: residues 423–646

R domain: residues 654–831

TMD2: residues 859–1155

NBD2: residues 1210–1443

Positions outside these annotated regions were classified as “Other.”

### Machine Learning Analysis

I developed a machine-learning component to predict the likely consequence of eligible CFTR amino-acid substitutions.

The model uses a combination of variant-level, evolutionary, and amino-acid property features. These include the human CFTR position, wild-type and mutated amino acids, alignment position, human residue frequency, mutant residue frequency, gap frequency, number of distinct residues observed, whether the mutant residue is observed in the alignment, and changes in amino-acid hydrophobicity, polarity, charge, and size.

Categorical amino-acid features were converted into numerical indicator variables using one-hot encoding. Missing and non-finite numerical values were handled through preprocessing so that the resulting feature matrix could be used by the classifier.

Variant consequence labels were also prepared for model training. The small number of initiator codon variants and records represented by “-” were grouped into an “Other” category. Stop-loss variants were excluded from the machine-learning training dataset because only a very small number were available, which was insufficient to support reliable model training for that consequence class.

A Random Forest classifier was then trained using 300 decision trees with balanced class weighting and a fixed random state for reproducibility.

The trained model predicts the consequence category of a selected amino-acid substitution and provides the highest predicted class probability as a confidence value. In the interactive application, the predicted consequence is displayed alongside the recorded consequence so that the prediction can be compared with the observed annotation.

The machine-learning component is intended as an exploratory computational analysis. Model predictions and confidence values should not be interpreted as clinical diagnoses or definitive determinations of variant pathogenicity.

### Variant Feature Engineering

Two main groups of features were developed for the machine-learning analysis.

The first group consists of evolutionary and alignment-based features derived from the multiple sequence alignment. These features describe how frequently the human and mutant residues occur at the corresponding alignment position, the frequency of gaps, the number of distinct residues observed, and whether the mutant residue is represented among the aligned sequences.

The second group consists of amino-acid property changes between the wild-type and mutated residues. These include changes in hydrophobicity, polarity, electrical charge, and molecular size.

Together, these features allow the model to consider both the evolutionary context of a position and the biochemical characteristics of the amino-acid substitution.

### Model Prediction

After training, the Random Forest model and its final feature-column structure were saved for use by the Streamlit application.

When a user selects an eligible variant in the Explorer, the application reconstructs the same feature set used during training, applies the same preprocessing structure, and passes the resulting features to the trained model.

The application then displays the predicted consequence, the recorded consequence from the dataset, and the model confidence. This provides an interactive way to examine how the computational model classifies individual substitutions and where its predictions agree or differ from the recorded annotations.

### Technology

This project uses Python, Pandas, NumPy, Biopython, scikit-learn, joblib, Matplotlib, Altair, Streamlit, EMBL’s Clustal Omega, Google Colab, and UniProt data.

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

``` bash
pip install -r requirements.txt
```

Then run the Streamlit application:

streamlit run app.py

### Limitations

This project is intended for exploratory bioinformatics analysis and does not diagnose disease, predict individual patient outcomes, or determine whether a specific variant is clinically harmful.

The presence, frequency, or consequence category of a variant does not by itself establish its clinical significance. Evolutionary conservation and other characteristics examined in this project describe patterns within the analyzed datasets and should not be interpreted as proof of causation.

The machine-learning model is also limited by the size, composition, and quality of the available variant dataset. Some consequence categories contain relatively few examples and therefore may not provide enough observations for reliable model training. Stop-loss variants were excluded from model training because of their small sample size.

The model is designed for eligible standard amino-acid substitutions and does not attempt to predict every possible CFTR variant consequence. Predictions should therefore be interpreted as computational classifications within the context of the training dataset rather than definitive biological or clinical conclusions.

The evolutionary analysis is dependent on the sequences included in the multiple sequence alignment and the methods used to calculate conservation.

### Sources

**Protein and Domain Information**

UniProtKB. CFTR_HUMAN (P13569).

https://www.uniprot.org/uniprotkb/P13569

**CFTR Structure and Function**

Csanády, L., Vergani, P., & Gadsby, D. C. (2019). Structure, Gating, and Regulation of the CFTR Anion Channel. Physiological Reviews, 99(1), 707–738.

https://doi.org/10.1152/physrev.00007.2018

**CFTR Molecular Evolution**

Infield, D. T., et al. (2021). The molecular evolution of function in the CFTR chloride channel. Journal of General Physiology, 153(12), e202012625.

https://doi.org/10.1085/jgp.202012625

**Acknowledgments**

This project was developed as an individual entry for the UnivaBio Hackathon 2026.

The accompanying research notebook documents the computational analysis, evolutionary analysis, machine-learning development, and application development process used to create the CFTR Variant Explorer.
