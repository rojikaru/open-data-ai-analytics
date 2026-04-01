import os
import sys
import json

from src.constants import (
    ARTIFACTS_ROOT,
    DATASET_URL,
    DB_PATH,
    DB_TABLE,
    CSV_SEPARATOR,
    CSV_QUOTE_CHAR,
    DATA_LOAD_SAMPLE_SIZE,
)
from src.data_load import load_data
from src.db import write_dataframe_to_sqlite


def main():
    out_dir = os.path.join(ARTIFACTS_ROOT, "data_load")
    os.makedirs(out_dir, exist_ok=True)

    df = load_data(
        DATASET_URL,
        clear_cache=False,
        separator=CSV_SEPARATOR,
        quote_char=CSV_QUOTE_CHAR,
    )
    if isinstance(df, Exception):
        print(f"Failed to load data: {df}", file=sys.stderr)
        sys.exit(1)

    print(f"Shape: {df.shape}")
    print(df.head())
    df.head(DATA_LOAD_SAMPLE_SIZE).write_csv(os.path.join(out_dir, "sample.csv"))

    inserted_rows = write_dataframe_to_sqlite(df, table_name=DB_TABLE, db_path=DB_PATH)

    summary = {
        "dataset_url": DATASET_URL,
        "db_path": DB_PATH,
        "table": DB_TABLE,
        "rows_inserted": inserted_rows,
        "columns": len(df.columns),
    }
    summary_path = os.path.join(out_dir, "ingestion_summary.json")
    with open(summary_path, "w", encoding="utf-8") as file_obj:
        json.dump(summary, file_obj, indent=2)

    print(f"Data loaded into SQLite: {DB_PATH} ({inserted_rows} rows)")
    print(f"Ingestion summary saved to {summary_path}")


if __name__ == "__main__":
    main()
