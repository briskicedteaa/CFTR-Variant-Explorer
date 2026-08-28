import streamlit as st
import pandas as pd
import altair as alt
import py3Dmol
from data_loader import load_data
from pathlib import Path

from structure_prediction import (
    run_structure_prediction,
    create_mutated_sequence,
)

def display_structure(pdb_path, color_mode="confidence"):
    """Create an interactive 3D viewer for a predicted protein structure."""

    view = py3Dmol.view(
        width=900,
        height=600
    )

    with open(pdb_path, "r") as f:
        pdb_data = f.read()

    view.addModel(pdb_data, "pdb")

    if color_mode == "confidence":
        view.setStyle({
            "cartoon": {
                "colorscheme": {
                    "prop": "b",
                    "gradient": "roygb",
                    "min": 50,
                    "max": 90
                }
            }
        })

    elif color_mode == "rainbow":
        view.setStyle({
            "cartoon": {
                "color": "spectrum"
            }
        })

    view.zoomTo()

    return view

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
</style>
""", unsafe_allow_html=True)

from variant_explorer import (
    get_position_summary,
    get_consequence_summary
)

position_df, variants_df = load_data()

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
    "Click “Explore Position” to search."
    "</p>",
    unsafe_allow_html=True
)

GIF_PATH = Path(__file__).resolve().parent.parent / "images" / "8D83949E-9C79-479B-BD57-BA4F6ED95A0A.gif"

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.image(
        str(GIF_PATH),
        use_container_width=True
    )

st.markdown(
    "<h3 style='text-align: center;'>Research Question</h3>",
    unsafe_allow_html=True
)

IMG1_PATH = Path(__file__).resolve().parent.parent / "images" / "0E11DECF-757B-4E64-ADBA-713D560B56A9.gif"

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.image(
        str(IMG1_PATH),
        use_container_width=True
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
            CFTR variants are responsible for the underlying genetic changes associated with
            cystic fibrosis and other CFTR-related conditions, but their effects are not always
            the same. Differences in CFTR function can contribute to major clinical challenges,
            including persistent respiratory symptoms, recurrent lung infections, digestive and
            nutritional complications, and the long-term progression of disease. Because individual
            variants can disrupt CFTR function in different ways, determining how a specific variant
            affects the protein is an important part of understanding its potential clinical significance.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

N_PATH = Path(__file__).resolve().parent.parent / "images" / "Untitled16_20260826211636.png"

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(
        str(N_PATH),
        use_container_width=True
    )

st.markdown(
    """
    <div class="info-bubble">
        <p style='text-align: center; font-family: Fredoka, sans-serif; font-size: 1.2rem; font-weight: 500;'>
            The purpose of this project is to investigate the molecular patterns that may help explain
            differences between CFTR variants and their potential effects on health. By examining where
            variants occur, what types of changes they produce, and what characteristics define the
            affected regions of the CFTR protein, the Explorer provides an interactive way to connect
            genetic variation with protein function and its broader clinical relevance. This approach
            can help make complex CFTR variant data more accessible for exploring why different genetic
            changes may contribute to different outcomes for patients.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align: center;'>Variant Explorer</h3>",
    unsafe_allow_html=True
)

position = st.number_input(
    "Enter a CFTR amino-acid position",
    min_value=1,
    max_value=1481,
    step=1
)

with st.expander("View positions with recorded variants"):
            st.write(sorted(valid_positions))

if st.button("Explore position"):
    st.session_state["explored_position"] = position

    position_info, variants = get_position_summary(position)

    st.title("Results")

    if position_info is None and position not in valid_positions:
        st.error("That position was not found in the CFTR dataset.")

    elif position_info is None and position == 1481:
        st.subheader("CFTR Position 1481")

        st.info(
            "CFTR contains 1,480 amino acids. Position 1481 appears in this "
            "dataset because stop-loss variants alter the normal stop signal, "
            "allowing translation to continue beyond the usual protein endpoint."
        )

        variants = variants_df[variants_df["Position"] == 1481]

        col1, col2, col3 = st.columns(3)
        col1.metric("Domain", "NaN")
        col2.metric("Conservation", "NaN")
        col3.metric("Variant count", len(variants))

    elif position_info is not None and position in valid_positions:
        st.subheader(f"CFTR Position {position}")

        info = position_info.iloc[0]

        col1, col2, col3 = st.columns(3)
        col1.metric("Domain", info["CFTR_Domain"])
        col2.metric("Conservation", f"{info['Conservation']:.3f}")
        col3.metric("Variant count", int(info["Variant_Count"]))

    if variants is None or variants.empty:
        st.info("No recorded variants were found at this position.")

    else:
        st.subheader("Variants at this position")
        st.dataframe(variants)

        if variants is not None and not variants.empty:
            st.subheader("3D Protein Structure")

            selected_variant = variants.iloc[0]

            if (
                pd.notna(selected_variant["WildType"])
                and pd.notna(selected_variant["MutatedType"])
                and len(str(selected_variant["WildType"])) == 1
                and len(str(selected_variant["MutatedType"])) == 1
            ):
                mutated_sequence = create_mutated_sequence(
                    human_sequence=human_sequence,
                    position=int(selected_variant["Position"]),
                    wild_type=selected_variant["WildType"],
                    mutated_type=selected_variant["MutatedType"],
                )

                if st.button("Predict 3D Structure"):
                    with st.spinner(
                        "Predicting mutated CFTR structure..."
                    ):
                        results = run_structure_prediction(
                            mutated_sequence,
                            jobname=(
                                f"CFTR_position_"
                                f"{selected_variant['Position']}_"
                                f"{selected_variant['WildType']}"
                                f"{selected_variant['MutatedType']}"
                            ),
                        )

                    output_dir = (
                        Path(__file__).resolve().parent.parent
                        / "structure_results"
                        / (
                            f"CFTR_position_"
                            f"{selected_variant['Position']}_"
                            f"{selected_variant['WildType']}"
                            f"{selected_variant['MutatedType']}"
                        )
                    )

                    
                    pdb_files = list(output_dir.glob("*.pdb"))

                    if pdb_files:
                        pdb_path = pdb_files[0]

                    if pdb_path:
                        color_mode = st.selectbox(
                            "Structure coloring",
                            ["confidence", "rainbow"]
                        )

                        viewer = display_structure(
                            pdb_path,
                            color_mode=color_mode
                        )

                        st.components.v1.html(
                            viewer._make_html(),
                            height=600
                        )

                    else:
                        st.error(
                            "The structure prediction completed, "
                            "but no PDB structure was found."
                        )

    if position in valid_positions and position != 1481:
        st.subheader("CFTR Domain Conservation")

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
                x=alt.X("Domain:N", title=None),
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

        st.subheader("Variant Distribution by Protein Region")

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
                x=alt.X("Region:N", title=None),
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

        st.subheader("Variant consequences")

        consequence_summary = get_consequence_summary(position)

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
CFTR domains differ in their average conservation.
NBD1 is the most conserved domain in this dataset, while the R domain
has the lowest average conservation. Variant distribution also differs
across the N-terminal, Middle, and C-terminal regions.
</p>
</div>
""", unsafe_allow_html=True)


    DON_PATH = Path(__file__).resolve().parent.parent / "images" / "77C31030-2369-452B-B746-B1636E691D0B.gif"

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(
            str(DON_PATH),
            use_container_width=True
        )


    st.markdown("""
<div class="info-bubble">
<h3>Why This Matters</h3>

<p>
CFTR helps regulate chloride and bicarbonate transport across
epithelial tissues. Changes that substantially reduce CFTR function
can affect several organs and contribute to the manifestations
associated with cystic fibrosis.
</p>

<p>
By examining where variants occur, what types of changes they represent,
and how conserved the affected regions are, this project helps investigate
why variants in different parts of CFTR may have different functional
consequences. These patterns can also help identify regions of the protein
that may be particularly important for CFTR function.
</p>

<p>
Importantly, this analysis identifies patterns and possible relationships
rather than proving that a particular variant causes a specific clinical outcome.
</p>

</div>
""", unsafe_allow_html=True)


    DON_PATH = Path(__file__).resolve().parent.parent / "images" / "77C31030-2369-452B-B746-B1636E691D0B.gif"

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(
            str(DON_PATH),
            use_container_width=True
        )


    st.markdown("""
<div class="info-bubble">
<h3>Understanding Variant Consequences</h3>

<p>
A variant consequence describes what a genetic change does to the
CFTR sequence or protein. The consequence type alone does not determine
whether a variant is harmful. Its effect depends on the specific change,
where it occurs, and how much functional CFTR remains.
</p>

<p>
Missense variants replace one amino acid with another. Depending on the
location and properties of the substituted amino acid, this can have little
effect or can interfere with CFTR folding, stability, trafficking, or channel
activity.
</p>

<p>
Frameshift variants result from insertions or deletions that change the
reading frame. They can alter the downstream protein sequence and may
introduce a premature stop signal, often resulting in substantially reduced
CFTR function.
</p>

<p>
Inframe deletions remove one or more amino acids without shifting the
reading frame. Their effects depend strongly on which amino acids and
structural regions are removed.
</p>

<p>
Synonymous, sometimes called silent, variants do not change the encoded
amino acid. They are often less disruptive to the protein sequence, but
some can still affect RNA processing or splicing.
</p>

<p>
Nonsense or stop-gained variants introduce a premature stop signal.
This can produce a shortened protein or cause the cell to destroy the
altered RNA before a functional protein is produced.
</p>

<p>
Stop-loss variants alter the normal stop signal at the end of the CFTR
coding sequence. Instead of stopping at the usual endpoint, protein
production can continue beyond the normal 1,480-amino-acid sequence,
producing an altered protein with additional amino acids at its end.
</p>

<p>
This type of variant is represented in this dataset at position 1481.
These variants are recorded as stop-loss changes, meaning that the normal
CFTR stop signal has been altered. Position 1481 therefore does not mean
that normal CFTR is 1,481 amino acids long; rather, it reflects a variant
that can extend translation beyond the usual protein endpoint.
</p>

<p>
Splice-site variants can interfere with the normal processing of CFTR RNA.
This may result in abnormal transcripts and reduced production of correctly
functioning CFTR protein.
</p>

</div>
""", unsafe_allow_html=True)


    DON_PATH = Path(__file__).resolve().parent.parent / "images" / "77C31030-2369-452B-B746-B1636E691D0B.gif"

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
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