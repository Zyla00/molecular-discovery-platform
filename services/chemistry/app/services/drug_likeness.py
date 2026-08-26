from rdkit.Chem import Crippen, Descriptors, Lipinski, QED

from app.services.descriptors import parse_smiles


def calculate_drug_likeness(smiles: str) -> dict:
    molecule = parse_smiles(smiles)

    molecular_weight = Descriptors.MolWt(molecule)
    logp = Crippen.MolLogP(molecule)
    h_bond_donors = Lipinski.NumHDonors(molecule)
    h_bond_acceptors = Lipinski.NumHAcceptors(molecule)

    rules = {
        "molecular_weight": {
            "value": round(molecular_weight, 3),
            "threshold": "<= 500",
            "passes": molecular_weight <= 500,
        },
        "logp": {
            "value": round(logp, 3),
            "threshold": "<= 5",
            "passes": logp <= 5,
        },
        "h_bond_donors": {
            "value": h_bond_donors,
            "threshold": "<= 5",
            "passes": h_bond_donors <= 5,
        },
        "h_bond_acceptors": {
            "value": h_bond_acceptors,
            "threshold": "<= 10",
            "passes": h_bond_acceptors <= 10,
        },
    }

    violations = sum(
        not rule["passes"]
        for rule in rules.values()
    )

    qed_score = QED.qed(molecule)

    return {
        "lipinski": {
            "rules": rules,
            "violations": violations,
            "passes_rule_of_five": violations <= 1,
        },
        "qed": round(float(qed_score), 4),
    }