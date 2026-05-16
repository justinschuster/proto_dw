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
- `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`: Pull request template to use when opening PRs.

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
- Run a focused test:
  ```bash
  make typecheck
  ```

#### Coverage

- Generate coverage (fails if coverage drops below threshold):
  ```bash
  make coverage
  ```

#### Formatting, linting

- Formatting and linting use `ruff`; run `make format` (applies fixes) and `make lint` (checks only).
- Type hints must pass `make typecheck`.
- Write comments as full sentences ending with a period.
- Imports are managed by Ruff and should stay sorted.

#### Mandatory local run order

When `$code-change-verification` applies, run the full sequence in order (or use the skill scripts):

```bash
make format
make lint
make typecheck
make tests
```

#### Terraform

Terraform infrastructure lives in `infra/`.

When modifying Terraform code, run:

```bash
make terraform-check
```

### Utilities & Tips

- Install or refresh development dependencies:
  ```bash
  make sync
  ```
- Review `Makefile` for common commands and use `uv run` for Python invocations.

### Pull Request & Commit Guidelines

- Use the template at `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`; include a summary, test plan, and issue number if applicable.
- Add tests for new behavior when feasible and update documentation for user-facing changes.
- Run `make format`, `make lint`, `make typecheck`, and `make tests` before marking work ready.
- Commit messages should be concise and written in the imperative mood. Small, focused commits are preferred.

### Review Process & What Reviewers Look For

- ✅ Checks pass (`make format`, `make lint`, `make typecheck`, `make tests`).
- ✅ Tests cover new behavior and edge cases.
- ✅ Code is readable, maintainable, and consistent with existing style.
- ✅ Public APIs and user-facing behavior changes are documented.
- ✅ Examples are updated if behavior changes.
- ✅ History is clean with a clear PR description.
