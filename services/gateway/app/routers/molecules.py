import httpx

from fastapi import APIRouter, HTTPException, status

from app.clients.chemistry import chemistry_client
from app.schemas.molecule import (
    MoleculeInput,
    SimilarityInput,
)


router = APIRouter(
    prefix="/api/v1/molecules",
    tags=["molecules"],
)


@router.post("/descriptors")
async def get_descriptors(molecule: MoleculeInput):
    try:
        return await chemistry_client.get_descriptors(
            molecule.smiles
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail="Chemistry service rejected the request",
        ) from exc

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chemistry service unavailable",
        ) from exc


@router.post("/similarity")
async def calculate_similarity(molecules: SimilarityInput):
    try:
        return await chemistry_client.calculate_similarity(
            molecules.smiles_a,
            molecules.smiles_b,
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail="Chemistry service rejected the request",
        ) from exc

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chemistry service unavailable",
        ) from exc