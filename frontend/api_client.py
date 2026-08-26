import os

import requests


GATEWAY_URL = os.getenv(
    "GATEWAY_URL",
    "http://localhost:8000",
)


class MolecularDiscoveryClient:
    def __init__(self) -> None:
        self.base_url = GATEWAY_URL

    def analyze_molecule(
        self,
        smiles: str,
    ) -> dict:
        response = requests.post(
            f"{self.base_url}/api/v1/molecules/analyze",
            json={
                "smiles": smiles,
            },
            timeout=20,
        )

        response.raise_for_status()

        return response.json()

    def similarity_search(
        self,
        smiles: str,
        top_k: int = 5,
    ) -> dict:
        response = requests.post(
            f"{self.base_url}/api/v1/molecules/similarity-search",
            json={
                "smiles": smiles,
                "top_k": top_k,
                "exclude_exact_match": True,
            },
            timeout=20,
        )

        response.raise_for_status()

        return response.json()

    def chemical_space(
        self,
        smiles: str,
        top_k: int = 5,
    ) -> dict:
        response = requests.post(
            f"{self.base_url}/api/v1/molecules/chemical-space",
            json={
                "smiles": smiles,
                "top_k": top_k,
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def molecule_depiction(
        self,
        smiles: str,
    ) -> dict:
        response = requests.post(
            f"{self.base_url}/api/v1/molecules/depiction",
            json={
                "smiles": smiles,
            },
            timeout=20,
        )

        response.raise_for_status()

        return response.json()

    def drug_likeness(
        self,
        smiles: str,
    ) -> dict:
        response = requests.post(
            f"{self.base_url}/api/v1/molecules/drug-likeness",
            json={
                "smiles": smiles,
            },
            timeout=20,
        )

        response.raise_for_status()

        return response.json()


client = MolecularDiscoveryClient()