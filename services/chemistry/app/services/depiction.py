from rdkit import Chem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D

from app.services.descriptors import parse_smiles


def generate_molecule_svg(
    smiles: str,
    width: int = 400,
    height: int = 300,
) -> tuple[str, str]:

    molecule = parse_smiles(smiles)

    canonical_smiles = Chem.MolToSmiles(
        molecule
    )

    rdDepictor.Compute2DCoords(
        molecule
    )

    drawer = rdMolDraw2D.MolDraw2DSVG(
        width,
        height,
    )

    drawer.DrawMolecule(
        molecule
    )

    drawer.FinishDrawing()

    svg = drawer.GetDrawingText()

    return canonical_smiles, svg