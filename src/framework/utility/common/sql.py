
from pyspark.sql import SparkSession, DataFrame


def execute_sql(spark: SparkSession, sql_statement: str) -> DataFrame:

    result_df = spark.sql(sql_statement)

    return result_df
