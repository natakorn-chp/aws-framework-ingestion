import logging

log = logging.getLogger("BaseTask")

class BaseTask:
    def __init__(self, job_params: dict, parameters: dict):
        self.job_params = job_params
        self.parameters = parameters    