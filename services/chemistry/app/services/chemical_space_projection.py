import numpy as np

from rdkit import DataStructs
from sklearn.decomposition import PCA

from app.services.chemical_space import (
    chemical_space_index,
    morgan_generator,
)
from app.services.descriptors import parse_smiles


class ChemicalSpaceProjector:
    def __init__(self) -> None:
        self.pca = PCA(
            n_components=2,
            random_state=42,
        )

        self.fingerprint_matrix = self._fingerprints_to_matrix(
            chemical_space_index.fingerprints
        )

        self.coordinates = self.pca.fit_transform(
            self.fingerprint_matrix
        )

    @staticmethod
    def _fingerprint_to_array(fingerprint) -> np.ndarray:
        array = np.zeros(
            (fingerprint.GetNumBits(),),
            dtype=np.float32,
        )

        DataStructs.ConvertToNumpyArray(
            fingerprint,
            array,
        )

        return array

    def _fingerprints_to_matrix(
        self,
        fingerprints,
    ) -> np.ndarray:

        return np.vstack(
            [
                self._fingerprint_to_array(fp)
                for fp in fingerprints
            ]
        )

    def project_query(
        self,
        smiles: str,
    ) -> tuple[str, list[float]]:

        molecule = parse_smiles(smiles)

        from rdkit import Chem

        canonical_smiles = Chem.MolToSmiles(
            molecule
        )

        fingerprint = morgan_generator.GetFingerprint(
            molecule
        )

        fingerprint_array = self._fingerprint_to_array(
            fingerprint
        ).reshape(1, -1)

        coordinates = self.pca.transform(
            fingerprint_array
        )[0]

        return canonical_smiles, [
            float(coordinates[0]),
            float(coordinates[1]),
        ]

    def build_visualization(
            self,
            smiles: str,
            top_k: int = 5,
    ) -> dict:
        canonical_smiles, query_coordinates = (
            self.project_query(smiles)
        )

        _, neighbours = chemical_space_index.search(
            smiles=smiles,
            top_k=top_k,
            exclude_exact_match=True,
        )

        neighbour_map = {
            item["smiles"]: item["similarity"]
            for item in neighbours
        }

        points = []

        for compound, coordinates in zip(
                chemical_space_index.compounds,
                self.coordinates,
        ):
            compound_smiles = compound["smiles"]

            is_neighbor = (
                    compound_smiles in neighbour_map
            )

            points.append(
                {
                    "compound_id": compound["compound_id"],
                    "smiles": compound_smiles,
                    "x": float(coordinates[0]),
                    "y": float(coordinates[1]),
                    "similarity": (
                        float(neighbour_map[compound_smiles])
                        if is_neighbor
                        else None
                    ),
                    "is_neighbor": is_neighbor,
                }
            )

        return {
            "method": "PCA",
            "explained_variance": [
                float(value)
                for value in self.pca.explained_variance_ratio_
            ],
            "query": {
                "smiles": canonical_smiles,
                "x": query_coordinates[0],
                "y": query_coordinates[1],
            },
            "points": points,
        }

chemical_space_projector = ChemicalSpaceProjector()