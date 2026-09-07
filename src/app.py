import streamlit as st
import pandas as pd
import altair as alt
from data_loader import load_data
from pathlib import Path
import joblib
from variant_explorer import (
    get_position_summary,
    get_consequence_summary,
    predict_consequence
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

model_metrics = joblib.load(
    DATA_DIR / "cftr_model_metrics1.pkl"
)

st.set_page_config(
    page_title="CFTR Variant Explorer",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600&family=Quicksand:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {

    font-family: 'Fredoka', sans-serif !important;

}

h1, h2, h3 {
    font-family: 'Fredoka', sans-serif !important;
}

.info-bubble {
    background: #fff4fa;
    border: 1.5px solid #ffc4e7;
    border-radius: 18px;
    padding: 18px 22px;
    margin: 14px 0;
    box-shadow: 0 3px 10px rgba(200, 90, 145, 0.08);
}

.info-bubble h3 {
    color: #c85a91;
    margin-top: 0;
}

.info-bubble p {
    font-weight: 700;
}

.info-bubble p {
    color: #4a3a42;
}
.glossary-metric {
    text-align: center;
}

.glossary-metric summary {
    cursor: pointer;
    list-style: none;
    font-family: 'Fredoka', sans-serif;
    font-size: 1.1rem;
    font-weight: 500;
    color: inherit;
    text-decoration: underline dotted;
    text-underline-offset: 3px;
}

.glossary-heading .glossary-metric summary {
    font-size: inherit;
}

.glossary-metric summary::-webkit-details-marker {
    display: none;
}

.glossary-value {
    text-align: center;
    font-family: 'Fredoka', sans-serif;
    font-size: 2rem;
    font-weight: 400;
    line-height: 1.2;
    margin-top: 0.15rem;
}
.glossary-definition {
    margin: 0.5rem auto;
    padding: 0.5rem;
    max-width: 280px;
    border-radius: 0.5rem;
    font-family: 'Quicksand', sans-serif;
    font-size: 0.85rem;
    line-height: 1.4;
    background: rgba(128, 128, 128, 0.1);
}
.position-1481-dropdown {
    width: 100%;
    max-width: 100%;
    text-align: center;
}
.position-1481-dropdown summary {
    cursor: pointer;
    list-style: none;
    font-family: 'Fredoka', sans-serif;
    font-size: 1.5rem;
    font-weight: 500;
    color: inherit;
    text-decoration: underline dotted;
    text-underline-offset: 3px;
}

.position-1481-dropdown summary::-webkit-details-marker {
    display: none;
}

.position-1481-content {
    width: 100%;
    max-width: 100%;
    margin: 0.75rem 0;
    font-family: 'Quicksand', sans-serif;
}

.position-1481-table {
    width: 100%;
    max-width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}

.position-1481-table th,
.position-1481-table td {
    padding: 14px 18px;
    text-align: left;
    vertical-align: top;
    border-bottom: 1px solid rgba(128, 128, 128, 0.25);
    word-wrap: break-word;
}

.position-1481-table th {
    font-weight: 600;
}

.position-1481-table th:first-child,
.position-1481-table td:first-child {
    width: 25%;
}

.position-1481-table th:last-child,
.position-1481-table td:last-child {
    width: 75%;
}
</style>
""", unsafe_allow_html=True)

from variant_explorer import (
    get_position_summary,
    get_consequence_summary
)

position_df, variants_df = load_data()

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

cftr_df = pd.read_csv(DATA_DIR / "CFTR_df.csv")

human_sequence = cftr_df.loc[
    cftr_df["ID"].astype(str).str.contains("P13569", na=False),
    "Sequence"
].iloc[0]

valid_positions = set(variants_df["Position"].dropna().astype(int))

st.markdown(
    "<h1 style='text-align: center; font-size: 3rem;'>"
    "CFTR Variant Explorer"
    "</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; font-family: Fredoka, sans-serif; font-size: 1.2rem; font-weight: 500;'>"
    "Explore CFTR variant locations, consequences, conservation, "
    "and protein-region characteristics."
    "</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; font-family: Fredoka, sans-serif; font-size: 1.2rem; font-weight: 500;'>"
    "<strong>WARNING:</strong> The Explorer will display results only for "
    "amino acid positions with recorded variants in this dataset. "
    "View positions with recorded variants then click “Explore Position” to search."
    "</p>",
    unsafe_allow_html=True
)

def glossary_metric(label, value, definition):
    st.markdown(
        f"""
        <details class="position-1481-dropdown">
            <summary>{label}</summary>
            <div class="glossary-definition">{definition}</div>
        </details>
        <div class="glossary-value">{value}</div>
        """,
        unsafe_allow_html=True
    )

GIF_PATH = Path(__file__).resolve().parent.parent / "images" / "8D83949E-9C79-479B-BD57-BA4F6ED95A0A.gif"

left, center, right = st.columns([1, 3, 1])

with center:
    st.image(
        str(GIF_PATH),
        use_container_width=True
    )

st.markdown(
    "<h3 style='text-align: center;'>Research Question</h3>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='font-family: Fredoka, sans-serif; font-size: 1.2rem; font-weight: 500;''>"
    "Where do CFTR variants occur across the protein, "
    "what types of variants "
    "occur at those positions, "
    "and what characteristics of the affected protein "
    "regions might help explain their different "
    "effects on CFTR function?"
    "</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align: center;'>Purpose</h3>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-bubble">
        <p style='text-align: center; font-family: Fredoka, sans-serif; font-size: 1.2rem; font-weight: 500;'>
            CFTR variants are genetic changes that can affect the structure, processing, or
            function of the CFTR protein. Their effects are not always the same, even when
            variants occur within the same general region or share a similar consequence
            type. Understanding these differences is important for investigating how
            changes in the CFTR sequence may relate to protein function and potential
            clinical significance.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

N_PATH = Path(__file__).resolve().parent.parent / "images" / "bcb43178-c776-4fed-b8ee-5b9f36f8bfa7_removalai_preview.png"

left, center, right = st.columns([1, 3, 1])

with center:
    st.image(
        str(N_PATH),
        use_container_width=True
    )

st.markdown(
    """
    <div class="info-bubble">
        <p style='text-align: center; font-family: Fredoka, sans-serif; font-size: 1.2rem; font-weight: 500;'>
            The purpose of this project is to investigate patterns across CFTR variants by
            examining where variants occur in the protein, what types of consequences they
            have, how variants are distributed across protein regions, and how conserved
            the affected domains are. The Explorer brings these analyses together in an
            interactive interface so users can examine individual positions while also
            viewing broader patterns across the CFTR protein.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

N_PATH = Path(__file__).resolve().parent.parent / "images" / "bcb43178-c776-4fed-b8ee-5b9f36f8bfa7_removalai_preview.png"

left, center, right = st.columns([1, 3, 1])

with center:
    st.image(
        str(N_PATH),
        use_container_width=True
    )

st.markdown(
    """
    <div class="info-bubble">
        <p style='text-align: center; font-family: Fredoka, sans-serif; font-size: 1.2rem; font-weight: 500;'>
            The project also uses machine learning to predict the likely consequence of
            selected amino-acid substitutions. By comparing the model's predictions with
            recorded variant consequences and displaying its confidence, the Explorer
            demonstrates how computational methods can be applied to biological variant
            data. Together, these analyses provide a data-driven approach for exploring
            relationships between CFTR sequence variation, protein characteristics, and
            variant consequences.
        </p>
    </div>
    """,
    unsafe_allow_html=True 
)
    
st.markdown(
    "<h3 style='text-align: center;'>Variant Explorer</h3>",
    unsafe_allow_html=True
)

if "explored_position" not in st.session_state:
    st.session_state["explored_position"] = None

position_input = st.text_input(
    "Enter a CFTR amino-acid position",
    placeholder="Example: 125"
)

with st.expander("View positions with recorded variants"):
            st.write(sorted(valid_positions))

if st.button("Explore position"):

    st.session_state["explored_position"] = None

    if not position_input.strip().isdigit():
        st.error("Please enter a valid amino-acid position.")

    else:
        position = int(position_input)

        if position < 1 or position > 1481:
            st.error(
                "Please enter a CFTR amino-acid position between 1 and 1481. Only positions with recorded variants in the dataset can be explored! :)"
            )

        elif position not in valid_positions:
            st.error(
                "That position was not found in the CFTR dataset."
            )

        else:
            st.session_state["explored_position"] = position
    
if st.session_state["explored_position"] is not None:

    explored_position = int(st.session_state["explored_position"])

    if explored_position < 1 or explored_position > 1481:
        st.error(
            "Please enter a CFTR amino-acid position between 1 and 1481."
        )

    elif explored_position not in valid_positions:
        st.error(
            "That position was not found in the CFTR dataset."
        )

    else:
        position_info, variants = get_position_summary(explored_position)
        
        st.markdown(
            "<h1 style='text-align: center;'>Results</h1>",
            unsafe_allow_html=True
        )

        if explored_position == 1481:
            
            THE_PATH = Path(__file__).resolve().parent.parent / "images" / "0E11DECF-757B-4E64-ADBA-713D560B56A9.gif"

            left, center, right = st.columns([1, 3, 1])

            with center:
                st.image(
                    str(THE_PATH),
                    use_container_width=True
                )
                
            st.markdown(
                """
                <h3 style='text-align: center;'>
                    CFTR Position 1481
                </h3>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown(
                """
                <details class="position-1481-dropdown">
                    <summary>Special Case: Position 1481! (Click For Information About Position 1481)</summary>
                    <div class="position-1481-content">
                        <table class="position-1481-table">
                            <tr>
                                <th>Topic</th>
                                <th>Explanation</th>
                            </tr>
                            <tr>
                                <td>Why does position 1481 appear?</td>
                                <td>CFTR contains 1,480 amino acids. Position 1481 appears in this dataset because stop-loss variants alter the normal stop signal, allowing translation to continue beyond the usual protein endpoint.</td>
                            </tr>
                            <tr>
                                <td>Why is the domain "Other"?</td>
                                <td>Position 1481 is outside the canonical CFTR protein sequence, so it does not fall within any of the major CFTR domains defined in this analysis.</td>
                            </tr>
                            <tr>
                                <td>Why is conservation "N/A"?</td>
                                <td>Position 1481 is not a canonical amino-acid position in human CFTR, so it cannot be assigned a conservation score using the same position-based analysis as positions 1–1480.</td>
                            </tr>
                            <tr>
                                <td>Why are there no predictions?</td>
                                <td>Stop-loss variants were excluded from the machine-learning model because only a very small number were present in the dataset, which was insufficient to support reliable model training for that consequence class.</td>
                            </tr>
                        </table>
                    </div>
                </details>
                """,
                unsafe_allow_html=True
            )

            N_PATH = Path(__file__).resolve().parent.parent / "images" / "bcb43178-c776-4fed-b8ee-5b9f36f8bfa7_removalai_preview.png"

            left, center, right = st.columns([1, 3, 1])

            with center:
                st.image(
                    str(N_PATH),
                use_container_width=True
                )

            variants = variants_df[
                variants_df["Position"] == 1481
            ].copy()
                    
        else:
            B_PATH = Path(__file__).resolve().parent.parent / "images" / "B07F52FD-0104-4A8D-BD55-7B8E1BA7E386.gif"
                
            left, center, right = st.columns([1, 4 , 1])

            with center:
                st.image(
                    str(B_PATH),
                    use_container_width=True
                )
                
            st.markdown(
                f"""
                <h3 style='text-align: center;'>
                    CFTR Position {explored_position}
                </h3>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown(
                """
                <details class="position-1481-dropdown">
                    <summary>Why Are Some Variants Not Available For Prediction? (Click For Information)</summary>
                    <div class="position-1481-content">
                        <table class="position-1481-table">
                            <tr>
                                <th>Variant Type</th>
                                <th>Why Is It Not Available For Prediction?</th>
                            </tr>
            
                            <tr>
                                <td>Standard amino-acid substitutions</td>
                                <td>
                                    These variants <b>are available for prediction</b>. They replace one
                                    amino acid with another, such as K&gt;N or S&gt;A. The Random Forest
                                    was specifically trained to represent this one-to-one amino-acid
                                    change. Its features include the wild-type and mutated amino acids,
                                    changes in hydrophobicity, polarity, charge, and size, as well as
                                    evolutionary information from the sequence alignment.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Stop-gained variants (*) — 316</td>
                                <td>
                                    Stop-gained variants are represented by <b>*</b>, which means a
                                    premature stop codon rather than an amino acid. The reason these
                                    variants are not available is <b>not simply because there are too
                                    few of them</b>: there are 316 stop-gained variants in the dataset.
                                    The technical limitation is that the current model was designed
                                    around a one-to-one amino-acid substitution. For a substitution
                                    such as K&gt;N, the model can calculate changes in hydrophobicity,
                                    polarity, charge, and size between two amino acids. For K&gt;*,
                                    there is no amino-acid property profile for the stop symbol, so
                                    those same features cannot be calculated. Supporting stop-gained
                                    variants would therefore require a different feature representation
                                    and retraining the model.
                                </td>
                            </tr>
            
                            <tr>
                                <td>In-frame deletions — 52</td>
                                <td>
                                    In-frame deletions remove one or more amino acids rather than
                                    replacing one amino acid with another. The current model expects
                                    one <b>WildType</b> amino acid and one <b>MutatedType</b> amino acid
                                    so that their biochemical properties can be compared. A deletion
                                    does not provide that one-to-one relationship. There are also only
                                    52 in-frame deletion variants in the dataset, compared with 2,809
                                    missense variants. Supporting this class would require sequence-level
                                    features that explicitly describe the deleted residues and
                                    retraining the model.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Insertions / multi-amino-acid changes — 11</td>
                                <td>
                                    Insertions can introduce multiple amino acids rather than making
                                    one amino-acid substitution. For example, a value such as <b>LL</b>
                                    represents more than one residue and cannot be treated as a single
                                    amino acid when calculating hydrophobicity, polarity, charge, or
                                    size. The current model expects one WildType amino acid and one
                                    MutatedType amino acid. In addition, there are only <b>11 insertion
                                    variants</b> in the dataset, which provides very little data from
                                    which to learn an insertion-specific pattern. Supporting insertions
                                    would require a different sequence-level representation and
                                    substantially more training data.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Frameshifts — 459</td>
                                <td>
                                    Frameshift variants alter the reading frame of the sequence and can
                                    change every downstream codon. They therefore cannot be represented
                                    as a simple single-amino-acid substitution. Although there are
                                    <b>459 frameshift variants</b> in the dataset, the current model's
                                    features do not describe the downstream sequence changes caused by
                                    a frameshift. Including them would require sequence-level features
                                    specifically designed to represent changes in the reading frame,
                                    followed by retraining and reevaluation of the model.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Missing / "-" mutated amino-acid values — 13</td>
                                <td>
                                    A missing value or <b>-</b> does not identify a specific replacement
                                    amino acid. The current model needs a defined MutatedType in order
                                    to calculate the biochemical property changes used as model
                                    features. Without knowing what amino acid was introduced, the
                                    required features cannot be calculated consistently. These variants
                                    therefore cannot be passed through the same prediction pipeline
                                    without inventing biological information that is not present in
                                    the dataset.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Stop-loss variants — 3</td>
                                <td>
                                    Stop-loss variants were excluded from model training because there
                                    are only <b>3 examples</b> in the dataset. Three examples are not
                                    enough for a machine-learning model to learn a reliable consequence
                                    pattern or for the class to be meaningfully evaluated on independent
                                    test data. This is therefore a <b>training-data limitation</b>,
                                    rather than a statement that stop-loss variants are unimportant.
                                    Position 1481 is an example of a stop-loss position and is handled
                                    separately in the app.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Initiator codon variants — 1</td>
                                <td>
                                    There is only <b>1 initiator codon variant</b> in the dataset. A
                                    single example cannot provide enough information for a Random Forest
                                    to learn a reliable pattern for this consequence class or for its
                                    performance to be independently evaluated. It was therefore
                                    excluded from the model rather than allowing the model to learn
                                    from an effectively unsupported class.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Why not train one model on every variant type?</td>
                                <td>
                                    The limitation is both <b>technical and statistical</b>. The current
                                    feature engineering was designed for a single amino acid changing
                                    into another single amino acid. Stop codons, deletions, insertions,
                                    and frameshifts require different representations of the sequence
                                    change. At the same time, some consequence classes have very few
                                    examples: only 3 stop-loss variants, 1 initiator codon variant, and
                                    11 insertion variants are present. Simply adding these records to
                                    the existing model would not give the model the information needed
                                    to represent those biological changes and could produce unreliable
                                    predictions for rare classes.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Does "not available" mean these variants can never be predicted?</td>
                                <td>
                                    <b>No.</b> These variants are outside the scope of the current model,
                                    not inherently impossible to predict. A future model could use
                                    sequence-level features designed for insertions, deletions,
                                    frameshifts, stop-gained variants, and other complex changes.
                                    However, that would require appropriate feature engineering,
                                    substantially more representative training data for rare classes,
                                    and a new evaluation strategy. The current project intentionally
                                    limits predictions to variants that the model's feature design and
                                    training data can support.
                                </td>
                            </tr>
            
                        </table>
                    </div>
                </details>
                """,
                unsafe_allow_html=True
            )
            
            consequence_counts = (
                variants["Consequence"]
                .fillna("Missing")
                .value_counts()
            )
            
            def get_count(name):
                return consequence_counts.get(name, 0)
            
            st.markdown(
                f"""
                <details class="position-1481-dropdown">
                    <summary>Why Are Some Variants Not Available For Prediction? (Click For Information)</summary>
                    <div class="position-1481-content">
                        <table class="position-1481-table">
                            <tr>
                                <th>Variant Type</th>
                                <th>Why Is It Not Available For Prediction?</th>
                            </tr>
            
                            <tr>
                                <td>Standard amino-acid substitutions</td>
                                <td>
                                    These variants <b>are available for prediction</b>. They replace one
                                    amino acid with another, such as K&gt;N or S&gt;A. The Random Forest
                                    was specifically trained to represent this one-to-one amino-acid
                                    change using the wild-type and mutated amino acids, biochemical
                                    property changes, and evolutionary information.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Stop-gained variants (*) — {get_count("stop gained")}</td>
                                <td>
                                    Stop-gained variants are represented by <b>*</b>, which means a
                                    premature stop codon rather than an amino acid. There are
                                    <b>{get_count("stop gained")}</b> of these variants in the dataset,
                                    so rarity is not the primary reason they are excluded. The technical
                                    limitation is that the current model calculates hydrophobicity,
                                    polarity, charge, and size changes between two amino acids.
                                    A stop codon does not have those amino-acid properties, so a change
                                    such as K&gt;* cannot be represented using the same feature pipeline.
                                    Supporting stop-gained variants would require different features
                                    and retraining the model.
                                </td>
                            </tr>
            
                            <tr>
                                <td>In-frame deletions — {get_count("inframe deletion")}</td>
                                <td>
                                    In-frame deletions remove one or more amino acids instead of
                                    replacing one amino acid with another. The current model requires
                                    one WildType amino acid and one MutatedType amino acid so their
                                    biochemical properties can be compared. A deletion does not provide
                                    that one-to-one relationship. The dataset contains
                                    <b>{get_count("inframe deletion")}</b> in-frame deletion variants,
                                    but supporting them would still require sequence-level deletion
                                    features and retraining.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Insertions / multi-amino-acid changes — {get_count("insertion")}</td>
                                <td>
                                    Insertions can introduce multiple amino acids rather than making
                                    one amino-acid substitution. Values such as LL or KK therefore
                                    cannot be treated as a single amino acid when calculating
                                    biochemical property changes. There are only
                                    <b>{get_count("insertion")}</b> insertion variants in the dataset,
                                    so there is also very limited data for learning an
                                    insertion-specific pattern. Supporting this class would require
                                    a different sequence-level representation and more training data.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Frameshifts — {get_count("frameshift")}</td>
                                <td>
                                    Frameshift variants alter the reading frame and can change every
                                    downstream codon. They therefore cannot be represented as a simple
                                    single-amino-acid substitution. Although the dataset contains
                                    <b>{get_count("frameshift")}</b> frameshift variants, the current
                                    features do not describe the downstream sequence changes caused by
                                    a frameshift. Supporting them would require sequence-level features
                                    designed specifically for this type of mutation.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Missing / "-" mutated amino-acid values — {get_count("-")}</td>
                                <td>
                                    A missing value or <b>-</b> does not identify a specific replacement
                                    amino acid. The current model needs a defined MutatedType to
                                    calculate the biochemical property changes used as features.
                                    Without that information, the required features cannot be calculated
                                    consistently.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Stop-loss variants — {get_count("stop lost")}</td>
                                <td>
                                    Stop-loss variants were excluded from model training because the
                                    dataset contains only <b>{get_count("stop lost")}</b> examples.
                                    That is not enough data for a machine-learning model to learn a
                                    reliable consequence pattern or for the class to be meaningfully
                                    evaluated on independent test data. This is therefore a
                                    <b>training-data limitation</b>.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Initiator codon variants — {get_count("initiator codon variant")}</td>
                                <td>
                                    The dataset contains only
                                    <b>{get_count("initiator codon variant")}</b> initiator codon
                                    variant. A single example cannot provide enough information for
                                    the Random Forest to learn or independently evaluate a reliable
                                    pattern for this consequence class. It was therefore excluded
                                    from model training.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Why not train one model on every variant type?</td>
                                <td>
                                    The limitation is both <b>technical and statistical</b>. The current
                                    feature engineering was designed for a single amino acid changing
                                    into another single amino acid. Stop codons, deletions, insertions,
                                    and frameshifts require different representations of the sequence
                                    change. Some classes also contain very few examples. Simply adding
                                    these variants to the existing model would not give the model the
                                    appropriate biological features needed to represent them reliably.
                                </td>
                            </tr>
            
                            <tr>
                                <td>Does "not available" mean these variants can never be predicted?</td>
                                <td>
                                    <b>No.</b> These variants are outside the scope of the current model,
                                    not inherently impossible to predict. A future model could use
                                    sequence-level features designed for these variant types and would
                                    require appropriate training data and evaluation. The current project
                                    limits predictions to variants that the existing feature design and
                                    training data can support.
                                </td>
                            </tr>
            
                        </table>
                    </div>
                </details>
                """,
                unsafe_allow_html=True
            )
        if explored_position == 1481:

            stop_loss_count = int(
                (variants_df["Position"] == 1481).sum()
            )
        
            col1, col2, col3 = st.columns(3)
        
            with col1:
                glossary_metric(
                    "Domain",
                    "Other",
                    "Position 1481 is the stop-loss site immediately after the canonical 1,480-amino-acid CFTR sequence."
                )
        
            with col2:
                glossary_metric(
                    "Conservation",
                    "N/A",
                    "Conservation is not available because position 1481 is not an amino-acid position in canonical human CFTR."
                )
        
            with col3:
                glossary_metric(
                    "Variant count",
                    stop_loss_count,
                    "The number of recorded CFTR variants associated with position 1481 in the dataset."
                )
        
        elif explored_position in valid_positions:
        
            info = position_info.iloc[0]
        
            col1, col2, col3 = st.columns(3)
        
            with col1:
                glossary_metric(
                    "Domain",
                    info["CFTR_Domain"],
                    "A specific region of a protein that has a particular structure or function."
                )
        
            with col2:
                glossary_metric(
                    "Conservation",
                    f"{info['Conservation']:.3f}",
                    "A measure of how strongly this amino-acid position has been preserved across related proteins."
                )
        
            with col3:
                glossary_metric(
                    "Variant count",
                    int(info["Variant_Count"]),
                    "The number of recorded CFTR variants associated with this amino-acid position in the dataset."
                )
        
        if explored_position != 1481:
                
            st.markdown(
                "<h3 style='text-align: center;'>Machine Learning Prediction</h3>",
                unsafe_allow_html=True
            )

            with st.expander("What Random Forest Is Predicting"):
                st.write(
                    "The machine-learning model predicts the likely consequence of the "
                    "selected CFTR variant based on its amino-acid position and substitution. "
                    "The prediction is made for the specific variant you selected, rather than "
                    "for every variant recorded at that position."
                )

            

            prediction_variants = variants.copy()

            substitution_variants = prediction_variants[
                prediction_variants["MutatedType"].notna()
                & (prediction_variants["MutatedType"] != "*")
                & prediction_variants["MutatedType"].isin(
                    list("ACDEFGHIKLMNPQRSTVWY")
                )
            ].copy()
            
            if not substitution_variants.empty:

                substitution_variants["Variant"] = (
                    substitution_variants["WildType"].astype(str)
                    + ">"
                    + substitution_variants["MutatedType"].astype(str)
                )

                selected_variant_label = st.selectbox(
                    "Select a variant",
                    substitution_variants["Variant"].tolist()
                )

                selected_variant = substitution_variants[
                    substitution_variants["Variant"]
                    == selected_variant_label
                ].iloc[0]

                result = predict_consequence(
                    int(selected_variant["Position"]),
                    selected_variant["WildType"],
                    selected_variant["MutatedType"]
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Predicted consequence",
                    result["prediction"].title()
                )

                col2.metric(
                    "Recorded consequence",
                    selected_variant["Consequence"].title()
                )
                
                col1, col2 = st.columns(2)
            
                with col1:
                    st.metric(
                        "Model accuracy",
                        f"{model_metrics['accuracy']:.1%}"
                    )
            
                with col2:
                    st.metric(
                        "Macro F1",
                        f"{model_metrics['macro_f1']:.1%}"
                    )
    
            if result["confidence"] is not None:

                    col3.metric(
                        "Model confidence",
                        f"{result['confidence']:.2%}"
                    )
                    
                    if explored_position != 1481:
                        with st.expander("What Model Confidence Means"):
                            st.write(
                                "The confidence score indicates "
                                "how strongly the model favors its prediction. Because the model was trained "
                                "on existing CFTR variant data, its predictions should be interpreted as "
                                "computational estimates rather than definitive evidence of biological or "
                                "clinical effect." 
                            )

                    if result["prediction"] == selected_variant["Consequence"]:

                        st.success(
                            "The model prediction matches the recorded consequence."
                        )

                    else:
                        st.warning(
                            "The model prediction differs from the recorded consequence."
                        )

            else:
                st.info(
                    "No standard amino-acid substitutions are available "
                    "for prediction at this position."
                )
                

                N_PATH = Path(__file__).resolve().parent.parent / "images" / "bcb43178-c776-4fed-b8ee-5b9f36f8bfa7_removalai_preview.png"

                left, center, right = st.columns([1, 3, 1])

                with center:
                    st.image(
                        str(N_PATH),
                        use_container_width=True
                    )
                    
        st.markdown(
            """
            <h3 class='glossary-heading' style='text-align: center;'>
                <details class="position-1481-dropdown">
                    <summary>CFTR Domain Conservation</summary>
                    <div class="glossary-definition">
                        The average evolutionary conservation of amino-acid positions within each major CFTR domain.
                    </div>
                </details>
            </h3>
            """,
            unsafe_allow_html=True
        )

        domain_conservation = {
            "NBD1": 0.820016,
            "NBD2": 0.790831,
            "Other": 0.692784,
            "R domain": 0.640287,
            "TMD1": 0.767632,
            "TMD2": 0.729488,
        }

        domain_chart_data = pd.DataFrame(
            list(domain_conservation.items()),
            columns=["Domain", "Conservation"]
        )

        domain_chart = (
            alt.Chart(domain_chart_data)
            .mark_bar(
                color="#ffc4e7",
                cornerRadiusTopLeft=6,
                cornerRadiusTopRight=6
            )
            .encode(
                x=alt.X(
                    "Domain:N",
                    title=None
                ),
                y=alt.Y(
                    "Conservation:Q",
                    title="Average conservation"
                ),
                tooltip=[
                    alt.Tooltip(
                        "Domain:N",
                        title="Domain"
                    ),
                    alt.Tooltip(
                        "Conservation:Q",
                        title="Conservation",
                        format=".3f"
                    )
                ]
            )
        )

        st.altair_chart(
            domain_chart,
            use_container_width=True
        )
        
        with st.expander("Don't Understand Unfamiliar Terms? Click Me! (Explanations Are Simplifed For General-Understanding)"):
            st.markdown("""
            **NBD1 and NBD2:** Nucleotide-binding domains. These are two parts of CFTR that interact with ATP, a molecule that provides energy for many processes in cells. ATP helps CFTR control when its channel is open or closed.
        
            **R domain:** The regulatory domain. This part helps control the activity of CFTR, including whether the channel can open.
        
            **TMD1 and TMD2:** Transmembrane domains. These are parts of CFTR that are located within the cell membrane, the thin outer barrier of a cell. Together, they form the channel that allows chloride ions to move across the membrane.
        
            **Other:** Positions that are outside the five major CFTR domains included in this analysis.
        
            **Average conservation:** The average conservation score of all the amino-acid positions within a domain. A higher score means that these positions tend to remain more similar across related proteins, suggesting that they may be important for the protein's structure or function.
        
            This chart shows a **global view of CFTR conservation** rather than the conservation of the specific position entered above. Conservation is calculated for individual amino-acid positions by comparing related CFTR proteins. The scores are then grouped by domain and averaged, allowing us to compare how strongly different parts of CFTR have been preserved over evolutionary time.
            """)

        B_PATH = Path(__file__).resolve().parent.parent / "images" / "B07F52FD-0104-4A8D-BD55-7B8E1BA7E386.gif"
    
        left, center, right = st.columns([1, 4, 1])

        with center:
            st.image(
                str(B_PATH),
                use_container_width=True
            )
    
        st.markdown(
            """
            <h3 class='glossary-heading' style='text-align: center;'>
                <details class="position-1481-dropdown">
                    <summary>Variant Distribution by Protein Region</summary>
                    <div class="glossary-definition">
                        The distribution of recorded CFTR variants across the major protein regions.
                    </div>
                </details>
            </h3>
            """,
            unsafe_allow_html=True
        )
    
        region_counts = variants_df["Region"].value_counts()
    
        region_chart_data = (
            region_counts
            .rename_axis("Region")
            .reset_index(name="Variant_Count")
        )
    
        region_chart = (
            alt.Chart(region_chart_data)
            .mark_bar(
                color="#ffc4e7",
                cornerRadiusTopLeft=6,
                cornerRadiusTopRight=6
            )
            .encode(
                x=alt.X(
                    "Region:N",
                    title=None
                ),
                y=alt.Y(
                    "Variant_Count:Q",
                    title="Variant count"
                ),
                tooltip=[
                    alt.Tooltip(
                        "Region:N",
                        title="Region"
                    ),
                    alt.Tooltip(
                        "Variant_Count:Q",
                        title="Variants"
        
                    )
                ]
            )
        )
    
        st.altair_chart(
            region_chart,
            use_container_width=True
        )
        
        with st.expander("Don't Understand Unfamiliar Terms? Click Me! (Explanations Are Simplifed For General-Understanding)"):
            st.markdown("""
            **N-terminal:** The beginning of the protein sequence.
        
            **Middle:** The central portion of the protein sequence.
        
            **C-terminal:** The end of the protein sequence.
        
            Knowing where variants occur within a protein is important because different parts of a protein can have different structures and functions. Identifying whether variants are concentrated near the beginning, middle, or end of CFTR can help researchers see patterns in where changes occur and investigate whether certain regions may be more affected than others.
            """)
            
    
        B_PATH = Path(__file__).resolve().parent.parent / "images" / "B07F52FD-0104-4A8D-BD55-7B8E1BA7E386.gif"
    
        left, center, right = st.columns([1, 4, 1])

        with center:
            st.image(
                str(B_PATH),
                use_container_width=True
            )
    
        st.markdown(
            """
            <h3 class='glossary-heading' style='text-align: center;'>
                <details class="position-1481-dropdown">
                    <summary>Variant Consequences</summary>
                    <div class="glossary-definition">
                        The distribution of recorded CFTR variants by the type of change they produce in the protein.
                    </div>
                </details>
            </h3>
            """,
            unsafe_allow_html=True
        )
    
        consequence_summary = get_consequence_summary(
            explored_position
        )
    
        if consequence_summary:
            consequence_chart_data = (
                pd.Series(consequence_summary)
                .rename_axis("Consequence")
                .reset_index(name="Count")
            )
    
            consequence_chart = (
                alt.Chart(consequence_chart_data)
                .mark_bar(
                    color="#ffc4e7",
                    cornerRadiusTopLeft=6,
                    cornerRadiusTopRight=6
                )
                .encode(
                    x=alt.X(
                        "Consequence:N",
                        title=None
                    ),
                    y=alt.Y(
                        "Count:Q",
                        title="Variant count"
                    ),
                    tooltip=[
                        alt.Tooltip(
                            "Consequence:N",
                            title="Consequence"
                        ),
                        alt.Tooltip(
                            "Count:Q",
                            title="Variants"
                        )
                    ]
                )
            )
    
            st.altair_chart(
                consequence_chart,
                use_container_width=True
            )
            
            with st.expander("Don't Understand Unfamiliar Terms? Click Me! (Explanations Are Simplifed For General-Understanding)"):
                st.markdown("""
                **Variant consequence:** A description of how a genetic change affects the CFTR protein. Different types of changes can affect the protein in different ways, such as changing an amino acid, removing part of the protein, or causing the protein to end earlier than expected.
            
                **Missense:** A variant that changes one amino acid in the protein to a different amino acid. Depending on where the change occurs, it may affect how CFTR is structured or how well it functions.
            
                **Frameshift:** A change that shifts the way the genetic sequence is read. This can change many of the amino acids that follow the variant and may result in a protein that does not function normally.
            
                **Frame deletion:** A deletion that removes part of the genetic sequence while preserving the reading frame. This can remove one or more amino acids from the CFTR protein, and its effects depend on which part of the protein is removed.
            
                **Stop gained:** A variant that introduces an early stop signal into the genetic sequence. This can cause the cell to produce a shorter CFTR protein.
            
                **Stop loss:** A variant that removes the normal stop signal. This can cause the protein-making process to continue beyond its usual endpoint, resulting in extra amino acids being added to the protein.
            
                **Initiator codon variant:** A variant that changes the genetic signal that tells the cell where to begin making the CFTR protein. A change to this signal can interfere with the production of the protein.
            
                **Gap (-):** A dash means that no amino acid is present at that position in the sequence.
            
                **Sequence-level descriptions:** Some variants are represented by the amino-acid changes themselves rather than by a consequence label such as "missense" or "frameshift." These entries show the specific amino-acid sequence associated with the variant.
            
                This chart shows the distribution of recorded variant consequences in the CFTR dataset. Looking at these categories helps show which types of genetic changes are most frequently represented in the dataset.
                """)
                
            if variants is not None and not variants.empty:
                st.markdown(
                    """
                    <h3 class='glossary-heading' style='text-align: center;'>
                        <details class="position-1481-dropdown">
                            <summary>Variants at This Position</summary>
                            <div class="glossary-definition">
                                A list of recorded CFTR variants found at the amino-acid position you entered.
                            </div>
                        </details>
                    </h3>
                    """,
                    unsafe_allow_html=True
                )
            
                st.dataframe(variants)
            
            with st.expander("Don't Understand Unfamiliar Terms? Click Me! (Explanations Are Simplifed For General-Understanding)"):
                st.markdown("""
                **Position:** The location of the variant within the CFTR protein.
            
                **Wild type:** The amino acid normally found at this position in the reference human CFTR protein.
            
                **Mutated type:** The amino acid or value recorded at this position for the variant. If it says "None," the variant does not specify a replacement amino acid at that position.
            
                **Consequence:** A description of how the genetic change affects the CFTR protein.
            
                **Region:** The general part of the CFTR protein where the variant is located, such as the N-terminal, Middle, or C-terminal region.
            
                This table lists the recorded CFTR variants found at the amino-acid position you entered. Each row represents a variant in the dataset and provides information about the change and where it occurs in the CFTR protein.
                """)
            
if st.session_state.get("explored_position") in valid_positions:
    
    N_PATH = Path(__file__).resolve().parent.parent / "images" / "bcb43178-c776-4fed-b8ee-5b9f36f8bfa7_removalai_preview.png"

    left, center, right = st.columns([1, 3, 1])

    with center:
        st.image(
            str(N_PATH),
            use_container_width=True
        )
    
    st.markdown("""
<div class="info-bubble">
<h3>What The Data Suggests (Overall)</h3>

<p>
CFTR domains differ in their average conservation, with NBD1 being the most conserved domain in this dataset and the R domain having the lowest average conservation. 
Variant distribution also differs across the N-terminal, Middle, and C-terminal regions, and multiple consequence types can occur at the same amino-acid position. 
The machine-learning component predicts the likely consequence of a selected amino-acid substitution based on patterns learned from the CFTR variant dataset, 
allowing the prediction to be compared with the recorded consequence. These results identify patterns and computational predictions within the dataset but do not 
by themselves establish the biological or clinical effect of an individual variant.
</div>
""", unsafe_allow_html=True)

    DON_PATH = Path(__file__).resolve().parent.parent / "images" / "77C31030-2369-452B-B746-B1636E691D0B.gif"

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.image(
            str(DON_PATH),
            use_container_width=True
        )

    st.markdown("""
<div class="info-bubble">
<h3>Why This Matters</h3>

<p>
CFTR helps regulate chloride and bicarbonate transport across epithelial tissues,
making it important for the normal function of several organs. Changes in CFTR
can affect how the protein folds, reaches the cell surface, or functions as an
ion channel, contributing to the effects associated with cystic fibrosis and
other CFTR-related conditions. Because different variants can affect CFTR in
different ways, identifying where a variant occurs and what type of change it
produces can provide important information about its potential functional
significance.
</p>

<p>
This project examines CFTR variants from multiple perspectives by investigating
where variants occur across the protein, what consequence types are associated
with those positions, which protein regions contain greater numbers of variants,
and how conserved different CFTR domains are. By comparing variant locations
with regional and domain-level characteristics, the Explorer provides an
interactive way to investigate patterns between sequence variation and
characteristics of the affected protein regions.
</p>

<p>
The project also incorporates machine learning to analyze individual
amino-acid substitutions. The model was trained using CFTR variant data and
predicts the likely consequence of a selected substitution. Users can compare
the model's prediction with the recorded consequence of that variant while
also viewing the model's confidence, demonstrating how patterns within existing
biological data can be used for computational variant classification.
</p>

<p>
Together, these analyses connect sequence-level variation, protein-region
characteristics, conservation, variant consequences, and machine-learning
prediction in one interactive tool. The goal is to identify patterns that may
help explain why variants occurring in different parts of CFTR can have
different functional consequences. Importantly, these patterns and
machine-learning predictions represent computational analyses of the available
dataset and should not be interpreted as definitive evidence of an individual
variant's biological or clinical effect.
</p>
</div>
""", unsafe_allow_html=True)

    DON_PATH = Path(__file__).resolve().parent.parent / "images" / "77C31030-2369-452B-B746-B1636E691D0B.gif"

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.image(
            str(DON_PATH),
            use_container_width=True
        )

    st.markdown("""
<div class="info-bubble">
<h3>Understanding Variant Consequences</h3>

<p>
CFTR plays an important role in regulating the movement of chloride and
bicarbonate ions across epithelial tissues. Variants that reduce or disrupt
CFTR function can alter this transport and affect the movement of water and
ions across tissues. The resulting effects can involve multiple organs,
depending on the amount of CFTR function that remains and the specific
biological properties of the variant.
</p>

<p>
In the lungs, substantially impaired CFTR function can contribute to changes
in airway surface liquid and mucus clearance, which can increase the risk of
airway obstruction, inflammation, and recurrent respiratory infections. In
the digestive system, CFTR dysfunction can affect the pancreas and
gastrointestinal tract and may contribute to difficulties with digestion and
nutrient absorption. The severity and combination of these effects can vary
between individuals and between different CFTR variants.
</p>

<p>
These clinical effects are not determined by variant consequence type alone.
Different variants can affect CFTR through different molecular mechanisms and
can leave different amounts of residual protein function. As a result,
variants with the same general consequence category can have different
biological effects and may be associated with different clinical outcomes.
This is why examining variant location, consequence, conservation, and
protein-region characteristics together can provide more context than
considering consequence type alone.
</p>
</div>
""", unsafe_allow_html=True)

    DON_PATH = Path(__file__).resolve().parent.parent / "images" / "77C31030-2369-452B-B746-B1636E691D0B.gif"

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.image(
            str(DON_PATH),
            use_container_width=True
        )

    st.markdown("""
<div class="info-bubble">
<h3>From Variant to Clinical Effect</h3>

<p>
When a CFTR variant substantially reduces CFTR function, the effects can
extend beyond the protein itself. CFTR helps regulate chloride and bicarbonate
transport across epithelial tissues. Reduced CFTR activity can disrupt the
movement of ions and water, contributing to abnormal secretions in several
organs.
</p>

<p>
In the lungs, impaired CFTR function can contribute to thick, difficult-to-clear
mucus, airway inflammation, recurrent respiratory infections, and progressive
loss of lung function. In the digestive system, CFTR dysfunction can affect
the pancreas and intestines, contributing to problems with digestion and
nutrient absorption.
</p>

<p>
These clinical effects are not determined by consequence type alone.
Different variants can leave different amounts of CFTR function, so variants
with the same general consequence category can have different biological
and clinical effects.
</p>

</div>
""", unsafe_allow_html=True)
