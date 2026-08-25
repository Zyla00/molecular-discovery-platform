from pydantic import BaseModel, Field

class MoleculeInput(BaseModel):
    smiles: str = Field(..., min_length=1)


class SimilarityInput(BaseModel):
    smiles_a: str = Field(..., min_length=1)
    smiles_b: str = Field(..., min_length=1)

class SimilaritySearchInput(BaseModel):
    smiles: str = Field(
        ...,
        min_length=1,
    )
    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )
    exclude_exact_match: bool = True

class ChemicalSpaceInput(BaseModel):
    smiles: str = Field(
        ...,
        min_length=1,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )