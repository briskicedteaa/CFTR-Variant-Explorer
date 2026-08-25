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
