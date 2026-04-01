import os
import sqlite3
from typing import Any

import polars as pl

from src.constants import DB_PATH


def resolve_db_path() -> str:
    return os.getenv("DB_PATH", DB_PATH)


def ensure_db_parent_dir(db_path: str) -> None:
    parent_dir = os.path.dirname(db_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)


def _sqlite_type(dtype: pl.DataType) -> str:
    if dtype in (
        pl.Int8,
        pl.Int16,
        pl.Int32,
        pl.Int64,
        pl.UInt8,
        pl.UInt16,
        pl.UInt32,
        pl.UInt64,
        pl.Boolean,
    ):
        return "INTEGER"
    if dtype in (pl.Float32, pl.Float64):
        return "REAL"
    return "TEXT"


def _create_table_sql(df: pl.DataFrame, table_name: str) -> str:
    columns = []
    for name, dtype in zip(df.columns, df.dtypes, strict=False):
        columns.append(f'"{name}" {_sqlite_type(dtype)}')
    columns_sql = ", ".join(columns)
    return f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_sql})'


def write_dataframe_to_sqlite(
    df: pl.DataFrame,
    table_name: str,
    db_path: str | None = None,
    replace: bool = True,
) -> int:
    target_db = db_path or resolve_db_path()
    ensure_db_parent_dir(target_db)

    conn = sqlite3.connect(target_db)
    try:
        cur = conn.cursor()
        if replace:
            cur.execute(f'DROP TABLE IF EXISTS "{table_name}"')

        cur.execute(_create_table_sql(df, table_name))

        placeholders = ", ".join("?" for _ in df.columns)
        quoted_columns = ", ".join(f'"{col}"' for col in df.columns)
        insert_sql = (
            f'INSERT INTO "{table_name}" ({quoted_columns}) VALUES ({placeholders})'
        )

        rows_iter = (tuple(row) for row in df.iter_rows())
        cur.executemany(insert_sql, rows_iter)
        conn.commit()

        return df.height
    finally:
        conn.close()


def load_table_from_sqlite(
    table_name: str,
    db_path: str | None = None,
) -> pl.DataFrame:
    target_db = db_path or resolve_db_path()
    conn = sqlite3.connect(target_db)
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM "{table_name}"')
        rows = cur.fetchall()

        cur.execute(f'PRAGMA table_info("{table_name}")')
        columns = [row[1] for row in cur.fetchall()]

        if not rows:
            return pl.DataFrame(schema=columns)

        frame = pl.DataFrame(rows, schema=columns, orient="row")

        numeric_candidates = ["OPER_CODE", "REG_ADDR_KOATUU"]
        for col in numeric_candidates:
            if col in frame.columns:
                frame = frame.with_columns(pl.col(col).cast(pl.Int64, strict=False))

        return frame
    finally:
        conn.close()


def fetch_row_count(table_name: str, db_path: str | None = None) -> int:
    target_db = db_path or resolve_db_path()
    conn = sqlite3.connect(target_db)
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        result: Any = cur.fetchone()
        if result is None:
            return 0
        return int(result[0])
    finally:
        conn.close()
