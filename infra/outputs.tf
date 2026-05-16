output "aws_region" {
  description = "AWS region used by the provider."
  value       = var.aws_region
}

output "project_name" {
  description = "Project name used for tags and naming."
  value       = var.project_name
}

output "environment" {
  description = "Deployment environment name."
  value       = var.environment
}

output "raw_data_bucket_name" {
  description = "Name of the S3 bucket for raw extracted data."
  value       = aws_s3_bucket.raw_data.bucket
}

output "raw_data_bucket_arn" {
  description = "ARN of the S3 bucket for raw extracted data."
  value       = aws_s3_bucket.raw_data.arn
}
