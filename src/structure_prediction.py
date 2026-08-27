def validate_protein_sequence(sequence):
    """Validate and clean a protein sequence."""
    sequence = sequence.strip().upper().replace(" ", "").replace("\n", "")

    valid_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")

    if not sequence:
        raise ValueError("Protein sequence is empty.")

    invalid = set(sequence) - valid_amino_acids

    if invalid:
        raise ValueError(
            f"Invalid amino-acid characters found: {', '.join(sorted(invalid))}"
        )

    return sequence


def prepare_colabfold_query(sequence, query_name="CFTR_variant"):
    """Prepare a validated protein sequence for a ColabFold query."""
    sequence = validate_protein_sequence(sequence)

    return {
        "name": query_name,
        "sequence": sequence,
    }