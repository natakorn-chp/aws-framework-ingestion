
import sys
import json
import logging

from framework.utility.functions.func_get_class import get_class_by_name
from framework.utility.common.file_reader import read_input_config
from framework.modules.pipeline.ingestion_pipeline import IngestionPipeline
from framework.modules.job.job_input_parameters import JobParameters,JobInfoParameters

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(name)s - %(message)s')
logging.getLogger(__name__)

def entrypoint():
    read_mode = None
    try:
        try:
            from awsglue.utils import getResolvedOptions

            logging.info(f"Start calling by AWS Glue Job")
            args = getResolvedOptions(sys.argv, ['job_input_params'])
            job_input_params = json.loads(args['job_input_params'])

        except Exception as e:
            logging.info(f"Start calling by local script")
            read_mode = "local"
            job_input_params = {
                "env": "dev",
                "ingest_dt": "2025-05-12",
                "job_config_name": {
                    "file_name": "s3://iceberg-bucket-tutorial/config_ingest_order_detail.json",
                    "local_file_name": rf"<local_path>\aws-framework-pipeline\test\dummy_inputs\config_ingest_order_detail.json"
                }
            }

        job_params = JobParameters(**job_input_params)

        config_info = read_input_config(replace_set=job_params, \
                                            bucket_name=job_params.job_config_name['bucket_name'], \
                                            key_name=job_params.job_config_name['key_name'], \
                                            local_file_name=job_params.job_config_name['local_file_name'], \
                                            mode=read_mode)

        job_params.job_info = JobInfoParameters(**config_info['job_info'])

        logging.info(f"Start calling the pipeline")
        pipe_cls = get_class_by_name(__name__, config_info['pipeline_name'])
        b = pipe_cls(job_params=job_params, config=config_info)
        b.execute()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    entrypoint()
