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

## References

- [GitHub - github/gitignore: A collection of useful .gitignore templates](https://github.com/github/gitignore)
- [uv project manager](https://docs.astral.sh/uv/#installation)
- [Data.gov.ua - Open Data Portal of Ukraine](https://data.gov.ua/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
