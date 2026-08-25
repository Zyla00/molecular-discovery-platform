import csv
from pathlib import Path

from rdkit import Chem, DataStructs
from rdkit.Chem import rdFingerprintGenerator

from app.services.descriptors import parse_smiles


ROOT_DIR = Path(__file__).resolve().parents[4]

DATA_PATH = (
    ROOT_DIR
    / "data"
    / "compound_library"
    / "delaney.csv"
)


morgan_generator = rdFingerprintGenerator.GetMorganGenerator(
    radius=2,
    fpSize=2048,
)


class ChemicalSpaceIndex:
    def __init__(self) -> None:
        self.compounds = []
        self.fingerprints = []

        self._load_compounds()

    def _load_compounds(self) -> None:
        if not DATA_PATH.exists():
            raise FileNotFoundError(
                f"Compound library not found: {DATA_PATH}"
            )

        with open(
            DATA_PATH,
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                smiles = row["SMILES"]

                molecule = Chem.MolFromSmiles(smiles)

                if molecule is None:
                    continue

                canonical_smiles = Chem.MolToSmiles(molecule)

                fingerprint = morgan_generator.GetFingerprint(
                    molecule
                )

                self.compounds.append(
                    {
                        "compound_id": row["Compound ID"],
                        "smiles": canonical_smiles,
                        "measured_log_s": float(
                            row["measured log(solubility:mol/L)"]
                        ),
                    }
                )

                self.fingerprints.append(fingerprint)

    def search(
        self,
        smiles: str,
        top_k: int = 5,
        exclude_exact_match: bool = True,
    ) -> tuple[str, list[dict]]:

        query_molecule = parse_smiles(smiles)

        canonical_query = Chem.MolToSmiles(
            query_molecule
        )

        query_fingerprint = (
            morgan_generator.GetFingerprint(
                query_molecule
            )
        )

        similarities = (
            DataStructs.BulkTanimotoSimilarity(
                query_fingerprint,
                self.fingerprints,
            )
        )

        results = []

        for compound, similarity in zip(
            self.compounds,
            similarities,
        ):
            if (
                exclude_exact_match
                and compound["smiles"] == canonical_query
            ):
                continue

            results.append(
                {
                    **compound,
                    "similarity": float(similarity),
                }
            )

        results.sort(
            key=lambda item: item["similarity"],
            reverse=True,
        )

        return canonical_query, results[:top_k]


chemical_space_index = ChemicalSpaceIndex()