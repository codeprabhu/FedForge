from uuid import uuid4
from datetime import datetime, UTC

from app.db.models.task import Task
from app.models.enums import TaskStatus, TaskType

class TaskRegistry:
    def __init__(self, repository):
        self.repository = repository

    def _get_task_or_raise(self, task_id : str):
        task = self.repository.get(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} DNE")
        return task
    
    def _transition(self, task, expected_status: TaskStatus, new_status: TaskStatus):
        if task.status != expected_status:
            raise ValueError(f"Cannot transition task from {task.status} to {new_status}")
        task.status = new_status

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
            assigned_at = None,
            started_at=None,
            completed_at=None
        )
        self.repository.save(task)
        return task
    
    def assign_task(self, task_id: str, worker_id: str):
        task= self._get_task_or_raise(task_id)
        self._transition(task, TaskStatus.CREATED, TaskStatus.ASSIGNED)

        task.worker_id = worker_id
        task.assigned_at = datetime.now(UTC)
        return task
    
    def start_task(self, task_id:str):
        task = self._get_task_or_raise(task_id)
        self._transition(task, TaskStatus.ASSIGNED, TaskStatus.RUNNING)
        
        task.started_at = datetime.now(UTC)
        return task
    
    def complete_task(self, task_id: str, result: dict):
        task = self._get_task_or_raise(task_id)
        self._transition(task, TaskStatus.RUNNING, TaskStatus.COMPLETED)

        task.result = result
        task.completed_at = datetime.now(UTC)
        return task
    
    def fail_task(self, task_id: str, error_message: str):
        task = self._get_task_or_raise(task_id)
        if task.status not in (TaskStatus.ASSIGNED, TaskStatus.RUNNING):
            raise ValueError(f"Cannot fail task from state {task.status}")
        
        task.status = TaskStatus.FAILED
        task.error_message = error_message
        task.completed_at = datetime.now(UTC)
        return task
    
    def assign_next_task(self, worker_id: str):
        task = self.repository.get_oldest_created()
        if task is None:
            return None
        self._transition(task, TaskStatus.CREATED, TaskStatus.ASSIGNED)

        task.worker_id = worker_id
        task.assigned_at = datetime.now(UTC)
        return task