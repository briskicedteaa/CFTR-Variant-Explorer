from .data_loader import load_data

def get_position(position):
    FinalPosition, CFTR_variants = load_data()
  
    result = FinalPosition[
        FinalPosition["Human_Position"] == position
    ].copy()

    return result
