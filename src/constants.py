import os


RAW_DATA_ROOT = os.getenv("RAW_DATA_ROOT", "data/raw")
ARTIFACTS_ROOT = os.getenv("ARTIFACTS_ROOT", "artifacts")
DB_PATH = os.getenv("DB_PATH", "db/app.db")
DB_TABLE = os.getenv("DB_TABLE", "vehicles")
CSV_SEPARATOR = os.getenv("CSV_SEPARATOR", ";")
CSV_QUOTE_CHAR = os.getenv("CSV_QUOTE_CHAR", '"')
DATASET_URL = os.getenv(
	"DATASET_URL",
	"https://data.gov.ua/dataset/0ffd8b75-0628-48cc-952a-9302f9799ec0/resource/3f13166f-090b-499e-8e23-e9851c5a5f67/download/reestrtz2026.zip",
)
