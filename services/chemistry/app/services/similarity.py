from rdkit import DataStructs
from rdkit.Chem import rdFingerprintGenerator

from app.services.descriptors import parse_smiles


morgan_generator = rdFingerprintGenerator.GetMorganGenerator(
    radius=2,
    fpSize=2048,
)


def calculate_similarity(
    smiles_a: str,
    smiles_b: str,
) -> tuple[str, str, float]:

    molecule_a = parse_smiles(smiles_a)
    molecule_b = parse_smiles(smiles_b)

    fingerprint_a = morgan_generator.GetFingerprint(molecule_a)
    fingerprint_b = morgan_generator.GetFingerprint(molecule_b)

    similarity = DataStructs.TanimotoSimilarity(
        fingerprint_a,
        fingerprint_b,
    )

    from rdkit import Chem

    canonical_a = Chem.MolToSmiles(molecule_a)
    canonical_b = Chem.MolToSmiles(molecule_b)

    return canonical_a, canonical_b, round(similarity, 4)