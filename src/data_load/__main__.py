import os
import sys

from src.constants import DATASET_URL
from src.data_load import load_data


def main():
    out_dir = os.path.join("artifacts", "data_load")
    os.makedirs(out_dir, exist_ok=True)

    df = load_data(DATASET_URL, clear_cache=False)
    if isinstance(df, Exception):
        print(f"Failed to load data: {df}", file=sys.stderr)
        sys.exit(1)

    print(f"Shape: {df.shape}")
    print(df.head())
    df.head(1000).write_csv(os.path.join(out_dir, "sample.csv"))


if __name__ == "__main__":
    main()
