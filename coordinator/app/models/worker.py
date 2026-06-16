from pydantic import BaseModel
from datetime import datetime
class WorkerRegistrationRequest(BaseModel):
    hostname: str
    ip : str

    cpu_cores: int
    memory_gb: int
    worker_version: str