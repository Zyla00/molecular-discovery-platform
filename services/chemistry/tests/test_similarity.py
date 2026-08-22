from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_identical_molecules_have_similarity_one():
    response = client.post(
        "/api/v1/molecules/similarity",
        json={
            "smiles_a": "CCO",
            "smiles_b": "CCO",
        },
    )

    assert response.status_code == 200
    assert response.json()["similarity"] == 1.0


def test_different_molecules_have_similarity_below_one():
    response = client.post(
        "/api/v1/molecules/similarity",
        json={
            "smiles_a": "CCO",
            "smiles_b": "CCCCCCCC",
        },
    )

    assert response.status_code == 200
    assert response.json()["similarity"] < 1.0


def test_invalid_smiles_returns_422():
    response = client.post(
        "/api/v1/molecules/similarity",
        json={
            "smiles_a": "CCO",
            "smiles_b": "INVALID",
        },
    )

    assert response.status_code == 422