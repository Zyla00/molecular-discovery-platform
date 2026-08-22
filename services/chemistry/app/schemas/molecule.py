from pydantic import BaseModel, Field


class MoleculeInput(BaseModel):
    smiles: str = Field(
        ...,
        min_length=1,
        description="Molecule represented as a SMILES string",
    )


class MolecularDescriptors(BaseModel):
    molecular_weight: float
    logp: float
    tpsa: float
    h_bond_donors: int
    h_bond_acceptors: int
    rotatable_bonds: int


class MoleculeDescriptorsResponse(BaseModel):
    input_smiles: str
    canonical_smiles: str
    descriptors: MolecularDescriptors