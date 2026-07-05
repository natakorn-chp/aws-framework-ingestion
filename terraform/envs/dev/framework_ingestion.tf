module "framework_ingestion" {
  source = "../../modules/glue-job"

  job_name          = "terraform-framework-ingestion"
  glue_version      = "4.0"
  worker_type       = "G.1X"
  number_of_workers = 2
  max_retries       = 0
  timeout_minutes   = 2880

  glue_role_arn = var.glue_role_arn
  script_bucket = var.script_bucket
  script_key    = "scripts/framework-ingestion.py"

  max_concurrent_runs          = 1
  job_bookmark_option          = "job-bookmark-disable"
  enable_glue_datacatalog      = true
  enable_auto_scaling          = true
  enable_observability_metrics = true
  datalake_formats              = "iceberg"
  additional_python_modules     = "s3://natakorn-th-dev-artifacts/framework/ingestion/aws_framewwork_pipeline-0.1.0-py3-none-any.whl,s3://iceberg-bucket-tutorial/pydantic-2.11.7-py3-none-any.whl"
  job_input_params               = "{\"env\": \"dev\", \"ingest_dt\": \"2025-05-12\", \"job_config_name\": { \"file_name\": \"s3://natakorn-th-dev-artifacts/config_ingest/ntk/config_ingest_order_detail.json\", \"local_file_name\": \"None\" }}"
}
