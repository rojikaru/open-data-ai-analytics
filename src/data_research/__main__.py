import os
import sys

from src.constants import DATASET_URL
from src.data_load import load_data
from src.analysis import most_common_vehicle_type, vehicle_ownership_by_region


def main():
    out_dir = os.path.join("artifacts", "data_research")
    os.makedirs(out_dir, exist_ok=True)

    df = load_data(DATASET_URL, clear_cache=False)
    if isinstance(df, Exception):
        print(f"Failed to load data: {df}", file=sys.stderr)
        sys.exit(1)

    vehicle_type, count = most_common_vehicle_type(df)
    summary = f"Most common vehicle type: {vehicle_type} ({count} registrations)\n"
    print(summary)
    with open(os.path.join(out_dir, "most_common_vehicle.txt"), "w") as f:
        f.write(summary)

    ownership = vehicle_ownership_by_region(df)
    print("Vehicle ownership by region:")
    print(ownership)
    ownership.write_csv(os.path.join(out_dir, "ownership_by_region.csv"))


if __name__ == "__main__":
    main()
