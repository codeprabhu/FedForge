from fastapi import APIRouter # type:ignore
from fastapi import Depends # type: ignore
from fastapi import HTTPException # type: ignore

from app.models.task import CreateTaskRequest
from app.api.dependencies import get_task_registry
from app.services.task_registry import TaskRegistry

router = APIRouter()

@router.post("/tasks")
def create_task(payload: CreateTaskRequest,
                task_registry: TaskRegistry = Depends(get_task_registry)):
    task = task_registry.create_task(payload.task_type, payload.payload)
    return task

@router.get("/tasks")
def get_tasks(task_registry: TaskRegistry = Depends(get_task_registry)):
    return task_registry.repository.get_all()

@router.get("/tasks/{task_id}")
def get_task(task_id: str, task_registry: TaskRegistry = Depends(get_task_registry)):
    task = task_registry.repository.get(task_id)
    if task is None:
        raise HTTPException(status_code = 404, detail = "Task Not Found")
    return task
