from .data_loader import load_data

def get_position(position):
    position_df, variants_df = load_data()
  
    result = position_df[
        position_df["Human_Position"] == position
    ].copy()

    return result
