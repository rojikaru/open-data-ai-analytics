import matplotlib

matplotlib.use("Agg")  # non-interactive backend — must be set before importing pyplot

import matplotlib.pyplot as plt
import os
import sys

import seaborn as sns

from src.constants import ARTIFACTS_ROOT, DB_PATH, DB_TABLE
from src.analysis import most_common_vehicle_type, vehicle_ownership_by_region
from src.db import load_table_from_sqlite


def main():
    out_dir = os.path.join(ARTIFACTS_ROOT, "visualization")
    os.makedirs(out_dir, exist_ok=True)

    try:
        df = load_table_from_sqlite(DB_TABLE, db_path=DB_PATH)
    except Exception as ex:
        print(f"Failed to load data from DB: {ex}", file=sys.stderr)
        sys.exit(1)

    if df.height == 0:
        print("No data found in database table", file=sys.stderr)
        sys.exit(1)

    ownership = vehicle_ownership_by_region(df)
    ownership_pd = ownership.sort("HUMAN_REGION").to_pandas()

    _, ax = plt.subplots(figsize=(16, 6))
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

    if "KIND" in df.columns:
        top_vehicle_kinds = (
            df.group_by("KIND")
            .len()
            .sort("len", descending=True)
            .head(10)
            .to_pandas()
        )

        _, ax2 = plt.subplots(figsize=(12, 6))
        sns.barplot(data=top_vehicle_kinds, x="KIND", y="len", ax=ax2)
        sns.despine()
        ax2.set_xlabel("Vehicle type")
        ax2.set_ylabel("Registrations")
        ax2.set_title("Top 10 vehicle types")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        out_path_2 = os.path.join(out_dir, "top_vehicle_types.png")
        plt.savefig(out_path_2, dpi=150, bbox_inches="tight")
        print(f"Plot saved to {out_path_2}")

    top_type, top_count = most_common_vehicle_type(df)
    with open(os.path.join(out_dir, "visualization_summary.txt"), "w", encoding="utf-8") as file_obj:
        file_obj.write(
            f"DB: {DB_PATH}\nTable: {DB_TABLE}\nMost common vehicle type: {top_type} ({top_count})\n"
        )


if __name__ == "__main__":
    main()
