
import logging
from pydantic import BaseModel
from pyspark.sql import DataFrame, SparkSession
from framework.modules.task.base_task import BaseTask
from framework.utility.common.sql import execute_sql

log = logging.getLogger("AddControlColumnsPartition")

class AddControlColumnsPartitionTemplate(BaseModel):
    add_system_columns: str
    partition_column: list

class AddControlColumnsPartition(BaseTask):

    parameter_config_model = AddControlColumnsPartitionTemplate
    def __init__(self, job_params: dict, parameters: dict, spark: SparkSession):
        self.spark = spark
        super().__init__(job_params, parameters)

    def add_control_columns(self, sql_statement: list) -> DataFrame:

        ctl_col_list = "current_timestamp() as load_tms"

        sql_statement.append(ctl_col_list)

        return sql_statement

    def add_partition_columns(self, sql_statement: list) -> DataFrame:

        column_template = "{{partition_logic}} as {{column_name}}"

        for val in self.parameters.partition_column:
            column_result = column_template.replace("{{partition_logic}}",val.get('partition_logic')) \
                            .replace("{{column_name}}",val.get('column_name'))

            sql_statement.append(column_result)

        return sql_statement
    
    def generate_sql_statement(self, sql_statement: str, src_df: DataFrame) -> str:

        src_df.createOrReplaceTempView("tran_df")

        sql_select_stament = "SELECT *\n,"
        sql_from_statment = "\nFROM tran_df"
        sql_statement_lst = []

        sql_statement_lst = self.add_control_columns(sql_statement_lst)
        sql_statement_lst = self.add_partition_columns(sql_statement_lst)

        sql_statement = '\n, '.join(sql_statement_lst)
        
        return sql_select_stament + sql_statement + sql_from_statment

    def execute(self, src_df: DataFrame) -> DataFrame:
        log.info("Executing AddControlColumnsPartition")
        sql_statement = ''
        sql_statement = self.generate_sql_statement(sql_statement, src_df)
        tran_df = execute_sql(self.spark, sql_statement)
        
        return tran_df
