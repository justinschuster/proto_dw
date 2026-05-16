# Infrastructure

Terraform infrastructure for this project lives in this directory.

## Backend

Terraform state is stored in the S3 bucket `proto-dw-infra` with the state key `proto-dw/terraform.tfstate` in `us-east-2`.

No DynamoDB lock table is configured.

## AWS Provider

The AWS provider defaults to `us-east-2`. Override `aws_region` in a local `.tfvars` file if a different region is needed.

## Raw Data Bucket

The `raw_data_bucket_name` variable configures the S3 bucket used to store raw data extracted by pipelines. It defaults to `proto-dw-raw-data`.

The bucket is private, blocks public access, enables server-side encryption, enables versioning, and disables ACLs with bucket-owner-enforced ownership.

## Usage

AWS credentials must have access to the S3 backend bucket before initializing Terraform.

Run Terraform checks after modifying infrastructure code:

```bash
make terraform-check
```

Individual commands are also available:

```bash
make terraform-fmt
make terraform-init
make terraform-validate
```
