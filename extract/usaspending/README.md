# USAspending Extract

This package contains the dlt extraction pipeline for USAspending.gov data as defined by `https://api.usaspending.gov/docs/endpoints`.

AWS credentials should come from `~/.aws/credentials`, environment variables, an IAM role, or non-committed dlt secrets.
The raw data bucket is defined in `./dlt/secrets.toml`.