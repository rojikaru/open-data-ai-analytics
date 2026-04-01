# Open data AI analytics

This repository contains code and resources for analyzing open data using AI techniques. The goal is to provide insights and visualizations that can help understand trends and patterns in the data.

## Goal

The main goal of this project is to learn & experiment with git and uv. The code is not intended for production use, but rather as a learning exercise.

The codebase comprises a single script that performs data analysis on a dataset. For more info please refer to the [data README](data/README.md).

I would try to answer the following questions with my work in this repository:

1. What are the most common types of vehicles owned by individuals in the dataset?
2. How does vehicle ownership vary by region or city?
3. Are there any noticeable trends in vehicle ownership over time?

The questions are not exhaustive, and I may explore other aspects of the data as I work through the analysis.

## Project structure

The project is organized as follows:

```plaintext
open-data-ai-analytics/
├── data/
│   ├── raw/                # Raw data files (not tracked in git)
│   └── processed/          # Processed data files (not tracked in git)
├── src/                    # Source code for data analysis
├── notebooks/              # Jupyter notebooks for exploratory data analysis
├── reports/                # Generated reports and visualizations
├── .gitignore              # Git ignore file
├── pyproject.toml          # Project configuration file
├── LICENSE                 # License file
└── README.md               # Project documentation
```

## Getting Started

To get started, clone the repository and install the required dependencies using [uv](https://docs.astral.sh/uv/#installation):

```bash
uv sync
```

## Running the Code

You can run the main analysis script using:

```bash
uv run -m src.main
```

## Docker Workspace Run

The project includes a multi-container setup to run all modules in one local Docker workspace.

### Services

- `data_load`: downloads CSV, creates SQLite table, imports records.
- `data_quality_analysis`: computes missing values, duplicates and basic validity checks.
- `data_research`: computes basic statistics and research summaries.
- `visualization`: generates at least two plots.
- `web`: FastAPI + Jinja2 interface for data, reports and visualizations.

### Files added for containerization

- `compose.yaml`
- `src/data_load/Dockerfile`
- `src/data_quality_analysis/Dockerfile`
- `src/data_research/Dockerfile`
- `src/visualization/Dockerfile`
- `web/Dockerfile`
- `.env`

### One-command startup

Configuration template is available in `.env.example`.

```bash
docker compose up --build
```

After startup:

- Web UI: [http://localhost:8000](http://localhost:8000)
- Health endpoint: [http://localhost:8000/health](http://localhost:8000/health)

### Ports

- `8000/tcp` — web interface (`web` service).

### Example CSV file

- `data/raw/reestrtz2026/reestrtz01.01.2026.csv` (will be downloaded by `data_load` service on local run if not present).

### Data exchange strategy

- `data_load` writes source data into SQLite DB (`db/app.db`) and artifacts (`artifacts/data_load`).
- Analysis, research and visualization services read from SQLite and write their outputs into shared artifacts.
- The web service reads both SQLite and generated artifacts.

### Volumes and network

- `raw_data` volume: downloaded CSV files.
- `db_data` volume: SQLite database file.
- `artifacts_data` volume: reports and plots.
- `analytics_net` bridge network for all services.

### Expected outputs

- `artifacts/data_load/ingestion_summary.json`
- `artifacts/data_quality_analysis/quality_summary.json`
- `artifacts/data_quality_analysis/null_counts.csv`
- `artifacts/data_research/research_summary.json`
- `artifacts/visualization/ownership_by_region.png`
- `artifacts/visualization/top_vehicle_types.png`

### Stop and cleanup

```bash
docker compose down
```

To remove named volumes too:

```bash
docker compose down -v
```

## References

- [GitHub - github/gitignore: A collection of useful .gitignore templates](https://github.com/github/gitignore)
- [uv project manager](https://docs.astral.sh/uv/#installation)
- [Data.gov.ua - Open Data Portal of Ukraine](https://data.gov.ua/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
