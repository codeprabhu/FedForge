from pydantic import BaseModel, Field
class WorkerRegistrationRequest(BaseModel):
    hostname: str = Field(min_length= 1)
    ip : str = Field(min_length = 1)

    cpu_cores: int = Field(gt=0)
    memory_gb: int = Field(gt = 0)
    worker_version: str = Field(min_length = 1)