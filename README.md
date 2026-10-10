### **PLEASE READ**

**Demo Note:** Streamlit Community Cloud automatically puts apps to sleep after 12 hours of inactivity. If the CFTR Variant Explorer has been inactive and is temporarily asleep when you open it, this is normal Streamlit behavior and does not indicate a problem with the application. Simply click “Yes, get this app back up!” when prompted, and the application should load normally after it wakes.

# CFTR Variant Explorer

**UnivaBio Hackathon 2026**

An interactive bioinformatics tool for exploring genetic variants across the CFTR protein, examining evolutionary conservation and protein regions, and predicting the consequences of eligible amino-acid substitutions using machine learning.

# Project Overview

I developed the CFTR Variant Explorer to investigate where genetic variants occur across the CFTR protein, what types of variants occur at those positions, and what characteristics of the affected protein regions might help explain differences in their potential functional effects.

The project combines computational bioinformatics analysis with machine learning and an interactive Streamlit application. Users can enter a human CFTR amino-acid position and explore its recorded variants, conservation score, and assigned protein domain. They can also examine variant consequences, compare conservation across major CFTR domains, view variant distributions across protein regions, and explore machine-learning predictions for eligible substitutions.

# Research Question

Where do CFTR variants occur across the protein, what types of variants occur at those positions, and what characteristics of the affected protein regions might help explain their different effects on CFTR function?

# Why CFTR?

I chose CFTR because it is a well-studied protein with extensive publicly available biological and genetic data. This made it a practical protein for investigating relationships between variant location, variant consequence, evolutionary conservation, and protein-region characteristics.

CFTR is also clinically important because substantial disruption of its function is associated with cystic fibrosis. This provided a meaningful biological context for investigating how variants are distributed throughout the protein and how different characteristics of CFTR regions may relate to variant consequences.

# What the CFTR Variant Explorer Does

Users can enter a human CFTR amino-acid position and select which analyses they want to explore. The application uses a section chooser rather than displaying every result at once.

The Position Metrics section displays the selected position, its conservation score, and its assigned protein domain. Clicking a metric name reveals its definition. Conservation scores are rounded to two decimal places for display.

The Machine Learning Prediction section allows users to select an eligible recorded amino-acid substitution and view its predicted consequence, recorded consequence, and model confidence. The prediction applies to the selected substitution rather than every variant at that position. The application also explains why certain consequence categories are not supported by the prediction model.

The Model Performance section displays the model’s accuracy and macro F1 score. These metrics provide an overview of its performance, although they do not guarantee that an individual prediction is correct.

The CFTR Domain Conservation section compares average conservation across five major CFTR domains and the “Other” category. The Variant Consequences section displays a position-specific consequence chart alongside a table summarizing consequence counts across the dataset. Its glossary provides explanations of the consequence categories. The Variant Distribution by Protein Region section shows how recorded variants are distributed across the N-terminal, Middle, and C-terminal regions used in the analysis.

Finally, the Interpretation section discusses the broader biological context of the analyses, including CFTR function, variant consequences, and why different variants may have different effects.

Some sections are unavailable for position 1481 because it falls outside the standard machine-learning prediction workflow.

# Data and Methodology

I used publicly available CFTR sequence and variant data, including the human CFTR reference sequence (UniProt accession P13569).

The analysis included processing and characterizing recorded CFTR variants, examining variant positions and consequences, collecting CFTR protein sequences from different organisms, filtering the sequences to retain appropriate CFTR homologs, performing multiple sequence alignment using Clustal Omega, calculating evolutionary conservation across alignment positions, and mapping alignment positions back to human CFTR amino-acid positions.

I also compared conservation with variant distribution, assigned human CFTR positions to major protein domains using UniProt annotations, and developed sequence-based and amino-acid property features for machine learning. The resulting analyses and trained model were incorporated into the interactive Streamlit application.

# Evolutionary Analysis

To investigate evolutionary conservation, I compared CFTR protein sequences from different organisms using multiple sequence alignment.

Conservation scores were calculated from the aligned sequences and mapped back to human CFTR positions. Alignment-based features were also used as inputs for the machine-learning analysis, including the frequency of the human residue, frequency of the mutant residue, gap frequency, number of distinct residues observed at an alignment position, and whether the mutant residue was observed among the aligned sequences.

This allowed evolutionary information to be incorporated into both the broader conservation analysis and the machine-learning feature set.

# Domain Analysis

Human CFTR positions were assigned to five major protein regions based on the curated UniProt annotation for CFTR_HUMAN (P13569).

TMD1: residues 81–365

NBD1: residues 423–646

R domain: residues 654–831

TMD2: residues 859–1155

NBD2: residues 1210–1443

Positions outside these annotated regions were classified as “Other.”

The application compares average conservation across these regions using the conservation values included in the app. These comparisons provide a broader view of conservation across CFTR rather than a conservation calculation specific to the position being explored.

# Machine Learning Analysis

I developed a machine-learning component to predict the likely consequence of eligible CFTR amino-acid substitutions.

The model uses a combination of variant-level, evolutionary, and amino-acid property features. These include the human CFTR position, wild-type and mutated amino acids, alignment position, human residue frequency, mutant residue frequency, gap frequency, number of distinct residues observed, whether the mutant residue is observed in the alignment, and changes in amino-acid hydrophobicity, polarity, charge, and size.

Categorical amino-acid features were converted into numerical indicator variables using one-hot encoding. Missing and non-finite numerical values were handled through preprocessing so that the resulting feature matrix could be used by the classifier.

Variant consequence labels were also prepared for model training. The small number of initiator codon variants and records represented by “-” were grouped into an “Other” category. Stop-loss variants were excluded from the machine-learning training dataset because there were too few examples to support reliable model training for that consequence class. Insertion variants were also excluded from the application’s prediction options because the available examples were insufficient for reliable learning.

A Random Forest classifier was trained using 300 decision trees with balanced class weighting and a fixed random state for reproducibility.

The application offers predictions for the supported consequence categories: missense, frameshift, stop gained, and in-frame deletion. When a user selects an eligible recorded substitution, the application displays the predicted consequence alongside its recorded consequence and the highest predicted class probability as a confidence value.

The model’s accuracy and macro F1 score are displayed separately in the Model Performance section. These metrics describe overall model performance and should not be confused with the confidence value for an individual prediction.

The machine-learning component is intended for exploratory computational analysis. Its predictions and confidence values should not be interpreted as clinical diagnoses or definitive determinations of variant pathogenicity.

# Variant Feature Engineering

Two main groups of features were developed for the machine-learning analysis.

The first group consists of evolutionary and alignment-based features derived from the multiple sequence alignment. These features describe how frequently the human and mutant residues occur at the corresponding alignment position, the frequency of gaps, the number of distinct residues observed, and whether the mutant residue is represented among the aligned sequences.

The second group consists of amino-acid property changes between the wild-type and mutated residues. These include changes in hydrophobicity, polarity, electrical charge, and molecular size.

Together, these features allow the model to consider both the evolutionary context of a position and the biochemical characteristics of the amino-acid substitution.

# Model Prediction

After training, the Random Forest model and its final feature-column structure were saved for use by the Streamlit application.

When a user selects an eligible variant in the Explorer, the application reconstructs the corresponding feature set and passes it to the trained model. The application then displays the predicted consequence, the recorded consequence from the dataset, and the model confidence.

This provides an interactive way to examine how the computational model classifies individual substitutions and where its predictions agree or differ from the recorded annotations.

# Handling Position 1481

The canonical human CFTR protein contains 1,480 amino acids, but the variant dataset includes a recorded variant at position 1481. This variant is classified as a stop-loss variant, which affects the normal signal marking the end of the protein-coding sequence.

Because position 1481 falls outside the canonical 1,480-amino-acid CFTR sequence, it cannot be assigned a standard evolutionary conservation score or mapped to one of the major CFTR protein domains used in this analysis.

Rather than estimating or creating information that is not supported by the data, the application handles this position as a special case. It displays the available recorded variant information, classifies the position as “Other,” and reports conservation as N/A. The Machine Learning Prediction and Model Performance sections are not offered for this position.

# Technology

This project uses Python, Pandas, NumPy, Biopython, scikit-learn, joblib, Matplotlib, Altair, Streamlit, EMBL’s Clustal Omega, Google Colab, and UniProt data.

# Repository Structure

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

Running the Application

Install the required dependencies:

``` bash
pip install -r requirements.txt
```

Then run the Streamlit application from the directory containing app.py:

streamlit run app.py

# Limitations

This project is intended for exploratory bioinformatics analysis and does not diagnose disease, predict individual patient outcomes, or determine whether a specific variant is clinically harmful.

The presence, frequency, or consequence category of a variant does not by itself establish its clinical significance. Evolutionary conservation and other characteristics examined in this project describe patterns within the analyzed datasets and should not be interpreted as proof of causation.

The machine-learning model is limited by the size, composition, and quality of the available variant dataset. Some consequence categories contain relatively few examples, which limits how reliably they can be modeled. Stop-loss and insertion variants are not offered for prediction because of their limited representation in the training data. The model also does not attempt to predict every possible CFTR variant consequence.

The evolutionary analysis depends on the sequences included in the multiple sequence alignment and the methods used to calculate conservation. The domain conservation comparison uses the values included in the application, while the position metrics display conservation associated with the selected position when available.

# Sources

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
