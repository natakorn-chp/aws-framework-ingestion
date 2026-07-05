variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
}

variable "project_name" {
  description = "Org/project label used for tagging and naming conventions"
  type        = string
  default     = "glue-tutorial"
}
