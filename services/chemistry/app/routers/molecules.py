from fastapi import APIRouter, HTTPException, status

from app.schemas.molecule import (
    MoleculeDescriptorsResponse,
    MoleculeInput, MoleculeSimilarityInput, MoleculeSimilarityResponse, ChemicalSpaceSearchInput,
    ChemicalSpaceSearchResponse, ChemicalSpaceVisualizationInput,
    ChemicalSpaceVisualizationResponse,
    MoleculeDepictionInput,
    MoleculeDepictionResponse,
)

from app.services.chemical_space_projection import chemical_space_projector
from app.services.descriptors import calculate_descriptors
from app.services.similarity import calculate_similarity
from app.services.chemical_space import chemical_space_index
from app.services.depiction import generate_molecule_svg

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

@router.post(
    "/similarity-search",
    response_model=ChemicalSpaceSearchResponse,
)
def search_chemical_space(
    request: ChemicalSpaceSearchInput,
) -> ChemicalSpaceSearchResponse:

    try:
        canonical_smiles, results = (
            chemical_space_index.search(
                smiles=request.smiles,
                top_k=request.top_k,
                exclude_exact_match=request.exclude_exact_match,
            )
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return ChemicalSpaceSearchResponse(
        query_smiles=canonical_smiles,
        results_count=len(results),
        results=results,
    )

@router.post(
    "/chemical-space",
    response_model=ChemicalSpaceVisualizationResponse,
)
def visualize_chemical_space(
    request: ChemicalSpaceVisualizationInput,
) -> ChemicalSpaceVisualizationResponse:

    try:
        result = chemical_space_projector.build_visualization(
            smiles=request.smiles,
            top_k=request.top_k,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return ChemicalSpaceVisualizationResponse(
        **result
    )

@router.post(
    "/depiction",
    response_model=MoleculeDepictionResponse,
)
def depict_molecule(
    request: MoleculeDepictionInput,
) -> MoleculeDepictionResponse:

    try:
        canonical_smiles, svg = generate_molecule_svg(
            request.smiles
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return MoleculeDepictionResponse(
        canonical_smiles=canonical_smiles,
        svg=svg,
    )