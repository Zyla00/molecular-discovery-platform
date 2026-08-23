import os

import httpx


CHEMISTRY_SERVICE_URL = os.getenv(
    "CHEMISTRY_SERVICE_URL",
    "http://chemistry:8000",
)


class ChemistryClient:

    def __init__(self) -> None:
        self.base_url = CHEMISTRY_SERVICE_URL

    async def get_descriptors(self, smiles: str) -> dict:
        async with httpx.AsyncClient(
            base_url=self.base_url,
            timeout=10.0,
        ) as client:
            response = await client.post(
                "/api/v1/molecules/descriptors",
                json={"smiles": smiles},
            )

            response.raise_for_status()

            return response.json()

    async def calculate_similarity(
        self,
        smiles_a: str,
        smiles_b: str,
    ) -> dict:
        async with httpx.AsyncClient(
            base_url=self.base_url,
            timeout=10.0,
        ) as client:
            response = await client.post(
                "/api/v1/molecules/similarity",
                json={
                    "smiles_a": smiles_a,
                    "smiles_b": smiles_b,
                },
            )

            response.raise_for_status()

            return response.json()


chemistry_client = ChemistryClient()