from pydantic import BaseModel


class MolecularFeatures(BaseModel):
    molecular_weight: float
    logp: float
    tpsa: float
    h_bond_donors: int
    h_bond_acceptors: int
    rotatable_bonds: int


class SolubilityPredictionResponse(BaseModel):
    predicted_log_s: float
    model: str