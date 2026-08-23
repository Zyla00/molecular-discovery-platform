from fastapi import APIRouter

from app.schemas.prediction import (
    MolecularFeatures,
    SolubilityPredictionResponse,
)
from app.services.solubility import solubility_predictor


router = APIRouter(
    prefix="/api/v1/predictions",
    tags=["predictions"],
)


@router.post(
    "/solubility",
    response_model=SolubilityPredictionResponse,
)
def predict_solubility(
    features: MolecularFeatures,
) -> SolubilityPredictionResponse:

    prediction = solubility_predictor.predict(features)

    return SolubilityPredictionResponse(
        predicted_log_s=round(prediction, 4),
        model=solubility_predictor.model_type,
    )


@router.get("/solubility/model-info")
def get_model_info():
    return {
        "model": solubility_predictor.model_type,
        "target": solubility_predictor.target,
        "features": solubility_predictor.feature_names,
        "metrics": solubility_predictor.metrics,
    }