variable "job_name" {
  description = "Name of the AWS Glue job resource"
  type        = string
}

variable "glue_version" {
  description = "AWS Glue version to run the job on"
  type        = string
  default     = "4.0"
}

variable "worker_type" {
  description = "Glue worker type (G.1X, G.2X, etc.)"
  type        = string
  default     = "G.1X"
}

variable "number_of_workers" {
  description = "Number of Glue workers to allocate"
  type        = number
  default     = 2
}

variable "max_retries" {
  description = "Number of retries on job failure"
  type        = number
  default     = 0
}

variable "timeout_minutes" {
  description = "Job timeout in minutes"
  type        = number
  default     = 10
}

variable "glue_role_arn" {
  description = "ARN of the pre-existing IAM role the Glue job assumes"
  type        = string
}

variable "script_bucket" {
  description = "Name of the pre-existing S3 bucket containing the Glue script"
  type        = string
}

variable "script_key" {
  description = "Key (path) of the Glue script object within script_bucket"
  type        = string
  default     = "scripts/glue_job_script.py"
}

variable "max_concurrent_runs" {
  description = "Maximum number of concurrent runs allowed for this job"
  type        = number
  default     = 1
}

variable "job_bookmark_option" {
  description = "Job bookmark setting: job-bookmark-enable, job-bookmark-disable, or job-bookmark-pause"
  type        = string
  default     = "job-bookmark-disable"
}

variable "enable_glue_datacatalog" {
  description = "Use the Glue Data Catalog as the Spark Hive metastore"
  type        = bool
  default     = true
}

variable "enable_auto_scaling" {
  description = "Enable Glue auto scaling (ETL auto tuning) for the job"
  type        = bool
  default     = true
}

variable "enable_observability_metrics" {
  description = "Enable enhanced observability metrics for the job"
  type        = bool
  default     = true
}

variable "datalake_formats" {
  description = "Comma-separated list of datalake formats to enable (e.g. iceberg)"
  type        = string
  default     = ""
}

variable "additional_python_modules" {
  description = "Comma-separated list of S3 paths to additional Python wheel/module dependencies"
  type        = string
  default     = ""
}

variable "job_input_params" {
  description = "JSON string passed to the job as the --job_input_params argument"
  type        = string
  default     = ""
}
