
from pyspark.sql import SparkSession, DataFrame


def read_table_spark(spark: SparkSession, table_name: str, read_cond: str) -> DataFrame:

    if read_cond:
        df = spark.read.table(table_name).where(read_cond)
    else:
        df = spark.read.table(table_name)
    
    return df