from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_solubility_prediction():
    response = client.post(
        "/api/v1/predictions/solubility",
        json={
            "molecular_weight": 46.069,
            "logp": -0.001,
            "tpsa": 20.23,
            "h_bond_donors": 1,
            "h_bond_acceptors": 1,
            "rotatable_bonds": 0,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "predicted_log_s" in data
    assert isinstance(data["predicted_log_s"], float)
    assert data["model"] == "XGBRegressor"


def test_model_info():
    response = client.get(
        "/api/v1/predictions/solubility/model-info"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["model"] == "XGBRegressor"
    assert data["target"] == "logS"
    assert len(data["features"]) == 6