

import logging
from pyspark.sql import SparkSession
from pydantic import BaseModel
from framework.modules.task.base_task import BaseTask
from framework.utility.common.table_reader import read_table_spark

log = logging.getLogger("ReadFromRawTable")

class ReadFromRawTableParam(BaseModel):
    raw_table_name: str
    read_condition: str

class ReadFromRawTable(BaseTask):
    parameter_config_model = ReadFromRawTableParam
    def __init__(self, job_params: dict, parameters: dict, spark: SparkSession):
        self.spark = spark
        super().__init__(job_params, parameters)
    
    def execute(self) -> None:
        log.info("Executing ReadFromRawTable with parameters")

        try:
            raw_df = read_table_spark(spark=self.spark,
                                    table_name=self.parameters.raw_table_name,
                                    read_cond=self.parameters.read_condition)
        except Exception as e:
            log.error(f"Failed to read from raw table {self.parameters.raw_table_name}: {e}")
            raise
    
        return raw_df