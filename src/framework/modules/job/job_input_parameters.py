from pydantic import BaseModel


class JobInfoParameters(BaseModel):
    system_name: str
    catalog_name: str
    raw_database_name: str
    raw_table_name: str
    persist_database_name: str
    persist_table_name: str
    warehouse_name: str

class JobParameters(BaseModel):
    env: str
    ingest_dt: str
    job_config_name: dict
    ingest_yyyy: str = None
    ingest_mm: str = None
    ingest_dd: str = None
    job_info: JobInfoParameters = None

    def __init__(self, **data):
        super().__init__(**data)
        self.add_yyyy_mm_dd_params()
        self.add_job_config_bucket_key()

    def add_yyyy_mm_dd_params(self) -> None:
        if self.ingest_dt:
            self.ingest_yyyy = self.ingest_dt.split("-")[0]
            self.ingest_mm = self.ingest_dt.split("-")[1]
            self.ingest_dd = self.ingest_dt.split("-")[2]

    def add_job_config_bucket_key(self) -> None:
        self.job_config_name['bucket_name'] = self.job_config_name['file_name'].split("/")[2]
        self.job_config_name['key_name'] = "/".join(self.job_config_name['file_name'].split("/")[3:])

