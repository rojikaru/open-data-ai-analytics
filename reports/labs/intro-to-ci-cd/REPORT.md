# Report: Intro to CI/CD pipelines on GitHub Actions

[This repository on GitHub](https://github.com/rojikaru/open-data-ai-analytics)

## What I learned

- **CI/CD basics**: A CI/CD pipeline automates the build, test, and deployment
  cycle so that every code change is verified consistently without manual steps.

- **GitHub Actions concepts**:
  - **Workflow** — a YAML file in `.github/workflows/` describing when and how
    jobs run.
  - **Job** — an isolated execution unit that runs on a runner (virtual machine
    or self-hosted machine). Jobs within the same workflow run in parallel by
    default; `needs:` creates explicit sequencing.
  - **Step** — a single shell command or reusable Action inside a job.
  - **Matrix strategy** — lets one job definition fan out into many parallel
    jobs by substituting each value from the matrix (e.g. one job per module).
  - **Artifacts** — files produced by a job that can be uploaded with
    `actions/upload-artifact` and downloaded by later jobs or inspected after
    the run completes.
  - **Path filters** (`dorny/paths-filter`) — detect which source paths changed
    in a push/pull_request so only the affected modules are re-run, saving
    runner minutes.

- **`matrix` context limitation**: The `matrix` context is only available
  inside step-level expressions, not in a job-level `if:`. The correct pattern
  is to compute a JSON array in an earlier job and pass it via `needs` outputs,
  then use `fromJson()` to drive the matrix — the job-level `if:` can then
  simply check whether the array is non-empty.

- **`actions/cache` vs artifacts for intra-run sharing**: `actions/cache` is
  designed to share data *across* runs, not *within* the same run. Parallel
  matrix cells all restore before any of them saves, so they cannot share a
  cache entry created in that same run. Uploading the data as a workflow
  artifact and downloading it in each matrix cell is the correct approach for
  sharing data within a single workflow run.

- **Self-hosted runners**: A self-hosted runner is a machine you register with
  your GitHub repository (Settings → Actions → Runners). It executes jobs with
  the `runs-on: [self-hosted, linux]` label, using the system Python and pip
  instead of the cloud environment's toolchain. This is useful for jobs that
  need local resources (persistent dataset cache, GPUs, internal network access)
  or to avoid cloud runner minutes.

## What I have done

### 1. Split the monolithic script into runnable modules (`99ea141`)

`src/data_load.py` was converted into a proper Python package
(`src/data_load/__init__.py`) so it can be invoked with `python -m src.data_load`.
Three new sibling packages were created, each with an `__init__.py` and a
`__main__.py` entry-point:

| Module | `__main__.py` produces |
| --- | --- |
| `src/data_load` | Downloads the dataset; writes `artifacts/data_load/sample.csv` (first 1 000 rows) |
| `src/data_quality_analysis` | Writes `quality_report.csv` (column statistics) and `null_counts.csv` |
| `src/data_research` | Writes `most_common_vehicle.txt` and `ownership_by_region.csv` |
| `src/visualization` | Renders and saves `ownership_by_region.png` (matplotlib/seaborn bar chart, headless Agg backend) |

The path resolution inside `load_data()` was also fixed: after the rename from
`src/data_load.py` to `src/data_load/__init__.py` the `__file__` depth
increased by one level, so the relative `..` path to the project root became
`../..`.

### 2. Cloud CI workflow (`5491479`) — `.github/workflows/ci.yml`

A three-job pipeline was configured for `push` and `pull_request` to `main`,
as well as manual `workflow_dispatch`:

```plaintext
detect-changes  →  download-dataset  →  run-modules (matrix)
```

- **`detect-changes`**: Uses `dorny/paths-filter` to detect which of the four
  modules have changed source files. Emits a JSON array (e.g.
  `["data_load","data_research"]`) so only the affected modules enter the
  matrix. For `workflow_dispatch` the array is built from the `module` input
  instead.

- **`download-dataset`**: Runs `uv run -m src.data_load` once to fetch
  `data/raw`, then uploads it as the `dataset-raw` workflow artifact
  (`retention-days: 1`). This avoids redundant downloads in parallel matrix
  cells — a pattern that `actions/cache` cannot provide within a single run.

- **`run-modules`**: Fan-out matrix over the JSON array from `detect-changes`.
  Each cell downloads `dataset-raw`, runs `uv run -m src.<module>`, and
  uploads its `artifacts/<module>/` directory. `fail-fast: false` lets
  unrelated modules complete even if one fails.

### 3. Self-hosted CI workflow (`3cdc71f`) — `.github/workflows/ci-selfhosted.yml`

A manual-only (`workflow_dispatch`) workflow for a locally registered runner
labelled `[self-hosted, linux]`:

```plaintext
resolve-modules  →  run-local (matrix)
```

- **`resolve-modules`**: Runs on the GitHub-hosted `ubuntu-latest` because the
  self-hosted runner may be offline. Converts the `module` input into the same
  JSON array pattern.
- **`run-local`**: Uses system `python3` and `pip install -e .` instead of
  `uv`, sets `MPLBACKEND=Agg` for headless plotting, and reuses any dataset
  already present in the workspace between runs.

### 4. Fix Node.js 20 deprecation (`f153414`)

Upgraded `actions/checkout` from `@v4` to `@v6` in both workflows to silence
the GitHub warning about the action's bundled Node.js 20 runtime being
deprecated.

## Output of the `git log --oneline --graph --all` command

```plaintext
* f153414 (HEAD -> feat/ci-cd, origin/feat/ci-cd) fix(ci): node.js 20 deprecation in actions/checkout
* 3cdc71f feat(ci): configure self-host runner
* 5491479 feat(ci): configure cloud runner
* 99ea141 feat: split up project execution steps
* 3f60b54 (origin/main, origin/HEAD, main) refactor: improve error handling and documentation in data loading functions
```
