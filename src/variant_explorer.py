from data_loader import load_data, load_alignment

import joblib
import pandas as pd
import numpy as np
from collections import Counter
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

final_model = joblib.load(
    DATA_DIR / "cftr_random_forest1.pkl"
)

model_features = joblib.load(
    DATA_DIR / "cftr_model_features1.pkl"
)

train_medians = joblib.load(
    DATA_DIR / "cftr_train_medians1.pkl"
)

alignment = load_alignment()

aa_properties = {
    "A": {"hydrophobicity": 1.8, "polarity": 8.1, "charge": 0, "size": 1},
    "R": {"hydrophobicity": -4.5, "polarity": 10.5, "charge": 1, "size": 4},
    "N": {"hydrophobicity": -3.5, "polarity": 11.6, "charge": 0, "size": 2},
    "D": {"hydrophobicity": -3.5, "polarity": 13.0, "charge": -1, "size": 2},
    "C": {"hydrophobicity": 2.5, "polarity": 5.5, "charge": 0, "size": 2},
    "Q": {"hydrophobicity": -3.5, "polarity": 10.5, "charge": 0, "size": 3},
    "E": {"hydrophobicity": -3.5, "polarity": 12.3, "charge": -1, "size": 3},
    "G": {"hydrophobicity": -0.4, "polarity": 9.0, "charge": 0, "size": 1},
    "H": {"hydrophobicity": -3.2, "polarity": 10.4, "charge": 1, "size": 3},
    "I": {"hydrophobicity": 4.5, "polarity": 5.2, "charge": 0, "size": 3},
    "L": {"hydrophobicity": 3.8, "polarity": 4.9, "charge": 0, "size": 3},
    "K": {"hydrophobicity": -3.9, "polarity": 11.3, "charge": 1, "size": 4},
    "M": {"hydrophobicity": 1.9, "polarity": 5.7, "charge": 0, "size": 3},
    "F": {"hydrophobicity": 2.8, "polarity": 5.2, "charge": 0, "size": 3},
    "P": {"hydrophobicity": -1.6, "polarity": 8.0, "charge": 0, "size": 2},
    "S": {"hydrophobicity": -0.8, "polarity": 9.2, "charge": 0, "size": 2},
    "T": {"hydrophobicity": -0.7, "polarity": 8.6, "charge": 0, "size": 2},
    "W": {"hydrophobicity": -0.9, "polarity": 5.4, "charge": 0, "size": 4},
    "Y": {"hydrophobicity": -1.3, "polarity": 6.2, "charge": 0, "size": 4},
    "V": {"hydrophobicity": 4.2, "polarity": 5.9, "charge": 0, "size": 2}
}


def get_position(position):
    position_df, variants_df = load_data()

    result = position_df[
        position_df["Human_Position"] == position
    ]

    if result.empty:
        return None

    return result.iloc[0]


def get_variants_at_position(position):
    position_df, variants_df = load_data()

    return variants_df[
        variants_df["Position"] == position
    ]


def get_position_summary(position):
    position_df, variants_df = load_data()

    position_info = position_df[
        position_df["Human_Position"].astype(int) == int(position)
    ]

    variants = variants_df[
        variants_df["Position"] == position
    ]

    return position_info, variants


def get_consequence_summary(position=None):
    position_df, variants_df = load_data()

    if position is not None:
        variants_df = variants_df[
            variants_df["Position"] == position
        ]

    return variants_df["Consequence"].value_counts().to_dict()


def predict_consequence(position, wild_type, mutated_type):
    position_df, variants_df = load_data()

    position_df["Human_Position"] = pd.to_numeric(
        position_df["Human_Position"],
        errors="coerce"
    )

    position_df["Alignment_Position"] = pd.to_numeric(
        position_df["Alignment_Position"],
        errors="coerce"
    )

    position = int(position)

    position_info = position_df[
        position_df["Human_Position"] == position
    ]

    if position_info.empty:
        return {
            "prediction": "Unable to predict",
            "confidence": None
        }

    alignment_position = position_info.iloc[0]["Alignment_Position"]

    if pd.isna(alignment_position):
        return {
            "prediction": "Unable to predict",
            "confidence": None
        }

    column = alignment[:, int(alignment_position) - 1]
    counts = Counter(column)

    total = len(column)

    wild_type = (
        str(wild_type).upper()
        if pd.notna(wild_type)
        else ""
    )

    mutated_type = (
        str(mutated_type).upper()
        if pd.notna(mutated_type)
        else ""
    )

    features = {
        "Position": position,
        "WildType": wild_type,
        "MutatedType": mutated_type,
        "Alignment_Position": alignment_position,
        "Human_Residue_Frequency":
            counts.get(wild_type, 0) / total,
        "Mutant_Residue_Frequency":
            counts.get(mutated_type, 0) / total,
        "Gap_Frequency":
            counts.get("-", 0) / total,
        "Distinct_Residues":
            len(counts),
        "Mutant_Observed":
            mutated_type in counts
    }

    wild = aa_properties.get(wild_type)
    mutant = aa_properties.get(mutated_type)

    if wild is not None and mutant is not None:
        features.update({
            "Hydrophobicity_Change":
                mutant["hydrophobicity"] - wild["hydrophobicity"],
            "Polarity_Change":
                mutant["polarity"] - wild["polarity"],
            "Charge_Change":
                mutant["charge"] - wild["charge"],
            "Size_Change":
                mutant["size"] - wild["size"]
        })
    else:
        features.update({
            "Hydrophobicity_Change": np.nan,
            "Polarity_Change": np.nan,
            "Charge_Change": np.nan,
            "Size_Change": np.nan
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

    input_df = input_df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    numeric_columns = input_df.select_dtypes(
        include=["number"]
    ).columns

    input_df[numeric_columns] = input_df[numeric_columns].fillna(
        train_medians
    )

    input_df = input_df.fillna(False)

    prediction = final_model.predict(input_df)[0]

    probabilities = final_model.predict_proba(input_df)[0]

    confidence = probabilities.max()

    return {
        "prediction": prediction,
        "confidence": confidence
    }