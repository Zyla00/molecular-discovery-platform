from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors, Lipinski, rdMolDescriptors

from app.schemas.molecule import MolecularDescriptors


def parse_smiles(smiles: str) -> Chem.Mol:
    molecule = Chem.MolFromSmiles(smiles)

    if molecule is None:
        raise ValueError("Invalid SMILES")

    return molecule


def calculate_descriptors(smiles: str) -> tuple[str, MolecularDescriptors]:
    molecule = parse_smiles(smiles)

    canonical_smiles = Chem.MolToSmiles(molecule)

    descriptors = MolecularDescriptors(
        molecular_weight=round(Descriptors.MolWt(molecule), 3),
        logp=round(Crippen.MolLogP(molecule), 3),
        tpsa=round(rdMolDescriptors.CalcTPSA(molecule), 3),
        h_bond_donors=Lipinski.NumHDonors(molecule),
        h_bond_acceptors=Lipinski.NumHAcceptors(molecule),
        rotatable_bonds=Lipinski.NumRotatableBonds(molecule),
    )

    return canonical_smiles, descriptors