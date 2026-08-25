import streamlit as st
import pandas as pd
import altair as alt
from data_loader import load_data

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600&family=Quicksand:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Quicksand', sans-serif;
}

h1, h2, h3 {
    font-family: 'Fredoka', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

from variant_explorer import (
    get_position_summary,
    get_consequence_summary
)

position_df, variants_df = load_data()

st.title("CFTR Variant Explorer")
st.write(
    "Explore CFTR variant locations, consequences, conservation, "
    "and protein-region characteristics."
)

st.subheader("Research Question")

st.write(
    "Where do CFTR variants occur across the protein, what types of variants "
    "occur at those positions, and what characteristics of the affected protein "
    "regions might help explain their different effects on CFTR function?"
)

position = st.number_input(
    "Enter a CFTR amino-acid position",
    min_value=1,
    step=1
)

if st.button("Explore position"):
    position_info, variants = get_position_summary(position)

    if position_info is None:
        st.error("That position was not found in the CFTR dataset.")
    else:
        st.subheader(f"CFTR Position {position}")
        
        info = position_info.iloc[0]
        col1, col2, col3 = st.columns(3)
        col1.metric("Domain", info["CFTR_Domain"])
        col2.metric("Conservation", f"{info['Conservation']:.3f}")
        col3.metric("Variant count", int(info["Variant_Count"]))

        if variants.empty:
            st.info("No recorded variants were found at this position.")
        else:
            st.subheader("Variants at this position")
            st.dataframe(variants)

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
                    x=alt.X("Consequence:N", title=None),
                    y=alt.Y("Count:Q", title="Variant count"),
                    tooltip=[
                        alt.Tooltip("Consequence:N", title="Consequence"),
                        alt.Tooltip("Count:Q", title="Variants")
                    ]
                )
            )
    
        
                st.altair_chart(
                    consequence_chart, 
                    use_container_width=True
                )
            
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
        y=alt.Y("Conservation:Q", title="Average conservation"),
        tooltip=[
            alt.Tooltip("Domain:N", title="Domain"),
            alt.Tooltip("Conservation:Q", title="Conservation", format=".3f")
        ]
    )
)

st.altair_chart(domain_chart, use_container_width=True)

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
        y=alt.Y("Variant_Count:Q", title="Variant count"),
        tooltip=[
            alt.Tooltip("Region:N", title="Region"),
            alt.Tooltip("Variant_Count:Q", title="Variants")
        ]
    )
)

st.altair_chart(region_chart, use_container_width=True)

st.subheader("What the data suggests")

st.subheader("What the data suggests")

st.write(
    "CFTR domains differ in their average conservation. "
    "NBD1 is the most conserved domain in this dataset, while the R domain "
    "has the lowest average conservation. Variant distribution also differs "
    "across the N-terminal, Middle, and C-terminal regions."
)

st.subheader("Why This Matters")

st.write(
    "CFTR is an ion channel that helps regulate the movement of chloride and "
    "bicarbonate across epithelial cell membranes. Variants that alter CFTR "
    "structure or function can interfere with this process and, when sufficiently "
    "disruptive, contribute to the abnormal mucus and other organ effects "
    "associated with cystic fibrosis."
)

st.write(
    "By examining where variants occur, what types of changes they represent, "
    "and how conserved the affected regions are, this project helps investigate "
    "why variants in different parts of CFTR may have different functional "
    "consequences. These patterns can also help identify regions of the protein "
    "that may be particularly important for CFTR function."
)

st.write(
    "Importantly, this analysis identifies patterns and possible relationships "
    "rather than proving that a particular variant causes a specific clinical outcome."
)
