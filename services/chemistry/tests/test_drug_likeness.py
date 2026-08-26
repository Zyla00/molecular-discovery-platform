from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_aspirin_drug_likeness():
    response = client.post(
        "/api/v1/molecules/drug-likeness",
        json={
            "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["lipinski"]["violations"] == 0
    assert data["lipinski"]["passes_rule_of_five"] is True

    assert 0.0 <= data["qed"] <= 1.0


def test_ethanol_drug_likeness():
    response = client.post(
        "/api/v1/molecules/drug-likeness",
        json={
            "smiles": "CCO",
        },
    )

    assert response.status_code == 200

    rules = response.json()["lipinski"]["rules"]

    assert rules["molecular_weight"]["passes"] is True
    assert rules["logp"]["passes"] is True
    assert rules["h_bond_donors"]["passes"] is True
    assert rules["h_bond_acceptors"]["passes"] is True


def test_invalid_smiles_returns_422():
    response = client.post(
        "/api/v1/molecules/drug-likeness",
        json={
            "smiles": "NOT_A_SMILES",
        },
    )

    assert response.status_code == 422