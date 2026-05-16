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
