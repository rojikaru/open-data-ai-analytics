import csv
import json
import os
import sqlite3
import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prometheus_client import Counter, Histogram, make_asgi_app

ARTIFACTS_ROOT = Path(os.getenv("ARTIFACTS_ROOT", "/app/artifacts"))
ARTIFACTS_ROOT.mkdir(parents=True, exist_ok=True)

DB_PATH = Path(os.getenv("DB_PATH", "/app/db/app.db"))
DB_TABLE = os.getenv("DB_TABLE", "vehicles")

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["endpoint"],
)

app = FastAPI(title="Open Data AI Analytics")
app.mount("/static", StaticFiles(directory="web/static"), name="static")
app.mount("/artifacts", StaticFiles(directory=str(ARTIFACTS_ROOT)), name="artifacts")
app.mount("/metrics", make_asgi_app())
templates = Jinja2Templates(directory="web/templates")


def read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return "Not available yet"
    return path.read_text(encoding="utf-8")


def read_json_if_exists(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_preview(path: Path, limit: int = 20) -> list[dict]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8", newline="") as file_obj:
        reader = csv.DictReader(file_obj)
        rows = []
        for idx, row in enumerate(reader):
            if idx >= limit:
                break
            rows.append(row)
    return rows


def db_preview(limit: int = 20) -> list[dict]:
    if not DB_PATH.exists():
        return []

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM "{DB_TABLE}" LIMIT ?', (limit,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except Exception:
        return []
    finally:
        conn.close()


@app.get("/health", response_class=JSONResponse)
def health() -> dict:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    t0 = time.perf_counter()
    data_load_dir = ARTIFACTS_ROOT / "data_load"
    quality_dir = ARTIFACTS_ROOT / "data_quality_analysis"
    research_dir = ARTIFACTS_ROOT / "data_research"
    visualization_dir = ARTIFACTS_ROOT / "visualization"

    context = {
        "project_description": "Containerized analytics pipeline for open transport registry data.",
        "ingestion_summary": read_json_if_exists(data_load_dir / "ingestion_summary.json"),
        "sample_data": read_csv_preview(data_load_dir / "sample.csv"),
        "quality_summary": read_json_if_exists(quality_dir / "quality_summary.json"),
        "null_counts_preview": read_csv_preview(quality_dir / "null_counts.csv"),
        "research_summary": read_json_if_exists(research_dir / "research_summary.json"),
        "research_text": read_text_if_exists(research_dir / "most_common_vehicle.txt"),
        "research_regions_preview": read_csv_preview(research_dir / "ownership_by_region.csv"),
        "db_rows_preview": db_preview(),
        "plots": [
            {
                "title": "Vehicle ownership by region",
                "path": "/artifacts/visualization/ownership_by_region.png",
                "exists": (visualization_dir / "ownership_by_region.png").exists(),
            },
            {
                "title": "Top vehicle types",
                "path": "/artifacts/visualization/top_vehicle_types.png",
                "exists": (visualization_dir / "top_vehicle_types.png").exists(),
            },
        ],
    }

    response = templates.TemplateResponse(request, "index.html", context)
    REQUEST_LATENCY.labels(endpoint="/").observe(time.perf_counter() - t0)
    REQUEST_COUNT.labels(method="GET", endpoint="/", status=200).inc()

    return response
