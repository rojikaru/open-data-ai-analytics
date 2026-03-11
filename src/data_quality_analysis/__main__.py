import os
import sys

from src.constants import DATASET_URL
from src.data_load import load_data


def main():
    out_dir = os.path.join("artifacts", "data_quality_analysis")
    os.makedirs(out_dir, exist_ok=True)

    df = load_data(DATASET_URL, clear_cache=False)
    if isinstance(df, Exception):
        print(f"Failed to load data: {df}", file=sys.stderr)
        sys.exit(1)

    describe = df.describe()
    print("Dataset description:")
    print(describe)
    describe.write_csv(os.path.join(out_dir, "quality_report.csv"))

    null_counts = df.null_count()
    print("\nNull counts per column:")
    print(null_counts)
    null_counts.write_csv(os.path.join(out_dir, "null_counts.csv"))

    print(f"\nRows: {df.shape[0]}, Columns: {df.shape[1]}")


if __name__ == "__main__":
    main()
