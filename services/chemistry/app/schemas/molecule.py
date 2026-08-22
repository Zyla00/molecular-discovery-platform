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

class MoleculeSimilarityInput(BaseModel):
    smiles_a: str = Field(..., min_length=1)
    smiles_b: str = Field(..., min_length=1)


class MoleculeSimilarityResponse(BaseModel):
    canonical_smiles_a: str
    canonical_smiles_b: str
    similarity: float