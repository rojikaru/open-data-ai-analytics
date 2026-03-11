import matplotlib

matplotlib.use("Agg")  # non-interactive backend — must be set before importing pyplot

import matplotlib.pyplot as plt
import os
import sys

import seaborn as sns

from src.constants import DATASET_URL
from src.data_load import load_data
from src.analysis import vehicle_ownership_by_region


def main():
    out_dir = os.path.join("artifacts", "visualization")
    os.makedirs(out_dir, exist_ok=True)

    df = load_data(DATASET_URL, clear_cache=False)
    if isinstance(df, Exception):
        print(f"Failed to load data: {df}", file=sys.stderr)
        sys.exit(1)

    ownership = vehicle_ownership_by_region(df)
    ownership_pd = ownership.sort("HUMAN_REGION").to_pandas()

    fig, ax = plt.subplots(figsize=(16, 6))
    sns.barplot(data=ownership_pd, x="HUMAN_REGION", y="len", ax=ax)
    sns.despine()
    ax.set_xlabel("Region")
    ax.set_ylabel("Vehicles registered")
    ax.set_title("Vehicle ownership by region (UA, 2026)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    out_path = os.path.join(out_dir, "ownership_by_region.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Plot saved to {out_path}")


if __name__ == "__main__":
    main()
