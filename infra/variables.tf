variable "aws_region" {
  description = "AWS region for provisioned resources."
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Project name used for naming and tagging resources."
  type        = string
  default     = "proto-dw"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"
}

variable "raw_data_bucket_name" {
  description = "S3 bucket name for raw extracted data."
  type        = string
  default     = "proto-dw-raw-data"
}
