
import logging
from pydantic import BaseModel
from pyspark.sql import SparkSession, DataFrame
from framework.modules.task.base_task import BaseTask

log = logging.getLogger("FullDumpLoadTableTask")

class FullDumpLoadTableTemplate(BaseModel):
    target_table_name: str
    partition_column: str

class FullDumpLoadTable(BaseTask):
    parameter_config_model = FullDumpLoadTableTemplate
    def __init__(self, job_params: dict, parameters: dict, spark: SparkSession):
        self.spark = spark
        super().__init__(job_params, parameters)

    def execute(self, write_df: DataFrame) -> None:
        log.info("Executing FullDumpLoadTable with parameters")

        try:
            write_df.writeTo(self.parameters.target_table_name) \
                .partitionedBy(self.parameters.partition_column) \
                .overwritePartitions()
            log.info(f"Load to the target table {self.parameters.target_table_name} done")
        except Exception as e:
            log.error(f"Failed to load to the target table {self.parameters.target_table_name}: {e}")
            raise
