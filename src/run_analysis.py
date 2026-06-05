from pathlib import Path

from generate_synthetic_dataset import ensure_dataset
from insurance_data_pipeline import run_pipeline


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    source_path = root / "data" / "iris_data.csv"
    report_dir = root / "reports"
    ensure_dataset(source_path)
    run_pipeline(source_path, report_dir)


if __name__ == "__main__":
    main()
