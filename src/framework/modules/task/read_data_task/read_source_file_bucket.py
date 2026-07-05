

import logging
from pyspark.sql import SparkSession
from pydantic import BaseModel

from framework.modules.task.base_task import BaseTask
from framework.utility.common.file_reader import read_file_spark

log = logging.getLogger("ReadSourceFileBucket")

class ReadSourceFileBucketParam(BaseModel):
    format: str
    reader_options: dict

class ReadSourceFileBucket(BaseTask):

    parameter_config_model = ReadSourceFileBucketParam 

    def __init__(self, job_params: dict, parameters: dict, spark: SparkSession):
        self.spark = spark
        super().__init__(job_params, parameters)

    def execute(self, source_file_path: str):
        log.info(f"Executing ReadSourceFileBucket with parameters")

        try:
            src_df = read_file_spark(
                        spark=self.spark,
                        file_path=source_file_path,
                        file_format=self.parameters.format,
                        reader_options=self.parameters.reader_options
                    )
            log.info(f"File read successfully from {source_file_path}")
        except Exception as e:
            log.error(f"Error reading file from {source_file_path}: {e}")
            raise


        return src_df