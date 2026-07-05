
import logging
import boto3
from typing import Any
from pydantic import BaseModel
from pyspark.sql import SparkSession

from framework.utility.functions.func_get_class import get_class_by_name
from framework.modules.task.get_source_file_task.search_source_file_bucket import SearchSourceFileBucket
from framework.modules.task.read_data_task.read_source_file_bucket import ReadSourceFileBucket
from framework.modules.task.read_data_task.read_from_raw_table import ReadFromRawTable
from framework.modules.task.load_to_table_task.fulldump_load_table_task import FullDumpLoadTable
from framework.modules.task.transform_data_task.transform_to_persist import TransformDataToPersistTable
from framework.modules.task.transform_data_task.add_ctl_col_partition import AddControlColumnsPartition
from framework.modules.job.job_input_parameters import JobParameters

log = logging.getLogger("base_pipeline")

class TaskConfigTemplate(BaseModel):
    module_name: str
    skip_flag: str
    parameters: dict

class PipelineConfigTemplate(BaseModel):
    pipeline_name: str
    job_info: dict
    tasks: dict[str, TaskConfigTemplate]

class BasePipeline:
    def __init__(self, job_params: JobParameters, config: dict, pipeline_task_model: Any):
        log.info('Loading pipeline tasks')
        self.job_params = job_params
        self.pipeline_config = PipelineConfigTemplate(**config)
        self.pipeline_tasks = pipeline_task_model(**self.pipeline_config.tasks)
        self.s3_cli = boto3.client('s3')
        self.spark = SparkSession.builder.appName("aws-framework-pipeline") \
                                            .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
                                            .config(f"spark.sql.catalog.{self.job_params.job_info.catalog_name}", "org.apache.iceberg.spark.SparkCatalog") \
                                            .config(f"spark.sql.catalog.{self.job_params.job_info.catalog_name}.warehouse", self.job_params.job_info.warehouse_name.replace("{{env}}", f"{self.job_params.env}")) \
                                            .config(f"spark.sql.catalog.{self.job_params.job_info.catalog_name}.catalog-impl", "org.apache.iceberg.aws.glue.GlueCatalog") \
                                            .config(f"spark.sql.catalog.{self.job_params.job_info.catalog_name}.io-impl", "org.apache.iceberg.aws.s3.S3FileIO") \
                                            .config("spark.sql.iceberg.handle-timestamp-without-timezone", "true") \
                                            .getOrCreate()

        for task_name, task_info in self.pipeline_config.tasks.items():
            module_cls = get_class_by_name(__name__,task_info.module_name)
            module_cls_parameters = module_cls.parameter_config_model(**task_info.parameters)

            task = getattr(self.pipeline_tasks, task_name)
            task.module_name = module_cls
            task.parameters = module_cls_parameters

        log.info('Done loading pipeline tasks')

    def set_spark_conf(self, conf_lst: dict):

        for key, value in conf_lst:
            self.spark.conf.set(key, value)
