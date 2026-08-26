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

class ChemicalSpaceSearchInput(BaseModel):
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


class SimilarCompound(BaseModel):
    compound_id: str
    smiles: str
    similarity: float
    measured_log_s: float


class ChemicalSpaceSearchResponse(BaseModel):
    query_smiles: str
    results_count: int
    results: list[SimilarCompound]

class ChemicalSpaceVisualizationInput(BaseModel):
    smiles: str = Field(
        ...,
        min_length=1,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class ChemicalSpacePoint(BaseModel):
    compound_id: str
    smiles: str
    x: float
    y: float
    similarity: float | None = None
    is_neighbor: bool = False


class QueryPoint(BaseModel):
    smiles: str
    x: float
    y: float


class ChemicalSpaceVisualizationResponse(BaseModel):
    method: str
    explained_variance: list[float]
    query: QueryPoint
    points: list[ChemicalSpacePoint]

class MoleculeDepictionInput(BaseModel):
    smiles: str = Field(
        ...,
        min_length=1,
    )

class MoleculeDepictionResponse(BaseModel):
    canonical_smiles: str
    svg: str