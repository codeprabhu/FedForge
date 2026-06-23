from pydantic import BaseModel

from app.models.enums import TaskType, TaskStatus

class CreateTaskRequest(BaseModel):
    task_type: TaskType
    payload: dict

class TaskResponse(BaseModel):
    task_id: str
    task_type: TaskType
    status: TaskStatus

    worker_id: str | None
    payload: dict
    result: dict | None
    error_message: str | None

    created_at: str
    assigned_at: str | None
    started_at: str | None
    completed_at: str | None