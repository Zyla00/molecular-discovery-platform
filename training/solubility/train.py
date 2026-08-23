from pathlib import Path
import json

import joblib
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors, Lipinski, rdMolDescriptors
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor


RANDOM_STATE = 42

SMILES_COLUMN = "SMILES"
TARGET_COLUMN = "measured log(solubility:mol/L)"
BASELINE_COLUMN = "ESOL predicted log(solubility:mol/L)"

FEATURE_NAMES = [
    "molecular_weight",
    "logp",
    "tpsa",
    "h_bond_donors",
    "h_bond_acceptors",
    "rotatable_bonds",
]

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "delaney.csv"

MODEL_DIR = (
    BASE_DIR.parent.parent
    / "services"
    / "prediction"
    / "models"
)

MODEL_PATH = MODEL_DIR / "solubility.joblib"
METADATA_PATH = MODEL_DIR / "solubility_metadata.json"


def load_dataset() -> pd.DataFrame:
    print(f"Loading dataset from: {DATA_PATH}")

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    print(f"Loaded {len(df)} molecules")

    required_columns = {
        SMILES_COLUMN,
        TARGET_COLUMN,
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}. "
            f"Available columns: {df.columns.tolist()}"
        )

    df = df.dropna(
        subset=[
            SMILES_COLUMN,
            TARGET_COLUMN,
        ]
    ).copy()

    df[TARGET_COLUMN] = pd.to_numeric(
        df[TARGET_COLUMN],
        errors="coerce",
    )

    df = df.dropna(subset=[TARGET_COLUMN])

    return df


def calculate_descriptors(smiles: str) -> dict:
    molecule = Chem.MolFromSmiles(smiles)

    if molecule is None:
        raise ValueError(
            f"Invalid SMILES: {smiles}"
        )

    return {
        "molecular_weight": Descriptors.MolWt(molecule),
        "logp": Crippen.MolLogP(molecule),
        "tpsa": rdMolDescriptors.CalcTPSA(molecule),
        "h_bond_donors": Lipinski.NumHDonors(molecule),
        "h_bond_acceptors": Lipinski.NumHAcceptors(molecule),
        "rotatable_bonds": Lipinski.NumRotatableBonds(molecule),
    }


def prepare_dataset(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    invalid_smiles_count = 0

    for _, row in df.iterrows():
        smiles = str(row[SMILES_COLUMN])

        try:
            descriptors = calculate_descriptors(smiles)

        except ValueError:
            invalid_smiles_count += 1
            continue

        processed_row = {
            "smiles": smiles,
            **descriptors,
            "target": float(row[TARGET_COLUMN]),
        }

        if BASELINE_COLUMN in df.columns:
            processed_row["baseline_prediction"] = row[
                BASELINE_COLUMN
            ]

        rows.append(processed_row)

    processed = pd.DataFrame(rows)

    if processed.empty:
        raise ValueError(
            "No valid molecules found after preprocessing."
        )

    print(f"Valid molecules: {len(processed)}")
    print(f"Invalid SMILES skipped: {invalid_smiles_count}")

    return processed


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> XGBRegressor:

    model = XGBRegressor(
        objective="reg:squarederror",
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbosity=0,
    )

    model.fit(
        X_train,
        y_train,
    )

    return model

def calculate_metrics(
    y_true: pd.Series,
    predictions,
) -> dict:

    mae = mean_absolute_error(
        y_true,
        predictions,
    )

    rmse = mean_squared_error(
        y_true,
        predictions,
    ) ** 0.5

    r2 = r2_score(
        y_true,
        predictions,
    )

    return {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
    }


def evaluate_model(
    model: XGBRegressor,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict:

    predictions = model.predict(X_test)

    return calculate_metrics(
        y_test,
        predictions,
    )


def save_model(
    model: XGBRegressor,
    metrics: dict,
) -> None:

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_bundle = {
        "model": model,
        "feature_names": FEATURE_NAMES,
        "target": "logS",
        "metrics": metrics,
        "model_type": "XGBRegressor",
    }

    joblib.dump(
        model_bundle,
        MODEL_PATH,
    )

    metadata = {
        "model_type": "XGBRegressor",
        "target": "logS",
        "features": FEATURE_NAMES,
        "metrics": metrics,
        "random_state": RANDOM_STATE,
    }

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metadata,
            file,
            indent=2,
        )

    print(f"\nModel saved to: {MODEL_PATH}")
    print(f"Metadata saved to: {METADATA_PATH}")


def main() -> None:

    df = load_dataset()

    processed = prepare_dataset(df)

    train_df, test_df = train_test_split(
        processed,
        test_size=0.2,
        random_state=RANDOM_STATE,
    )

    X_train = train_df[FEATURE_NAMES]
    y_train = train_df["target"]

    X_test = test_df[FEATURE_NAMES]
    y_test = test_df["target"]

    print(f"\nTraining samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")

    print("\nTraining XGBoost model...")

    model = train_model(
        X_train,
        y_train,
    )

    metrics = evaluate_model(
        model,
        X_test,
        y_test,
    )

    print("\nXGBoost metrics:")
    print(f"MAE:  {metrics['mae']:.4f}")
    print(f"RMSE: {metrics['rmse']:.4f}")
    print(f"R²:   {metrics['r2']:.4f}")

    # Compare against ESOL baseline if available
    if (
        "baseline_prediction" in test_df.columns
        and test_df["baseline_prediction"].notna().all()
    ):
        baseline_metrics = calculate_metrics(
            y_test,
            test_df["baseline_prediction"],
        )

        print("\nESOL baseline metrics:")
        print(f"MAE:  {baseline_metrics['mae']:.4f}")
        print(f"RMSE: {baseline_metrics['rmse']:.4f}")
        print(f"R²:   {baseline_metrics['r2']:.4f}")

        metrics["baseline"] = baseline_metrics

    save_model(
        model,
        metrics,
    )


if __name__ == "__main__":
    main()