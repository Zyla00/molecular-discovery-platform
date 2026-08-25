from fastapi.testclient import TestClient

from app.main import app
from app.services.chemical_space import chemical_space_index


client = TestClient(app)


def test_similarity_search_returns_requested_number_of_results():
    query_smiles = chemical_space_index.compounds[0]["smiles"]

    response = client.post(
        "/api/v1/molecules/similarity-search",
        json={
            "smiles": query_smiles,
            "top_k": 5,
            "exclude_exact_match": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["results_count"] == 5
    assert len(data["results"]) == 5


def test_exact_match_has_similarity_one():
    query_smiles = chemical_space_index.compounds[0]["smiles"]

    response = client.post(
        "/api/v1/molecules/similarity-search",
        json={
            "smiles": query_smiles,
            "top_k": 1,
            "exclude_exact_match": False,
        },
    )

    assert response.status_code == 200

    result = response.json()["results"][0]

    assert result["similarity"] == 1.0


def test_results_are_sorted_by_similarity():
    query_smiles = chemical_space_index.compounds[0]["smiles"]

    response = client.post(
        "/api/v1/molecules/similarity-search",
        json={
            "smiles": query_smiles,
            "top_k": 10,
            "exclude_exact_match": True,
        },
    )

    results = response.json()["results"]

    similarities = [
        result["similarity"]
        for result in results
    ]

    assert similarities == sorted(
        similarities,
        reverse=True,
    )


def test_invalid_smiles_returns_422():
    response = client.post(
        "/api/v1/molecules/similarity-search",
        json={
            "smiles": "THIS_IS_NOT_SMILES",
            "top_k": 5,
            "exclude_exact_match": True,
        },
    )

    assert response.status_code == 422