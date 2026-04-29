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

## Cloud Deployment (AWS via Terraform)

### Prerequisites

- An AWS account with programmatic access
- The project pushed to a **public** GitHub repository

### Steps

1. Open [AWS CloudShell](https://console.aws.amazon.com/cloudshell) or use a local terminal with AWS CLI configured.

2. Install Terraform if not present:

   ```bash
   curl -fsSL https://releases.hashicorp.com/terraform/1.8.5/terraform_1.8.5_linux_amd64.zip -o tf.zip
   unzip tf.zip && sudo mv terraform /usr/local/bin/
   ```

3. Clone this repository:

   ```bash
   git clone https://github.com/rojikaru/open-data-ai-analytics
   cd open-data-ai-analytics/infra/terraform
   ```

4. Create variables file:

   ```bash
   cat > terraform.tfvars <<EOF
   repo_url             = "https://github.com/rojikaru/open-data-ai-analytics"
   admin_ssh_public_key = "$(cat ~/.ssh/id_ed25519.pub)"
   EOF
   ```

5. Initialize and apply:

   ```bash
   terraform init
   terraform validate
   terraform plan
   terraform apply
   ```

6. After apply completes, copy the `app_url` output and open it in a browser.
   The VM runs cloud-init on first boot — wait ~5 minutes for Docker to install and containers to start.

7. Verify:

   ```bash
   curl $(terraform output -raw app_url)/health
   # Expected: {"status":"ok"}
   ```

8. **After your demo, destroy all resources** to avoid charges:

   ```bash
   terraform destroy
   ```

### AWS Resources Created

| Resource | Purpose |
|---|---|
| Key Pair | SSH public key for VM access |
| Security Group | Opens TCP 22 (SSH) and TCP 8000 (web) |
| EC2 Instance (t3.medium, Ubuntu 24.04) | Runs Docker Compose pipeline |
| Elastic IP | Static public IP address |

## References

- [GitHub - github/gitignore: A collection of useful .gitignore templates](https://github.com/github/gitignore)
- [uv project manager](https://docs.astral.sh/uv/#installation)
- [Data.gov.ua - Open Data Portal of Ukraine](https://data.gov.ua/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
