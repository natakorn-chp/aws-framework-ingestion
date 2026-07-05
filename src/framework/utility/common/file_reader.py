
import logging
import json
import boto3
from botocore.exceptions import ClientError
from pyspark.sql import SparkSession, DataFrame

log = logging.getLogger("FileReader")

def replace_req_values(content: str, replace_set) -> str:

    modified_content = content.replace("{{env}}", replace_set.env) \
                            .replace("{{yyyy}}", replace_set.ingest_dt.split('-')[0]) \
                            .replace("{{mm}}", replace_set.ingest_dt.split('-')[1]) \
                            .replace("{{dd}}", replace_set.ingest_dt.split('-')[2])

    return modified_content

def read_input_config(replace_set, bucket_name: str, key_name: str, local_file_name: str=None, mode: str='aws', s3_cli: boto3=None) -> dict:
    data = None

    if mode == 'local':
        try:
            with open(local_file_name, 'r') as f:
                file_content = f.read()        

            replaced_file_content = replace_req_values(file_content, replace_set)
            data = json.loads(replaced_file_content)
        except FileNotFoundError:
            logging.error(f"the file '{local_file_name}' not found")
        except IOError as e:
            logging.error("An error occurred:", e)
    else:
        try:
            if s3_cli is None:
                s3_cli = boto3.client('s3')
            response = s3_cli.get_object(Bucket=bucket_name, Key=key_name)
            file_content = response['Body'].read().decode('utf-8')
            replaced_file_content = replace_req_values(file_content, replace_set)
            data = json.loads(replaced_file_content)
        except ClientError as e:
            logging.error(f"An AWS ClientError occurred: {e}")        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    return data

def read_file_spark(spark: SparkSession, file_path: dict, file_format: str, reader_options: dict) -> DataFrame:

    df = spark.read.format(file_format) \
            .options(**reader_options) \
            .load(file_path)
    
    return df
