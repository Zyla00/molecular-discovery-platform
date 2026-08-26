import httpx

from fastapi import APIRouter, HTTPException, status
from app.clients.prediction import prediction_client

from app.clients.chemistry import chemistry_client
from app.schemas.molecule import (
    MoleculeInput,
    SimilarityInput,
    SimilaritySearchInput,
    ChemicalSpaceInput,
    MoleculeDepictionInput,
    DrugLikenessInput,

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

@router.post("/analyze")
async def analyze_molecule(molecule: MoleculeInput):
    try:
        chemistry_result = await chemistry_client.get_descriptors(
            molecule.smiles
        )

        descriptors = chemistry_result["descriptors"]

        prediction_result = await prediction_client.predict_solubility(
            descriptors
        )

        return {
            "molecule": {
                "input_smiles": chemistry_result["input_smiles"],
                "canonical_smiles": chemistry_result["canonical_smiles"],
            },
            "descriptors": descriptors,
            "predictions": {
                "solubility": prediction_result,
            },
        }

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail="Downstream service rejected the request",
        ) from exc

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Downstream service unavailable",
        ) from exc

@router.post("/similarity-search")
async def similarity_search(
    request: SimilaritySearchInput,
):
    try:
        return await chemistry_client.search_similar_compounds(
            smiles=request.smiles,
            top_k=request.top_k,
            exclude_exact_match=request.exclude_exact_match,
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

@router.post("/chemical-space")
async def chemical_space(
    request: ChemicalSpaceInput,
):
    try:
        return await chemistry_client.get_chemical_space(
            smiles=request.smiles,
            top_k=request.top_k,
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

@router.post("/depiction")
async def molecule_depiction(
    request: MoleculeDepictionInput,
):
    try:
        return await chemistry_client.get_depiction(
            request.smiles
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

@router.post("/drug-likeness")
async def drug_likeness(
    request: DrugLikenessInput,
):
    try:
        return await chemistry_client.get_drug_likeness(
            request.smiles
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