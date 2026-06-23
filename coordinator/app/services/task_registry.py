from uuid import uuid4
from datetime import datetime, UTC

from app.db.models.task import Task
from app.models.enums import TaskStatus, TaskType

class TaskRegistry:
    def __init__(self, repository):
        self.repository = repository

    def create_task(self, task_type:TaskType, payload:dict):
        task = Task(
            task_id=str(uuid4()),
            task_type=task_type,
            status=TaskStatus.CREATED,
            worker_id=None,
            payload=payload,
            result=None,
            error_message=None,
            created_at=datetime.now(UTC),
            started_at=None,
            completed_at=None
        )
        self.repository.save(task)
        return self.repository.get(task.task_id)