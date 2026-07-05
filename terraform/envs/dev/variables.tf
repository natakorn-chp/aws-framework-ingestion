variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
}

variable "project_name" {
  description = "Org/project label used for tagging and naming conventions"
  type        = string
  default     = "glue-tutorial"
}

variable "glue_role_arn" {
  description = "ARN of the pre-existing IAM role the Glue job assumes"
  type        = string
}

variable "script_bucket" {
  description = "Name of the pre-existing S3 bucket containing the Glue script and artifacts"
  type        = string
}
