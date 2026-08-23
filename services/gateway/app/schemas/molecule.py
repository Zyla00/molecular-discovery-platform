from pydantic import BaseModel, Field


class MoleculeInput(BaseModel):
    smiles: str = Field(..., min_length=1)


class SimilarityInput(BaseModel):
    smiles_a: str = Field(..., min_length=1)
    smiles_b: str = Field(..., min_length=1)