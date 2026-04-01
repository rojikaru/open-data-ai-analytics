import os
import sys
import json

from src.constants import ARTIFACTS_ROOT, DB_PATH, DB_TABLE
from src.analysis import most_common_vehicle_type, vehicle_ownership_by_region
from src.db import load_table_from_sqlite


def main():
    out_dir = os.path.join(ARTIFACTS_ROOT, "data_research")
    os.makedirs(out_dir, exist_ok=True)

    try:
        df = load_table_from_sqlite(DB_TABLE, db_path=DB_PATH)
    except Exception as ex:
        print(f"Failed to load data from DB: {ex}", file=sys.stderr)
        sys.exit(1)

    if df.height == 0:
        print("No data found in database table", file=sys.stderr)
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

    summary_json = {
        "db_path": DB_PATH,
        "table": DB_TABLE,
        "rows": df.height,
        "columns": df.width,
        "most_common_vehicle_type": vehicle_type,
        "most_common_vehicle_count": count,
        "regions_in_report": ownership.height,
    }
    with open(
        os.path.join(out_dir, "research_summary.json"),
        "w",
        encoding="utf-8",
    ) as file_obj:
        json.dump(summary_json, file_obj, indent=2)


if __name__ == "__main__":
    main()
