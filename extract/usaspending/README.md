# USAspending Extract

This package contains the dlt extraction pipeline for USAspending.gov data.

The initial implementation loads Disaster Emergency Fund Code (DEFC) reference data from `https://api.usaspending.gov/api/v2/references/def_codes/` into the local Postgres destination configured by dlt in `.dlt/secrets.toml`.

The DEFC resource uses `code` as the primary key and `merge` write disposition so repeated runs are idempotent.

Run the extract with:

```bash
uv run python -m extract.usaspending.extract_usaspending
```

Run validation with:

```bash
uv run ruff check .
uv run pytest
```
