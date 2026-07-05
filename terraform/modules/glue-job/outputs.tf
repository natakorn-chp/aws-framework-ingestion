output "glue_job_name" {
  description = "Name of the created Glue job"
  value       = aws_glue_job.this.name
}

output "glue_job_arn" {
  description = "ARN of the created Glue job"
  value       = aws_glue_job.this.arn
}
