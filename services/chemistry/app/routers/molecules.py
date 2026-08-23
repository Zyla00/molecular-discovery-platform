from fastapi import APIRouter, HTTPException, status

from app.schemas.molecule import (
    MoleculeDescriptorsResponse,
    MoleculeInput, MoleculeSimilarityInput, MoleculeSimilarityResponse,
)
from app.services.descriptors import calculate_descriptors
from app.services.similarity import calculate_similarity

router = APIRouter(
    prefix="/api/v1/molecules",
    tags=["molecules"],
)


@router.post(
    "/descriptors",
    response_model=MoleculeDescriptorsResponse,
)
def get_molecular_descriptors(
    molecule: MoleculeInput,
) -> MoleculeDescriptorsResponse:
    try:
        canonical_smiles, descriptors = calculate_descriptors(
            molecule.smiles
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return MoleculeDescriptorsResponse(
        input_smiles=molecule.smiles,
        canonical_smiles=canonical_smiles,
        descriptors=descriptors,
    )

@router.post(
    "/similarity",
    response_model=MoleculeSimilarityResponse,
)
def get_molecular_similarity(
    molecules: MoleculeSimilarityInput,
) -> MoleculeSimilarityResponse:

    try:
        canonical_a, canonical_b, similarity = calculate_similarity(
            molecules.smiles_a,
            molecules.smiles_b,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return MoleculeSimilarityResponse(
        canonical_smiles_a=canonical_a,
        canonical_smiles_b=canonical_b,
        similarity=similarity,
    )