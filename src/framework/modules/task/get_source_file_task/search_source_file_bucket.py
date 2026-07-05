
import boto3
import logging
from pydantic import BaseModel
from botocore.exceptions import ClientError

from framework.modules.task.base_task import BaseTask

log = logging.getLogger("SearchSourceFileBucketParam")

class SearchSourceFileBucketParam(BaseModel):
    source_bucket_file: str
    source_key_file: str

class SearchSourceFileBucket(BaseTask):
    parameter_config_model = SearchSourceFileBucketParam 

    def __init__(self, job_params: dict, parameters: dict, s3_cli: boto3):
        self.s3_cli = s3_cli
        super().__init__(job_params, parameters)              

    def execute(self) -> None:
        log.info(f"Executing SearchSourceFileBucketParam with parameters")

        try:
            self.s3_cli.head_object(Bucket=self.parameters.source_bucket_file, Key=self.parameters.source_key_file)
            log.info(f"File '{self.parameters.source_key_file}' exists in bucket '{self.parameters.source_bucket_file}'")
        except ClientError as e:
            log.error(f"The finding source file in S3 bucket failed")
            raise Exception(f"Calling s3_cli failed {e}")
        except Exception as e:
            log.error(f"The finding source file in S3 bucket failed: {e}")
            raise Exception(f"File '{self.parameters.source_key_file}' does not exist in bucket '{self.parameters.source_bucket_file}'.")

        return f"s3://{self.parameters.source_bucket_file}/{self.parameters.source_key_file}"