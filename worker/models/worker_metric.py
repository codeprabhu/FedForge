from pydantic import BaseModel, Field

class WorkerMetrics(BaseModel):
    cpu_percent: float = Field(ge = 0, le = 100)
    memory_percent: float = Field(ge = 0, le = 100)
    disk_percent: float = Field(ge = 0, le = 100)