# Changelog

v0.1.0

## Added

- Added docker-compose file with Postgres database for local development.

## Changed

- Updated the dbt dev profile to connect to the local Postgres database.

## Fixed

- Filtered null IDs from the starter dbt model so its not-null tests pass.
