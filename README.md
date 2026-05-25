# proto-dw

ETL code for common free data sources.

## Project Structure

- `extract/` contains extraction pipelines organized by data source.
- `dbt/` contains the dbt transformation project. Project configuration lives in `dbt/dbt_project.yml` and `dbt/profiles.yml`.
- `infra/` contains Terraform infrastructure.

## Prerequisites

- Python 3.13+
- `uv`
- `make`

## Common Commands

Install or refresh dependencies:

```bash
make sync
```

Run the standard local check suite:

```bash
make check
```

`make check` runs formatting checks, linting, type checks, and tests.

Run Terraform checks after modifying infrastructure code:

```bash
make terraform-check
```
