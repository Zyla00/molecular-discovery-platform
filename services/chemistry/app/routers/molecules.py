from fastapi import APIRouter, HTTPException, status

from app.schemas.molecule import (
    MoleculeDescriptorsResponse,
    MoleculeInput,
)
from app.services.descriptors import calculate_descriptors


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