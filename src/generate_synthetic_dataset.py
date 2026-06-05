from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris


def create_iris_dataset(path: Path, random_state: int = 42) -> pd.DataFrame:
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df["species"] = pd.Categorical.from_codes(iris.target, iris.target_names)

    rng = np.random.default_rng(random_state)
    n_rows = len(df)
    for col in ["sepal length (cm)", "petal length (cm)"]:
        mask = rng.choice([True, False], size=n_rows, p=[0.05, 0.95])
        df.loc[mask, col] = np.nan

    duplicates = df.sample(5, random_state=random_state)
    df = pd.concat([df, duplicates], ignore_index=True)
    df.to_csv(path, index=False)
    return df


def ensure_dataset(path: Path) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return pd.read_csv(path)
    return create_iris_dataset(path)
