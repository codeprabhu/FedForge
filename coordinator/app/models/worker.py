from pydantic import BaseModel


class WorkerRegistrationRequest(BaseModel):
    hostname: str
    cpu_cores: int
    memory_gb: int
    worker_version: str