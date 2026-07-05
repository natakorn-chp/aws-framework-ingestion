output "glue_job_name" {
  description = "Name of the framework-ingestion Glue job"
  value       = module.framework_ingestion.glue_job_name
}

output "glue_job_arn" {
  description = "ARN of the framework-ingestion Glue job"
  value       = module.framework_ingestion.glue_job_arn
}
