import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_data():
    position_df = pd.read_csv(DATA_DIR / "FinalPosition.csv")
    variants_df = pd.read_csv(DATA_DIR / "CFTR_variants.csv")
    cftr_df = pd.read_csv(DATA_DIR / "CFTR_DF.csv")

    return position_df, variants_df, cftr_df