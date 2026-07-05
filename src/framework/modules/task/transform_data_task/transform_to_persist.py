
import logging
import boto3
from pydantic import BaseModel
from pyspark.sql import SparkSession, DataFrame
from framework.modules.task.base_task import BaseTask
from framework.utility.common.file_reader import read_input_config
from framework.utility.common.sql import execute_sql

log = logging.getLogger("TransformDataToPersistTable")

class IngestionSpec(BaseModel):
    job_info: dict
    column_info: list

class TransformDataToPersistTableTemplate(BaseModel):
    local_file_name: str
    target_bucket_file: str
    target_key_file: str

class TransformDataToPersistTable(BaseTask):
    parameter_config_model = TransformDataToPersistTableTemplate

    def __init__(self, job_params: dict, parameters: dict, spark: SparkSession, s3_cli: boto3):
        self.spark = spark
        self.s3_cli = s3_cli
        self.ingest_spec_info = None
        super().__init__(job_params, parameters)

    def read_ingest_spec_config(self):
        read_mode =  None
        try:
            log.info("read_ingest_spec_config by AWS Glue Job")
            ingest_spec_info = read_input_config(self.job_params,
                                                bucket_name=self.parameters.target_bucket_file,
                                                key_name=self.parameters.target_key_file,
                                                local_file_name=self.parameters.local_file_name,
                                                mode=read_mode,
                                                s3_cli=self.s3_cli)            

        except Exception as e:
            log.error(f"Error reading ingest spec config: {e}")
            log.info("read_ingest_spec_config by local script")
            read_mode = 'local'
            ingest_spec_info = read_input_config(self.job_params,
                                                bucket_name=None,
                                                key_name=None,
                                                local_file_name=self.parameters.local_file_name,
                                                mode=read_mode)

        self.ingest_spec_info = IngestionSpec(**ingest_spec_info)

    def generate_sql_statement(self, raw_df: DataFrame) -> str:

        raw_df.createOrReplaceTempView("raw_to_tran_df")    

        column_cast_template = "CAST({{column_logic}} AS {{dtype}}) AS {{alias_name}}"
        sql_select_stament = "SELECT "
        sql_from_statment = "\nFROM raw_to_tran_df"
        sql_statment = ""

        cnt = 0
        for val in self.ingest_spec_info.column_info:
            dtype = val.get('data_type').lower()
            alias_name = val.get('column_name')
            column_logic = val.get('column_name') if val.get('column_logic') is None else val.get('column_logic').lower()

            if cnt == len(self.ingest_spec_info.column_info) - 1:
                sql_statment = sql_statment + column_cast_template.replace("{{column_logic}}", column_logic) \
                                                            .replace("{{dtype}}", dtype) \
                                                            .replace("{{alias_name}}", alias_name)
            else:
                sql_statment = sql_statment + column_cast_template.replace("{{column_logic}}", column_logic) \
                                                            .replace("{{dtype}}", dtype) \
                                                            .replace("{{alias_name}}", alias_name).rstrip(',') + ",\n"
            
            cnt += 1

        sql_statment = sql_select_stament + sql_statment + sql_from_statment
        log.info(f"Generated SQL statement: {sql_statment}")
        return sql_statment

    def execute(self, raw_df: DataFrame) -> DataFrame:
        log.info("Executing TransformDataToPersistTable")
        # read config
        self.read_ingest_spec_config()
        # execute sql statement
        tran_raw_df = execute_sql(spark=self.spark, sql_statement=self.generate_sql_statement(raw_df))

        return tran_raw_df