import os

import httpx


PREDICTION_SERVICE_URL = os.getenv(
    "PREDICTION_SERVICE_URL",
    "http://prediction:8000",
)


class PredictionClient:
    def __init__(self) -> None:
        self.base_url = PREDICTION_SERVICE_URL

    async def predict_solubility(
        self,
        descriptors: dict,
    ) -> dict:
        async with httpx.AsyncClient(
            base_url=self.base_url,
            timeout=10.0,
        ) as client:
            response = await client.post(
                "/api/v1/predictions/solubility",
                json=descriptors,
            )

            response.raise_for_status()

            return response.json()


prediction_client = PredictionClient()