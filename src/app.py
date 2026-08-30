import streamlit as st
import pandas as pd
import altair as alt
from data_loader import load_data
from pathlib import Path
from variant_explorer import (
    get_position_summary,
    get_consequence_summary,
    predict_consequence
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

.center-image {
    display: flex;
    justify-content: center;
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

GIF_PATH = Path(__file__).resolve().parent.parent / "images" / "8D83949E-9C79-479B-BD57-BA4F6ED95A0A.gif"

st.markdown('<div class="center-image">', unsafe_allow_html=True)

st.image(
    str(GIF_PATH),
    width=1000
)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    "<h3 style='text-align: center;'>Research Question</h3>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='font-family: Fredoka, sans-serif; font-size: 1.2rem; font-weight: 500;''>"
    "Where do CFTR variants occur across the protein, what types of variants "
    "occur at those positions, and what characteristics of the affected protein "
    "regions might help explain their different effects on CFTR function?"
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
        
        N_PATH = Path(__file__).resolve().parent.parent / "images" / "bcb43178-c776-4fed-b8ee-5b9f36f8bfa7_removalai_preview.png"
        
        st.image(
            str(N_PATH),
            use_container_width=True
        )
        
        st.markdown(
            "<h1 style='text-align: center;'>Results</h1>",
            unsafe_allow_html=True
        )

        if explored_position == 1481:

            st.subheader("CFTR Position 1481")

            st.info(
                "CFTR contains 1,480 amino acids. Position 1481 appears in this "
                "dataset because stop-loss variants alter the normal stop signal, "
                "allowing translation to continue beyond the usual protein endpoint."
            )
            
            THE_PATH = Path(__file__).resolve().parent.parent / "images" / "0E11DECF-757B-4E64-ADBA-713D560B56A9.gif"

            st.image(
                str(THE_PATH),
                use_container_width=True
            )

            st.info(
                "Stop-loss variants were excluded from the machine-learning model "
                "because only a very small number of stop-loss variants were present "
                "in the dataset, which was insufficient to support reliable model "
                "training for that consequence class."
            )

            variants = variants_df[
                variants_df["Position"] == 1481
            ].copy()

            col1, col2, col3 = st.columns(3)

            col1.metric("Domain", "NaN")
            col2.metric("Conservation", "NaN")
            col3.metric("Variant count", len(variants))

        else:

            st.subheader(f"CFTR Position {explored_position}")

            if position_info is not None and not position_info.empty:

                info = position_info.iloc[0]

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Domain",
                    info["CFTR_Domain"]
                )

                col2.metric(
                    "Conservation",
                    f"{info['Conservation']:.3f}"
                )

                col3.metric(
                    "Variant count",
                    int(info["Variant_Count"])
                )
                
                B_PATH = Path(__file__).resolve().parent.parent / "images" / "B07F52FD-0104-4A8D-BD55-7B8E1BA7E386.gif"
                
                st.image(
                    str(B_PATH),
                    use_container_width=True
                )
  
        if explored_position != 1481:

                st.markdown(
                    "<h3 style='text-align: center;'>Machine Learning Prediction</h3>",
                    unsafe_allow_html=True
                )

                st.info(
                    "The machine-learning model predicts the likely consequence of the "
                    "selected CFTR variant based on its amino-acid position and substitution. "
                    "The prediction is made for the specific variant you selected, rather than "
                    "for every variant recorded at that position."
                )
                
                N_PATH = Path(__file__).resolve().parent.parent / "images" / "bcb43178-c776-4fed-b8ee-5b9f36f8bfa7_removalai_preview.png"

                st.image(
                    str(N_PATH),
                    use_container_width=True
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
                        "Predicted value",
                        result["prediction"].title()
                    )

                    col2.metric(
                        "Actual",
                        selected_variant["Consequence"].title()
                    )

                    if result["confidence"] is not None:

                        col3.metric(
                            "Model confidence",
                            f"{result['confidence']:.2%}"
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

                st.image(
                    str(N_PATH),
                    use_container_width=True
                )
                    
                st.info(
                    "The confidence score indicates "
                    "how strongly the model favors its prediction. Because the model was trained "
                    "on existing CFTR variant data, its predictions should be interpreted as "
                    "computational estimates rather than definitive evidence of biological or "
                    "clinical effect." 
                )

                B_PATH = Path(__file__).resolve().parent.parent / "images" / "B07F52FD-0104-4A8D-BD55-7B8E1BA7E386.gif"

                st.image(
                    str(B_PATH),
                    use_container_width=True
                )
        
        if variants is not None and not variants.empty:

            st.markdown(
                "<h3 style='text-align: center;'>Variants At This Position</h3>",
                unsafe_allow_html=True
            )
            
            st.dataframe(variants)

        B_PATH = Path(__file__).resolve().parent.parent / "images" / "B07F52FD-0104-4A8D-BD55-7B8E1BA7E386.gif"

        st.image(
            str(B_PATH),
            use_container_width=True
        )
                    
        st.markdown(
            "<h3 style='text-align: center;'>CFTR Domain Conservation</h3>",
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

        B_PATH = Path(__file__).resolve().parent.parent / "images" / "B07F52FD-0104-4A8D-BD55-7B8E1BA7E386.gif"
    
        st.image(
            str(B_PATH),
            use_container_width=True
        )
    
        st.markdown(
            "<h3 style='text-align: center;'>Variant Distribution by Protein Region</h3>",
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
    
        B_PATH = Path(__file__).resolve().parent.parent / "images" / "B07F52FD-0104-4A8D-BD55-7B8E1BA7E386.gif"
    
        st.image(
            str(B_PATH),
            use_container_width=True
        )
    
        st.markdown(
            "<h3 style='text-align: center;'>Variant Consequences</h3>",
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
            
if st.session_state.get("explored_position") in valid_positions:
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
