import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_descriptors_for_ethanol():
    response = client.post(
        "/api/v1/molecules/descriptors",
        json={"smiles": "CCO"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["canonical_smiles"] == "CCO"

    descriptors = data["descriptors"]

    assert descriptors["molecular_weight"] == pytest.approx(
        46.069,
        abs=0.01,
    )
    assert descriptors["h_bond_donors"] == 1
    assert descriptors["h_bond_acceptors"] == 1


def test_invalid_smiles_returns_422():
    response = client.post(
        "/api/v1/molecules/descriptors",
        json={"smiles": "ABCXYZ"},
    )

    assert response.status_code == 422