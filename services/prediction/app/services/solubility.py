from pathlib import Path

import joblib
import pandas as pd

from app.schemas.prediction import MolecularFeatures


MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "models"
    / "solubility.joblib"
)


class SolubilityPredictor:
    def __init__(self) -> None:
        bundle = joblib.load(MODEL_PATH)

        self.model = bundle["model"]
        self.feature_names = bundle["feature_names"]
        self.metrics = bundle["metrics"]
        self.model_type = bundle["model_type"]
        self.target = bundle["target"]

    def predict(
        self,
        features: MolecularFeatures,
    ) -> float:

        feature_values = features.model_dump()

        X = pd.DataFrame(
            [
                [
                    feature_values[feature_name]
                    for feature_name in self.feature_names
                ]
            ],
            columns=self.feature_names,
        )

        prediction = self.model.predict(X)[0]

        return float(prediction)


solubility_predictor = SolubilityPredictor()