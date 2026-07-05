resource "aws_glue_job" "this" {
  name              = var.job_name
  role_arn          = var.glue_role_arn
  glue_version      = var.glue_version
  worker_type       = var.worker_type
  number_of_workers = var.number_of_workers
  max_retries       = var.max_retries
  timeout           = var.timeout_minutes

  execution_property {
    max_concurrent_runs = var.max_concurrent_runs
  }

  command {
    name            = "glueetl"
    script_location = "s3://${var.script_bucket}/${var.script_key}"
    python_version  = "3"
  }

  default_arguments = merge(
    {
      "--job-language"                     = "python"
      "--TempDir"                          = "s3://${var.script_bucket}/temporary/"
      "--spark-event-logs-path"            = "s3://${var.script_bucket}/sparkHistoryLogs/"
      "--enable-metrics"                   = "true"
      "--enable-continuous-cloudwatch-log" = "true"
      "--enable-observability-metrics"     = tostring(var.enable_observability_metrics)
      "--enable-glue-datacatalog"          = tostring(var.enable_glue_datacatalog)
      "--enable-auto-scaling"              = tostring(var.enable_auto_scaling)
      "--job-bookmark-option"              = var.job_bookmark_option
      "--datalake-formats"                 = var.datalake_formats
    },
    var.additional_python_modules != "" ? { "--additional-python-modules" = var.additional_python_modules } : {},
    var.job_input_params != "" ? { "--job_input_params" = var.job_input_params } : {}
  )
}
