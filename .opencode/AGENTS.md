# Contributor Guide

## Table of Contents

1. [Project Structure Guide](#project-structure-guide)
2. [Operation Guide](#operation-guide)

## Project Structure Guide

### Overview

This repository provides ETL code for common free data sources.

## Repo Structure & Important Files

- `extract/` - Contains all extraction pipelines. Organized in folders by data source name.
- `dbt/` - DBT project for all transformation logic.
- `dags/` - Airflow DAGs for orchestration.
- `pyproject.toml`, `uv.lock`: Python dependencies and tool configuration.
- `dbt/db_project.yaml`, `dbt/profiles.yaml`: DBT project configuration.

## Operation Guide

### Prerequisites

- Python 3.10+
- `uv` installed for dependency management (`uv sync`) and `uv run` for Python commands.
- `make` available to run repository tasks.

### Development Workflow

1. Sync with `main` and create a feature branch:
   ```bash
   git checkout -b feat/<short-description>
   ```
2. If dependencies changed or you are setting up the repo, run `make sync`.
3. Implement changes after adding or updating tests.

#### Unit tests and type checking

- Run the full test suite:
  ```bash
  make tests
  ```
- Run a focused test:
  ```bash
  uv run pytest -s -k <pattern>
  ```

#### Coverage

- Generate coverage (fails if coverage drops below threshold):
  ```bash
  make coverage
  ```

#### Formatting, linting, and type checking

- Formatting and linting use `ruff`; run `make format` (applies fixes) and `make lint` (checks only).
- Type hints must pass `make typecheck`.
- Write comments as full sentences ending with a period.
- Imports are managed by Ruff and should stay sorted.

#### Mandatory local run order

When `$code-change-verification` applies, run the full sequence in order (or use the skill scripts):

```bash
make format
make lint
make tests
```

### Utilities & Tips

- Install or refresh development dependencies:
  ```bash
  make sync
  ```
- Review `Makefile` for common commands and use `uv run` for Python invocations.
- Consult `tests/README.md` for test and snapshot workflows.
