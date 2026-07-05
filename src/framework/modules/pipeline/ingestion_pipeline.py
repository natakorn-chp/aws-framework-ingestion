
import logging
from typing import Any
from pydantic import BaseModel
from pyspark.sql import DataFrame

from framework.modules.pipeline.base_pipeline import BasePipeline

log = logging.getLogger("IngestionPipeline")

class IngestionPipelineTasksTemplete(BaseModel):
    search_source_file_task: Any
    read_source_file_task: Any
    transform_to_raw_task: Any
    load_to_raw_task: Any
    read_from_raw_table_task: Any
    transform_to_persist_task: Any
    load_to_persist_task: Any

class IngestionPipeline(BasePipeline):
    def __init__(self, job_params: dict, config: dict):
        super().__init__(job_params, config, IngestionPipelineTasksTemplete)

    def execute_search_source_file_task(self) -> str:
        source_file_path = None
        task_param = self.pipeline_tasks.search_source_file_task
        if task_param.skip_flag == "False":
            x = task_param.module_name(job_params=self.job_params, 
                                        parameters=task_param.parameters,
                                        s3_cli=self.s3_cli)
            source_file_path = x.execute()

        return source_file_path

    def execute_read_source_file_task(self, source_file_path: str) -> DataFrame:
        src_df = None
        task_param = self.pipeline_tasks.read_source_file_task
        if task_param.skip_flag == "False" and source_file_path is not None:
            x = task_param.module_name(job_params=self.job_params, 
                                       parameters=task_param.parameters, 
                                       spark=self.spark)
            src_df = x.execute(source_file_path)

        return src_df
    
    def execute_transform_to_raw_task(self, src_df: DataFrame):
        tran_src_df = None
        task_param = self.pipeline_tasks.transform_to_raw_task
        if task_param.skip_flag == "False" and src_df is not None:
            x = task_param.module_name(job_params=self.job_params, 
                                       parameters=task_param.parameters, 
                                       spark=self.spark)
            tran_src_df = x.execute(src_df)

        return tran_src_df
    
    def execute_load_to_raw_table_task(self, src_df: DataFrame):
        task_param = self.pipeline_tasks.load_to_raw_task
        if task_param.skip_flag == "False" and src_df is not None:
            x = task_param.module_name(job_params=self.job_params, 
                                       parameters=task_param.parameters, 
                                       spark=self.spark)
            x.execute(src_df)     

    def execute_read_from_raw_table_task(self) -> DataFrame:
        raw_df = None
        task_param = self.pipeline_tasks.read_from_raw_table_task
        if task_param.skip_flag == "False":
            x = task_param.module_name(job_params=self.job_params, 
                                       parameters=task_param.parameters, 
                                       spark=self.spark)
            raw_df = x.execute()

        return raw_df  

    def execute_transform_to_persist_task(self, raw_df: DataFrame) -> DataFrame:
        tran_raw_df = None
        task_param = self.pipeline_tasks.transform_to_persist_task
        if task_param.skip_flag == "False" and raw_df is not None:
            x = task_param.module_name(job_params=self.job_params, 
                                       parameters=task_param.parameters, 
                                       spark=self.spark,
                                       s3_cli=self.s3_cli)
            tran_raw_df = x.execute(raw_df)   

        return tran_raw_df     

    def execute_load_to_persist_table_task(self, tran_raw_df: DataFrame):
        task_param = self.pipeline_tasks.load_to_persist_task
        if task_param.skip_flag == "False" and tran_raw_df is not None:
            x = task_param.module_name(job_params=self.job_params, 
                                       parameters=task_param.parameters, 
                                       spark=self.spark)
            x.execute(tran_raw_df)   
        
    def execute(self):
        log.info(f"Executing IngestionPipeline")

        source_file_path = self.execute_search_source_file_task()

        src_df = self.execute_read_source_file_task(source_file_path)

        tran_src_df = self.execute_transform_to_raw_task(src_df)

        self.execute_load_to_raw_table_task(tran_src_df)

        raw_df = self.execute_read_from_raw_table_task()

        tran_raw_df = self.execute_transform_to_persist_task(raw_df)

        self.execute_load_to_persist_table_task(tran_raw_df)



        

