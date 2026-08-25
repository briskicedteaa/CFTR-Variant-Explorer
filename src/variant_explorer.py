from .data_loader import load_data

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
