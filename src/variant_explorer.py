from data_loader import load_data, load_alignment

import joblib
import pandas as pd
import numpy as np
from collections import Counter
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

final_model = joblib.load(
    DATA_DIR / "cftr_random_forest.pkl"
)

model_features = joblib.load(
    DATA_DIR / "cftr_model_features.pkl"
)

alignment = load_alignment()

aa_properties = {
    "A": {"hydrophobicity": 1.8, "polarity": 8.1, "charge": 0, "size": 89.1},
    "R": {"hydrophobicity": -4.5, "polarity": 10.5, "charge": 1, "size": 174.2},
    "N": {"hydrophobicity": -3.5, "polarity": 11.6, "charge": 0, "size": 132.1},
    "D": {"hydrophobicity": -3.5, "polarity": 13.0, "charge": -1, "size": 133.1},
    "C": {"hydrophobicity": 2.5, "polarity": 5.5, "charge": 0, "size": 121.2},
    "Q": {"hydrophobicity": -3.5, "polarity": 10.5, "charge": 0, "size": 146.2},
    "E": {"hydrophobicity": -3.5, "polarity": 12.3, "charge": -1, "size": 147.1},
    "G": {"hydrophobicity": -0.4, "polarity": 9.0, "charge": 0, "size": 75.1},
    "H": {"hydrophobicity": -3.2, "polarity": 10.4, "charge": 0, "size": 155.2},
    "I": {"hydrophobicity": 4.5, "polarity": 5.2, "charge": 0, "size": 131.2},
    "L": {"hydrophobicity": 3.8, "polarity": 4.9, "charge": 0, "size": 131.2},
    "K": {"hydrophobicity": -3.9, "polarity": 11.3, "charge": 1, "size": 146.2},
    "M": {"hydrophobicity": 1.9, "polarity": 5.7, "charge": 0, "size": 149.2},
    "F": {"hydrophobicity": 2.8, "polarity": 5.2, "charge": 0, "size": 165.2},
    "P": {"hydrophobicity": -1.6, "polarity": 8.0, "charge": 0, "size": 115.1},
    "S": {"hydrophobicity": -0.8, "polarity": 9.2, "charge": 0, "size": 105.1},
    "T": {"hydrophobicity": -0.7, "polarity": 8.6, "charge": 0, "size": 119.1},
    "W": {"hydrophobicity": -0.9, "polarity": 5.4, "charge": 0, "size": 204.2},
    "Y": {"hydrophobicity": -1.3, "polarity": 6.2, "charge": 0, "size": 181.2},
    "V": {"hydrophobicity": 4.2, "polarity": 5.9, "charge": 0, "size": 117.1}
}

def get_position(position):
    FinalPosition, CFTR_variants = load_data()

    result = FinalPosition[
        FinalPosition["Position"] == position
    ].copy()

    return result

def get_variants_at_position(position):
    position_df, variants_df = load_data()

    result = variants_df[
        variants_df["Position"] == position
    ].copy()

    return result

def get_position_summary(position):
    position_df, variants_df = load_data()

    position_info = position_df[
        position_df["Human_Position"] == position
    ].copy()

    if position_info.empty:
        return None, None

    variants = variants_df[
        variants_df["Position"] == position
    ].copy()

    return position_info, variants

def get_consequence_summary(position):
    position_df, variants_df = load_data()

    variants = variants_df[
        variants_df["Position"] == position
    ].copy()

    if variants.empty:
        return {}

    return variants["Consequence"].value_counts().to_dict()

def predict_consequence(position, wild_type, mutated_type):
    position_df, variants_df = load_data()

    position_info = position_df[
        position_df["Human_Position"] == position
    ]

    if position_info.empty:
        return {
            "prediction": "Unable to predict",
            "confidence": None
        }

    alignment_position = position_info.iloc[0]["Alignment_Position"]

    column = alignment[:, int(alignment_position) - 1]
    counts = Counter(column)

    total = len(column)
    non_gap = total - counts.get("-", 0)

    features = {
        "Position": position,
        "WildType": wild_type,
        "MutatedType": mutated_type,
        "Alignment_Position": alignment_position,
        "Human_Residue_Frequency": counts.get(
            wild_type, 0
        ) / non_gap,
        "Mutant_Residue_Frequency": counts.get(
            mutated_type, 0
        ) / non_gap,
        "Gap_Frequency": counts.get("-", 0) / total,
        "Distinct_Residues": len(
            [x for x in counts if x != "-"]
        ),
        "Mutant_Observed": counts.get(
            mutated_type, 0
        ) > 0
    }

    if (
        wild_type in aa_properties
        and mutated_type in aa_properties
    ):
        features.update({
            "Hydrophobicity_Change":
                aa_properties[mutated_type]["hydrophobicity"]
                - aa_properties[wild_type]["hydrophobicity"],

            "Polarity_Change":
                aa_properties[mutated_type]["polarity"]
                - aa_properties[wild_type]["polarity"],

            "Charge_Change":
                aa_properties[mutated_type]["charge"]
                - aa_properties[wild_type]["charge"],

            "Size_Change":
                aa_properties[mutated_type]["size"]
                - aa_properties[wild_type]["size"]
        })

    else:
        features.update({
            "Hydrophobicity_Change": 0,
            "Polarity_Change": 0,
            "Charge_Change": 0,
            "Size_Change": 0
        })

    input_df = pd.DataFrame([features])

    input_df = pd.get_dummies(
        input_df,
        columns=["WildType", "MutatedType"],
        dummy_na=True
    )

    input_df = input_df.reindex(
        columns=model_features,
        fill_value=0
    )

    input_df = input_df.fillna(0)

    prediction = final_model.predict(input_df)[0]

    probabilities = final_model.predict_proba(input_df)[0]
    confidence = probabilities.max()

    return {
        "prediction": prediction,
        "confidence": confidence
    }