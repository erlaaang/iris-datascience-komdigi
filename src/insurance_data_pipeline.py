from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    return df


def analyze_data(df: pd.DataFrame) -> list[str]:
    lines = ["# Ringkasan Analisis Data"]
    lines.append(f"Jumlah baris: {len(df)}")
    lines.append(f"Jumlah kolom: {len(df.columns)}")
    lines.append("\n## Kolom dan tipe data")
    lines.extend([f"- {col}: {dtype}" for col, dtype in df.dtypes.items()])
    lines.append("\n## Missing value")
    missing = df.isna().sum()
    lines.extend([f"- {col}: {int(count)}" for col, count in missing.items() if count > 0])
    lines.append("\n## Duplikasi")
    lines.append(f"- Baris duplikat: {df.duplicated().sum()}")
    lines.append("\n## Statistik numerik")
    lines.append(df.describe(include=[np.number]).to_string())

    invalid = []
    ranges = {
        "sepal length (cm)": (0, 10),
        "sepal width (cm)": (0, 10),
        "petal length (cm)": (0, 10),
        "petal width (cm)": (0, 10),
    }
    for col, (min_val, max_val) in ranges.items():
        if col in df.columns:
            invalid_count = ((df[col] < min_val) | (df[col] > max_val)).sum()
            invalid.append(f"- {col} di luar kisaran {min_val}-{max_val}: {invalid_count}")
    lines.append("\n## Data tidak valid")
    lines.extend(invalid)

    lines.append("\n## Outlier (IQR) pada kolom numerik")
    for col in df.select_dtypes(include=[np.number]).columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        if pd.isna(iqr) or iqr == 0:
            continue
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        lines.append(f"- {col}: {outliers} outlier")
    return lines


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates().reset_index(drop=True)
    numeric_cols = [col for col in df.select_dtypes(include=[np.number]).columns]
    categorical_cols = [col for col in df.select_dtypes(include=["object", "category"]).columns]

    df = df[df.isna().sum(axis=1) <= 2].reset_index(drop=True)
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())
    for col in categorical_cols:
        df[col] = df[col].astype("string")
        mode_value = df[col].mode(dropna=True)
        if not mode_value.empty:
            df[col] = df[col].fillna(mode_value.iloc[0])

    clip_ranges = {
        "sepal length (cm)": (3.0, 8.0),
        "sepal width (cm)": (2.0, 5.0),
        "petal length (cm)": (1.0, 7.0),
        "petal width (cm)": (0.1, 3.0),
    }
    for col, (low, high) in clip_ranges.items():
        if col in df.columns:
            df[col] = df[col].clip(lower=low, upper=high)
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if {"sepal length (cm)", "sepal width (cm)"}.issubset(df.columns):
        df["sepal_area"] = (df["sepal length (cm)"] * df["sepal width (cm)"]).round(3)
    if {"petal length (cm)", "petal width (cm)"}.issubset(df.columns):
        df["petal_area"] = (df["petal length (cm)"] * df["petal width (cm)"]).round(3)
    if {"sepal_area", "petal_area"}.issubset(df.columns):
        df["area_ratio"] = (df["petal_area"] / df["sepal_area"]).round(3)

    numeric_cols = [col for col in df.select_dtypes(include=[np.number]).columns]
    scaler = MinMaxScaler()
    if numeric_cols:
        df[[f"scaled_{col}" for col in numeric_cols]] = scaler.fit_transform(df[numeric_cols])

    if "species" in df.columns:
        df = pd.get_dummies(df, columns=["species"], drop_first=True)
    return df


def label_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "petal_area" in df.columns:
        df["petal_size_category"] = pd.qcut(df["petal_area"], q=3, labels=["small", "medium", "large"])
        df["petal_size_category"] = df["petal_size_category"].astype(str)
    if {"sepal_area", "petal_area"}.issubset(df.columns):
        df["shape_label"] = np.where(df["petal_area"] > df["sepal_area"], "petal_dominant", "sepal_dominant")
    return df


def save_report(lines: list[str], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def save_figures(df: pd.DataFrame, figure_dir: Path) -> None:
    figure_dir.mkdir(parents=True, exist_ok=True)
    if "sepal length (cm)" in df.columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(df["sepal length (cm)"], kde=True, color="#264653")
        plt.title("Distribusi Sepal Length")
        plt.savefig(figure_dir / "sepal_length_histogram.png", bbox_inches="tight")
        plt.close()
    if {"petal length (cm)", "species"}.issubset(df.columns):
        plt.figure(figsize=(8, 5))
        sns.boxplot(x=df["species"], y=df["petal length (cm)"], color="#e76f51")
        plt.title("Boxplot Petal Length by Species")
        plt.savefig(figure_dir / "petal_length_boxplot.png", bbox_inches="tight")
        plt.close()
    if {"sepal length (cm)", "sepal width (cm)"}.issubset(df.columns):
        plt.figure(figsize=(8, 5))
        hue = df["petal_size_category"].astype(str) if "petal_size_category" in df.columns else None
        if hue is not None:
            sns.scatterplot(data=df, x="sepal length (cm)", y="sepal width (cm)", hue=hue, palette="Set2")
        else:
            sns.scatterplot(data=df, x="sepal length (cm)", y="sepal width (cm)")
        plt.title("Sepal Length vs Sepal Width")
        plt.savefig(figure_dir / "sepal_scatter.png", bbox_inches="tight")
        plt.close()


def run_pipeline(source_path: Path, report_dir: Path) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    df_raw = load_data(source_path)
    analysis_lines = analyze_data(df_raw)

    df_cleaned = clean_data(df_raw)
    analysis_lines.append("\n# Data Setelah Pembersihan")
    analysis_lines.append(f"Jumlah baris setelah pembersihan: {len(df_cleaned)}")

    df_transformed = transform_data(df_cleaned)
    df_labeled = label_data(df_transformed)

    cleaned_path = source_path.parent / "iris_data_cleaned.csv"
    transformed_path = source_path.parent / "iris_data_transformed.csv"
    df_cleaned.to_csv(cleaned_path, index=False)
    df_labeled.to_csv(transformed_path, index=False)

    save_report(analysis_lines, report_dir / "analysis_report.md")
    label_counts = (
        df_labeled["petal_size_category"].value_counts().rename_axis("petal_size_category").reset_index(name="count")
        if "petal_size_category" in df_labeled.columns
        else pd.DataFrame()
    )
    label_counts.to_csv(report_dir / "label_distribution.csv", index=False)
    save_figures(df_cleaned, report_dir / "figures")
