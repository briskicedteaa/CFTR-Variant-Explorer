import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_data():
    position_df = pd.read_csv(DATA_DIR / "FinalPosition.csv")
    variants_df = pd.read_csv(DATA_DIR / "CFTR_variants.csv")

    return position_df, variants_df

def load_alignment():
    alignment_path = DATA_DIR / "clustalo-I20260824-221828-0411-59024886-p1m.aln-clustal_num"

    sequences = {}

    with open(alignment_path, "r") as file:
        for line in file:
            line = line.rstrip()

            if not line:
                continue

            if line.startswith("CLUSTAL"):
                continue

            parts = line.split()

            if len(parts) >= 2:
                sequence_id = parts[0]
                sequence_part = parts[1]

                if all(
                    character in "ABCDEFGHIJKLMNOPQRSTUVWXYZ-*"
                    for character in sequence_part.upper()
                ):
                    if sequence_id not in sequences:
                        sequences[sequence_id] = ""

                    sequences[sequence_id] += sequence_part

    return np.array([
        list(sequence)
        for sequence in sequences.values()
    ])