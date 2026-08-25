import streamlit as st

from src.variant_explorer import (
    get_position_summary,
    get_consequence_summary
)

st.title("CFTR Variant Explorer")
st.write(
    "Explore CFTR variant locations, consequences, conservation, "
    "and protein-region characteristics."
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
            st.write(get_consequence_summary(position))