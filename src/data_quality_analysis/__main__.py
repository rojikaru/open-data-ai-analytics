import os
import sys
import json

import polars as pl

from src.constants import ARTIFACTS_ROOT, DB_PATH, DB_TABLE
from src.db import load_table_from_sqlite


def main():
    out_dir = os.path.join(ARTIFACTS_ROOT, "data_quality_analysis")
    os.makedirs(out_dir, exist_ok=True)

    try:
        df = load_table_from_sqlite(DB_TABLE, db_path=DB_PATH)
    except Exception as ex:
        print(f"Failed to load data from DB: {ex}", file=sys.stderr)
        sys.exit(1)

    if df.height == 0:
        print("No data found in database table", file=sys.stderr)
        sys.exit(1)

    describe = df.describe()
    print("Dataset description:")
    print(describe)
    describe.write_csv(os.path.join(out_dir, "quality_report.csv"))

    null_counts = df.null_count()
    print("\nNull counts per column:")
    print(null_counts)
    null_counts.write_csv(os.path.join(out_dir, "null_counts.csv"))

    duplicates_count = int(df.is_duplicated().sum())

    validity_checks = {}
    for col in ["OPER_CODE", "REG_ADDR_KOATUU"]:
        if col in df.columns:
            null_values = int(df.get_column(col).is_null().sum())
            casted_col = df.get_column(col).cast(pl.Int64, strict=False)
            casted_null_values = int(casted_col.is_null().sum())
            validity_checks[col] = {
                "total_values": df.height,
                "null_values": null_values,
                "non_numeric_values": max(casted_null_values - null_values, 0),
            }

    report_json = {
        "db_path": DB_PATH,
        "table": DB_TABLE,
        "rows": df.height,
        "columns": df.width,
        "duplicates": duplicates_count,
        "validity_checks": validity_checks,
    }

    with open(os.path.join(out_dir, "quality_summary.json"), "w", encoding="utf-8") as file_obj:
        json.dump(report_json, file_obj, indent=2)

    with open(os.path.join(out_dir, "duplicates.txt"), "w", encoding="utf-8") as file_obj:
        file_obj.write(f"Duplicate rows: {duplicates_count}\n")

    print(f"\nRows: {df.shape[0]}, Columns: {df.shape[1]}")


if __name__ == "__main__":
    main()
